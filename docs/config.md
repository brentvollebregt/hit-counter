# Server Configuration

[config.py](../config.py) contains server configuration variables.

## `DATABASE_FILE_PATH`
The location of the SQLite database file. defaults to `data.db` in the current working directory. Can be overridden with the `DATABASE_FILE_PATH` environment variable.

## `COOKIE_TIMEOUT`
The amount of time in seconds before another view by the same user will count.

## `COOKIE_RANDOM_VALUE_LENGTH`
Length of cookie value (stored client side). Literally just the cookie size.

## `SVG_TEMPLATE`
The template of the SVG to respond with. Must take `count`, `width`, `recWidth`, `textX` and `url`.

## `ENABLE_SSL`
Enable SSL. Defaults to false for debugging purposes. Can be overridden with the `ENABLE_SSL` environment variable.

## `CANNOT_FIND_URL_MESSAGE`
Message to return on a 404.

## `FORBIDDEN_URL_MESSAGE`
Message to return on a 403.

## `TOP_SITES_IGNORE_DOMAIN_RE_MATCH`
Regular expressions to ignore when getting top sites. If a URL matches one of these expressions, the URL will be ignored in the domain calculation.

## `URL_WHITELIST_RE`
Regular expressions to decide which URLs to count and return an SVG for. If the server identifies a URL that does not match a regular expression in this list, it will return a 403. Leaving this list empty will disable the whitelist feature.

For example, adding `r'github\.com'` will only allow URLs with `github\.com` in them to be given a non-403 response.
