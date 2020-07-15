import os
import re
import sqlite3 as lite

import config

class DbAccess:
    """ This provides access to the database to keep track of urls and views """

    def __init__(self, filename):
        """ Setup connection to file and create tables if they don't exist"""
        self.filename = filename
        self.connection = None

        # Create folder for database file if it doesn't already exist
        if not os.path.exists(os.path.dirname(filename)):
            print('WARN: The parent directory for ' + filename + ' does not exist so it will be created.')
            os.makedirs(os.path.dirname(filename), exist_ok=True)

        self.connect()
        cursor = self.connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY, url VARCHAR(256), count INTEGER);')

    def connect(self):
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None

        self.connection = lite.connect(self.filename, check_same_thread=False)
        self.connection.execute('pragma journal_mode=wal')
        self.connection.create_function('REGEXP', 2, regexp)

    def get_connection(self):
        """ Get the cursor to use in the current thread and remove rows that have expired in views"""
        if self.connection is None:
            self.connect()
        return self.connection

    def getCount(self, url):
        """ Get the count of a particular url """
        cursor = self.connection.cursor()
        cursor.execute('SELECT count FROM url WHERE url=?', (url,))
        data = cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def addView(self, url):
        """ Create url entry if needed and increase url count and add cookie value to views if value is not stored """
        cursor = self.connection.cursor()
        # Make sure the url entry exists
        count = self.getCount(url)
        if count == 0:
            cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
        # Add 1 to the url count
        cursor.execute('UPDATE url SET count = count + 1 WHERE url=?', (url,))
        self.connection.commit()

    def getTopSites(self, amount=10):
        """ Get the top domains using this tool by hits. Ignore specified domains """
        return self.getTop(amount, 'domains')

    def getTopUrls(self, amount=10):
        """ Get the top urls using this tool by hits. Ignore specified domains """
        return self.getTop(amount, 'urls')

    def getTop(self, amount, what='domains'):
        query = self._top_urls_query() if what == 'urls' else self._top_domains_query()
        # Select all entities and counts
        cursor = self.connection.cursor()
        cursor.execute(
            query,
            [*[str(r) for r in config.TOP_SITES_IGNORE_DOMAIN_RE_MATCH], amount]
        )
        result = cursor.fetchall()

        entities, values = [], {}
        for row in result:
            url, domain, count = row
            if url == b'':
                continue
            entities.append(url)
            values[url] = count

        # Return sorted entities and their values, this allows for lower Python version support
        return {
            what: entities,
            'values': values
        }

    def _top_domains_query(self):
        sep = '\nAND '
        return f"""
            SELECT url, substr(url, 0, instr((url || '/'), '/')) as domain, SUM(count) as domain_sum
            FROM url
            WHERE domain != ''
            GROUP BY domain
            HAVING {sep.join(['domain NOT REGEXP ?' for _ in range(len(config.TOP_SITES_IGNORE_DOMAIN_RE_MATCH))])}
            ORDER BY domain_sum DESC
            LIMIT ?;
        """

    def _top_urls_query(self):
        sep = '\nAND '
        return f"""
            SELECT url, substr(url, 0, instr((url || '/'), '/')) as domain, SUM(count) as url_sum
            FROM url
            WHERE domain != ''
            GROUP BY url
            HAVING {sep.join(['domain NOT REGEXP ?' for _ in range(len(config.TOP_SITES_IGNORE_DOMAIN_RE_MATCH))])}
            ORDER BY url_sum DESC
            LIMIT ?;
        """