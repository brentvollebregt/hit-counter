import config
import db
import utils
from flask import Flask, request, make_response, render_template


app = Flask(__name__, static_url_path='')
db_connection = db.DbAccess(config.DATABASE_FILENAME)

if config.ENABLE_SSL:
    from flask_sslify import SSLify
    sslify = SSLify(app)


def makeTextRequest(count, url, cookie):
    """ Create a request with the count with a 200 status and give cookie back """
    response = make_response(str(count), 200)
    if cookie is not None:
        response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

def makeSVGRequest(count, url, cookie):
    sizes = utils.calculateSVGSizes(count)
    svg = utils.getSVG(count, sizes['width'], sizes['recWidth'], sizes['textX']).encode('utf-8')
    response = make_response(svg, 200)
    response.content_type = 'image/svg+xml'
    if cookie is not None:
        response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

@app.route("/")
def homeRoute():
    """ Home + tool to create (nocount/count + url in url) """
    return render_template('index.html')

@app.route("/count")
def countRoute():
    """ Return the count for a url and add 1 to it """
    # Attempt to find any sign of a url, return 404 if we can't find anything
    url = utils.getURL(request)
    if url is None:
        return config.CANNOT_FIND_URL_MESSAGE, 404

    # Get/generate cookie, cleanup views, add a view, get the count and commit changes
    cookie = utils.getCookie(request, url)
    connection = db_connection.get_connection()
    db_connection.addView(connection, url, cookie)
    count = db_connection.getCount(connection, url)

    return makeTextRequest(count, url, cookie)

@app.route("/count/tag.svg")
def countTagRoute():
    """ Return svg of count and add 1 to url """
    url = utils.getURL(request)
    if url is None:
        return config.CANNOT_FIND_URL_MESSAGE, 404

    cookie = utils.getCookie(request, url)
    connection = db_connection.get_connection()
    db_connection.addView(connection, url, cookie)
    count = db_connection.getCount(connection, url)

    return makeSVGRequest(count, url, cookie)

@app.route("/nocount")
def nocountRoute():
    """ Return the count for a url """
    url = utils.getURL(request)
    if url is None:
        return config.CANNOT_FIND_URL_MESSAGE, 404

    connection = db_connection.get_connection()
    count = db_connection.getCount(connection, url)

    return makeTextRequest(count, url, None)

@app.route("/nocount/tag.svg")
def nocountTagRoute():
    """ Return svg of count """
    url = utils.getURL(request)
    if url is None:
        return config.CANNOT_FIND_URL_MESSAGE, 404

    connection = db_connection.get_connection()
    count = db_connection.getCount(connection, url)

    return makeSVGRequest(count, url, None)

@app.after_request
def add_header(r):
    """
    Disable caching - https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
    Also fix "No 'Access-Control-Allow-Origin' header is present on the requested resource."
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Access-Control-Allow-Origin"] = '*'
    return r

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port)