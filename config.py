DATABASE_FILENAME = 'data.db' # Location of database
COOKIE_TIMEOUT = 600 # In seconds
SVG_TEMPLATE = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" width="80" height="20">

<rect width="30" height="20" fill="#555"/>
<rect x="30" width="50" height="20" fill="#4c1"/>

<rect rx="3" width="80" height="20" fill="transparent"/>
	<g fill="#fff" text-anchor="middle"
    font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
	    <text x="15" y="14">hits</text>
	    <text x="54" y="14">{count}</text>
	</g>
</svg>""" # Template of SVG with {count} to be provided
RANDOM_VALUE_LENGTH = 12 # Length of cookie value (stored both server and client side)
