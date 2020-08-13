import datetime
import random
import re
import string
import time
from urllib.parse import urlparse

from flask import request

import config


def __get_url():
    """ Get the url out of a request either passed as a query parameter or taken from the referrer. Remove any query """
    url = request.args.get('url', request.referrer)
    if url is None:
        return None
    parts = urlparse(url)
    return parts.netloc + parts.path


def __validate_url(url):
    if url is None or url == '':
        return "Could not find a requested url", 404

    for regex in config.URL_BLACKLIST_RE:
        if re.match(regex, url) is not None:
            return "URL has been blacklisted", 403

    if len(config.URL_WHITELIST_RE) != 0:
        for reg in config.URL_WHITELIST_RE:
            if re.match(reg, url) is not None:
                break
        else:
            return "Requested url is not whitelisted", 403

    return None


def get_and_validate_url(func):
    def wrapper(*args, **kwargs):
        # Get URL
        url = __get_url()

        # Validate the URL
        errors = __validate_url(url)
        if errors is not None:
            return errors

        # Return response if validation passed
        return func(url, *args, **kwargs)
    return wrapper


def get_svg(count, width, rec_width, text_x, url):
    """ Put the count in the pre-defined svg and return it """
    return config.SVG_TEMPLATE.format(count=count, width=width, recWidth=rec_width, textX=text_x, url=url)


def check_url_whitelist(url):
    if not len(config.URL_WHITELIST_RE):
        return True

    for reg in config.URL_WHITELIST_RE:
        if re.match(reg, url) is not None:
            return True
    return False


def check_valid_cookie(current_request, url):
    """ Check if the cookies expiration hasn't passed """
    if url in current_request.cookies:
        expires = float(current_request.cookies.get(url))
        if expires > time.time():
            return True
    return False


def get_cookie_value_to_set():
    """ Will return the valid value for a cookie to be set """
    return str(time.time() + config.COOKIE_TIMEOUT)


def random_value():
    """ Generate a random string from upper and lowercase letters and digits of a define length """
    possible_characters = string.ascii_letters + string.digits
    return ''.join([random.choice(possible_characters) for _ in range(config.COOKIE_RANDOM_VALUE_LENGTH)])


def get_expiration():
    """ Get the expiration time in seconds using defined timeout """
    expire_date = datetime.datetime.now()
    return expire_date + datetime.timedelta(seconds=config.COOKIE_TIMEOUT)


def calculate_svg_sizes(count):
    """ Calculate the size of the green half based off the length of count """
    text = str(count)
    sizes = {
        'width': 80,
        'recWidth': 50,
        'textX': 55
    }
    if len(text) > 5:
        sizes['width'] += 6 * (len(text) - 5)
        sizes['recWidth'] += 6 * (len(text) - 5)
        sizes['textX'] += 3 * (len(text) - 5)

    return sizes
