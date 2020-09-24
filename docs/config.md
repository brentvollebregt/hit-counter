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

## `EXPOSE_METRICS`
Enable [Prometheus](https://prometheus.io) metrics at the `/metrics` endpoint. Defaults to false for performance reasons. Can be overridden with the `EXPOSE_METRICS` environment variable. However, use this feature with care. It is recommended only for moderately large deployments of _hit-counter_, as a separate metric will be exposed for every URL in your data base.  

### `METRICS_PREFIX`
Configure the prefix to me used for all Prometheus measurements. Defaults to `hitcounter`, resulting in metrics labels like `hitcounter_hits_total`.

## `NUM_TOP_DOMAINS`
The number of top domains to display on the home page; set to 0 to disable. Can be overridden with the `NUM_TOP_DOMAINS` environment variable.

## `NUM_TOP_URLS`
The number of top URLs to display on the home page; set to 0 to disable. Can be overridden with the `NUM_TOP_URLS` environment variable.

## `TOP_SITES_IGNORE_DOMAIN_RE_MATCH`
Regular expressions to ignore when getting top sites. If a URL matches one of these expressions, the URL will be ignored in the domain calculation.

## `URL_WHITELIST_RE`
Regular expressions to decide which URLs to count and return an SVG for. If the server identifies a URL that does not match a regular expression in this list, it will return a 403. Leaving this list empty will disable the whitelist feature.

For example, adding `r'github\.com'` will only allow URLs with `github\.com` in them to be given a non-403 response.

## `URL_BLACKLIST_RE`
Regular expressions to decide which URLs to block and return a 403 for. Blacklist regular expressions are checked before whitelist regular expressions.

For example, adding `r'example\.com'` will block all requests for example.com.
