import config
import sqlite3 as lite
import time


class DbAccess:
    """ This provides access to the database to keep track of urls and views """
    def __init__(self, filename):
        """ Setup connection to file and create tables if they don't exist"""
        self.connection = lite.connect(filename)
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY, url VARCHAR(256), count INTEGER);')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS views (id INTEGER PRIMARY KEY, url_id INTEGER, value VARCHAR(64), time INTEGER, FOREIGN KEY (url_id) REFERENCES url(id));')

    def getCount(self, url):
        """ Get the count of a particular url """
        self.cursor.execute('SELECT count FROM url WHERE url=?', (url,))
        data = self.cursor.fetchone()
        if data is None:
            return 0
        else:
            return data[0]

    def addView(self, url, value):
        """ Create url entry if needed and increase url count and add cookie value to views if value is not stored """
        # Make sure the url entry exists
        count = self.getCount(url)
        if count == 0:
            self.cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
        # Get id of the url we are coutning
        self.cursor.execute('SELECT id FROM url WHERE url=?', (url, ))
        url_id = self.cursor.fetchone()[0]
        # Return if cookie value already here for the url
        self.cursor.execute('SELECT * FROM views WHERE url_id=? AND value=?', (url_id, value))
        if self.cursor.fetchone() is not None:
            return
        # Add 1 to the url count
        self.cursor.execute('UPDATE url SET count = count + 1 WHERE id=?', (url_id, ))
        # Add this view to the table with a timeout
        cookie_expiration = round(time.time() + config.COOKIE_TIMEOUT)
        self.cursor.execute('INSERT INTO views(url_id, value, time) VALUES(?, ?, ?)', (url_id, value, cookie_expiration))

    def commit(self):
        """ Commit """
        self.connection.commit()

    def clean(self):
        """ Remove view rows that have expired """
        self.cursor.execute('DELETE FROM views WHERE time < ?', (time.time(), ))
