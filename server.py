from flask import Flask, request, make_response, render_template

import config
import db
import utils


app = Flask(__name__, static_url_path='')
db_connection = db.DbAccess(config.DATABASE_FILE_PATH)

# Prometheus metrics
if config.EXPOSE_METRICS:
    from metrics import init_metrics
    init_metrics(app, db_connection)


def add_cookie(response, url):
    """ Add a cookie that may later be checked for repeated requests in small amounts of time """
    response.set_cookie(
        url,
        utils.get_cookie_value_to_set(),
        expires=utils.get_expiration(),
        secure=True,
        samesite="none"
    )


def make_text_response(count, url, cookie_required):
    """ Create a request with the count with a 200 status and give cookie back """
    response = make_response(str(count), 200)
    if cookie_required:
        add_cookie(response, url)
    return response


def make_svg_response(count, url, cookie_required):
    sizes = utils.calculate_svg_sizes(count)
    svg = utils.get_svg(count, sizes['width'], sizes['recWidth'], sizes['textX'], url).encode('utf-8')
    response = make_response(svg, 200)
    response.content_type = 'image/svg+xml'
    if cookie_required:
        add_cookie(response, url)
    return response


@app.route("/")
def home_route():
    """ Home + tool to create (nocount/count + url in url) """
    connection = db_connection.get_connection()
    return render_template(
        'index.html',
        top_domains=db_connection.get_top_sites(connection, config.NUM_TOP_DOMAINS),
        top_urls=db_connection.get_top_urls(connection, config.NUM_TOP_URLS),
        top_domain_amount=config.NUM_TOP_DOMAINS,
        top_url_amount=config.NUM_TOP_URLS
    )


@app.route("/count", endpoint="count_raw_route")
@utils.get_and_validate_url
def count_raw_route(url):
    """ Return the count for a url and add 1 to it """
    # Get/generate cookie, cleanup views, add a view, get the count and commit changes
    valid_cookie = utils.check_valid_cookie(request, url)
    connection = db_connection.get_connection()
    if not valid_cookie:
        db_connection.add_view(connection, url)
    count = db_connection.get_count(connection, url)

    return make_text_response(count, url, not valid_cookie)


@app.route("/count/tag.svg", endpoint="count_tag_route")
@utils.get_and_validate_url
def count_tag_route(url):
    """ Return svg of count and add 1 to url """
    valid_cookie = utils.check_valid_cookie(request, url)
    connection = db_connection.get_connection()
    if not valid_cookie:
        db_connection.add_view(connection, url)
    count = db_connection.get_count(connection, url)

    return make_svg_response(count, url, not valid_cookie)


@app.route("/nocount", endpoint="no_count_raw_route")
@utils.get_and_validate_url
def no_count_raw_route(url):
    """ Return the count for a url """
    connection = db_connection.get_connection()
    count = db_connection.get_count(connection, url)

    return make_text_response(count, url, False)


@app.route("/nocount/tag.svg", endpoint="no_count_tag_route")
@utils.get_and_validate_url
def no_count_tag_route(url):
    """ Return svg of count """
    connection = db_connection.get_connection()
    count = db_connection.get_count(connection, url)

    return make_svg_response(count, url, False)


@app.after_request
def add_header(r):
    # Disable caching: https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"

    # Allow cookies to be send from cross-origins
    r.headers["Access-Control-Allow-Origin"] = request.origin if request.origin is not None else '*'
    r.headers["Access-Control-Allow-Credentials"] = 'true'
    return r


if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port, ssl_context=('cert.pem', 'key.pem'))
