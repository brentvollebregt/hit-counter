import config
import random
import string
import datetime
from urllib.parse import urlparse


def getSVG(count, width, recWidth, textX):
    """ Put the count in the pre-defined svg and return it """
    return config.SVG_TEMPLATE.format(count=count, width=width, recWidth=recWidth, textX=textX)

def getURL(request):
    """ Get the url out of a request either passed as a query parameter or taken from the referrer. Remove any query """
    url = request.args.get('url', request.referrer)
    if url is None:
        return None
    parts = urlparse(url)
    return parts.netloc + parts.path

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
