import config
import random
import string
import datetime
from urllib.parse import urlparse
import time
import re

def getSVG(count, width, recWidth, textX, url):
    """ Put the count in the pre-defined svg and return it """
    return config.SVG_TEMPLATE.format(count=count, width=width, recWidth=recWidth, textX=textX, url=url)

def getURL(request):
    """ Get the url out of a request either passed as a query parameter or taken from the referrer. Remove any query """
    url = request.args.get('url', request.referrer)
    if url is None:
        return None
    parts = urlparse(url)
    return parts.netloc + parts.path

def checkURLWhitelist(url):
    if not len(config.URL_WHITELIST_RE):
        return True

    for reg in config.URL_WHITELIST_RE:
        if re.match(reg, url) is not None:
            return True
    return False

def checkValidCookie(request, url):
    """ Check if the cookies expiration hasn't passed """
    if url in request.cookies:
        expires = float(request.cookies.get(url))
        if expires > time.time():
            return True
    return False

def getCookieValueToSet():
    """ Will return the valid value for a cookie to be set """
    return str(time.time() + config.COOKIE_TIMEOUT)

def randomValue():
    """ Generate a random string from upper and lowercase letters and digits of a define length """
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(config.COOKIE_RANDOM_VALUE_LENGTH)])

def getExpiration():
    """ Get the expiration time in seconds using defined timeout """
    expire_date = datetime.datetime.now()
    return expire_date + datetime.timedelta(seconds=config.COOKIE_TIMEOUT)

def calculateSVGSizes(count):
    """ Calculate the size of the green half based off the length of count """
    text = str(count)
    sizes = {
        'width' : 80,
        'recWidth' : 50,
        'textX' : 55
    }
    if len(text) > 5:
        sizes['width'] += 6 * (len(text) - 5)
        sizes['recWidth'] += 6 * (len(text) - 5)
        sizes['textX'] += 3 * (len(text) - 5)

    return sizes
