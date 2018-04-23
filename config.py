DATABASE_FILENAME = 'data.db'
COOKIE_TIMEOUT = 600
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
</svg>"""
RANDOM_VALUE_LENGTH = 12
