import config
import sqlite3 as lite
import time


class DbAccess:
    """ This provides access to the database to keep track of urls and views """
    def __init__(self, filename):
        """ Setup connection to file and create tables if they don't exist"""
        self.filename = filename
        connection = lite.connect(filename)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY, url VARCHAR(256), count INTEGER);')
        cursor.execute('CREATE TABLE IF NOT EXISTS views (id INTEGER PRIMARY KEY, url_id INTEGER, value VARCHAR(64), time INTEGER, FOREIGN KEY (url_id) REFERENCES url(id));')

    def get_connection(self):
        """ Get the cursor to use in the current thread and remove rows that have expired in views"""
        connection = lite.connect(self.filename)
        cursor = connection.cursor()
        cursor.execute('DELETE FROM views WHERE time < ?', (time.time(),))
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

    def addView(self, connection, url, value):
        """ Create url entry if needed and increase url count and add cookie value to views if value is not stored """
        cursor = connection.cursor()
        # Make sure the url entry exists
        count = self.getCount(connection, url)
        if count == 0:
            cursor.execute('INSERT INTO url(url, count) VALUES(?, ?)', (url, 0))
        # Get id of the url we are counting
        cursor.execute('SELECT id FROM url WHERE url=?', (url, ))
        url_id = cursor.fetchone()[0]
        # Return if cookie value already here for the url
        cursor.execute('SELECT * FROM views WHERE url_id=? AND value=?', (url_id, value))
        if cursor.fetchone() is not None:
            return
        # Add 1 to the url count
        cursor.execute('UPDATE url SET count = count + 1 WHERE id=?', (url_id, ))
        # Add this view to the table with a timeout
        cookie_expiration = round(time.time() + config.COOKIE_TIMEOUT)
        cursor.execute('INSERT INTO views(url_id, value, time) VALUES(?, ?, ?)', (url_id, value, cookie_expiration))
        connection.commit()
