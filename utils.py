import config
import random
import string


def getSVG(count):
    return config.SVG_TEMPLATE.format(count=count)

def getURL(request):
    return request.args.get('url', request.referrer)

def getCookie(request, url):
    # return request.cookies[url] if url in request.cookies else randomValue()
    if url in request.cookies:
        return request.cookies[url]
    else:
        return randomValue()

def randomValue():
    return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(config.RANDOM_VALUE_LENGTH)])
