import os

# Location of database
DATABASE_FILE_PATH = os.path.abspath(os.getenv('DATABASE_FILE_PATH', 'data.db'))

# Amount of time before another view by the same user will count
COOKIE_TIMEOUT = 60 * 5

# Length of cookie value (stored client side). Literally just the cookie size.
COOKIE_RANDOM_VALUE_LENGTH = 12

# Template of SVG with {count} to be provided
SVG_TEMPLATE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20">
<rect width="30" height="20" fill="#555"/>
<rect x="30" width="{recWidth}" height="20" fill="#4c1"/>
<rect rx="3" width="80" height="20" fill="transparent"/>
	<g fill="#fff" text-anchor="middle"
    font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
	    <text x="15" y="14">hits</text>
	    <text x="{textX}" y="14">{count}</text>
	</g>
<!-- This count is for the url: {url} -->
</svg>"""

# Message to return on a 404
CANNOT_FIND_URL_MESSAGE = "Could not find a requested url"

# Enable SSL (set ENABLE_SSL=true to enable)
ENABLE_SSL = os.getenv('ENABLE_SSL', 'false').lower() == 'true'

# Regular expressions to ignore when getting top sites
TOP_SITES_IGNORE_DOMAIN_RE_MATCH = [r'192\.168\.\d{1,3}\.\d{1,3}', r'127\.0\.\d{1,3}\.\d{1,3}', r'^$']
