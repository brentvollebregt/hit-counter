import config
import sqlite3 as lite
import time


class DbAccess:
    """ This provides access to the database to keep track of views
    Tables:
        - URLs (keeps track of urls and counts)
            - id
            - url
            - count
        - Views (stops the refresh issue for a set amount of time)
            - id
            - URL_id
            - value (provided from cookie)
            - time
    """
    def __init__(self, filename):
        self.connection = lite.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY, url VARCHAR(256), count INTEGER);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS views (id INTEGER PRIMARY KEY, url_id INTEGER, value VARCHAR(64), time INTEGER, FOREIGN KEY (url_id) REFERENCES url(id));')

    def getCount(self, url):
        self.cursor.execute('SELECT count FROM url WHERE url=?', (url,))
        data = self.cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def addView(self, url, value):
        # Make sure the url entry exists
        count = self.getCount(url)
        if count == 0:
            self.cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
        # Get id of the url we are coutning
        self.cursor.execute('SELECT id FROM url WHERE url=?', (url,))
        url_id = self.cursor.fetchone()[0]
        # Return if cookie value already here for the url
        self.cursor.execute('SELECT * FROM views WHERE url_id=? AND value=?', (url_id, value))
        if self.cursor.fetchone() is not None:
            return
        # Add 1 to the url count
        self.cursor.execute('UPDATE url SET count = count + 1 WHERE id=?', (url_id, ))
        # Add this view to the table with a timeout
        cookie_expiration = time.time() + config.COOKIE_TIMEOUT
        self.cursor.execute('INSERT INTO views(url_id, value, time) VALUES(?, ?, ?)', (url_id, value, cookie_expiration))

    def commit(self):
        self.connection.commit()

    def clean(self):
        # Remove items that are less than time.time()
        pass
