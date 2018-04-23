import config
import random
import string
import datetime


def getSVG(count):
    """ Put the count in the pre-defined svg and return it """
    return config.SVG_TEMPLATE.format(count=count)

def getURL(request):
    """ Get the url out of a request either passed as a query parameter or taken from the referrer """
    return request.args.get('url', request.referrer)

def getCookie(request, url):
    """ Get the cookie out of the request relative to the url provided or generate a new value if it doesn't exist"""
    if url in request.cookies:
        return request.cookies[url]
    else:
        return randomValue()

def randomValue():
    """ Generate a random string from upper and lowercase letters and digits of a define length """
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(config.RANDOM_VALUE_LENGTH)])

def getExpiration():
    expire_date = datetime.datetime.now()
    return expire_date + datetime.timedelta(seconds=config.COOKIE_TIMEOUT)
