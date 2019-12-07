import sqlite3 as lite
import config
from collections import defaultdict
import re


class DbAccess:
    """ This provides access to the database to keep track of urls and views """
    def __init__(self, filename):
        """ Setup connection to file and create tables if they don't exist"""
        self.filename = filename
        connection = lite.connect(filename)
        connection.execute('pragma journal_mode=wal')
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY, url VARCHAR(256), count INTEGER);')

    def get_connection(self):
        """ Get the cursor to use in the current thread and remove rows that have expired in views"""
        connection = lite.connect(self.filename)
        return connection

    def getCount(self, connection, url):
        """ Get the count of a particular url """
        cursor = connection.cursor()
        cursor.execute('SELECT count FROM url WHERE url=?', (url,))
        data = cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def addView(self, connection, url):
        """ Create url entry if needed and increase url count and add cookie value to views if value is not stored """
        cursor = connection.cursor()
        # Make sure the url entry exists
        count = self.getCount(connection, url)
        if count == 0:
            cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
        # Add 1 to the url count
        cursor.execute('UPDATE url SET count = count + 1 WHERE url=?', (url, ))
        connection.commit()

    def getTopSites(self, connection, amount=10):
        """ Get the top domains using this tool by hits. Ignore specified domains """
        # Select all urls and counts
        cursor = connection.cursor()
        cursor.execute('select url, count from url')
        urls_and_counts = cursor.fetchall()

        # Get total hits per domain
        site_counts = defaultdict(int)
        for row in urls_and_counts:
            if row[0] == b'':
                continue
            # Get the domain - part before the first '/'
            domain = row[0].split('/')[0]
            # Check if domain is on the ignore list
            on_ignore = False
            for regex in config.TOP_SITES_IGNORE_DOMAIN_RE_MATCH:
                if re.match(regex, domain) is not None:
                    on_ignore = True
                    break
            if on_ignore:
                continue
            # Add hit counts to the domain
            site_counts[domain] += row[1]

        # Sort the domains by hits
        sorted_sites = sorted(site_counts, key=lambda x: site_counts[x], reverse=True)

        # Return sorted domains and their values, this allows for lower Python version support
        return {
            'domains': sorted_sites[:amount],
            'values': {site: site_counts[site] for site in site_counts}
        }
