import config
import sqlite3 as lite


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
    def __init__(self):
        connection = lite.connect(config.DATABASE_FILENAME)
        self.cursor = connection.cursor()

    def getUrl(self, url):
        pass

    def addView(self, url, value):
        pass

    def clean(self):
        pass
