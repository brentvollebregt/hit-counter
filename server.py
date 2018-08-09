import config
import db
import utils
from flask import Flask, request, make_response, render_template
# from flask_sslify import SSLify

app = Flask(__name__, static_url_path='')
# sslify = SSLify(app)
db_connection = db.DbAccess(config.DATABASE_FILENAME)

def makeTextRequest(count, url, cookie):
    """ Create a request with the count with a 200 status and give cookie back """
    response = make_response(str(count), 200)
    if not cookie is None:
        response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

def makeSVGRequest(count, url, cookie):
    sizes = utils.calculateSVGSizes(count)
    svg = utils.getSVG(count, sizes['width'], sizes['recWidth'], sizes['textX']).encode('utf-8')
    response = make_response(svg, 200)
    response.content_type = 'image/svg+xml'
    if not cookie is None:
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
        return "", 404

    # Get/generate cookie, cleanup views, add a view, get the count and commit changes
    cookie = utils.getCookie(request, url)
    db_connection.clean()
    db_connection.addView(url, cookie)
    count = db_connection.getCount(url)
    db_connection.commit()

    return makeTextRequest(count, url, cookie)

@app.route("/count/tag.svg")
def countTagRoute():
    """ Return svg of count and add 1 to url """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    cookie = utils.getCookie(request, url)
    db_connection.clean()
    db_connection.addView(url, cookie)
    count = db_connection.getCount(url)
    db_connection.commit()

    return makeSVGRequest(count, url, cookie)

@app.route("/nocount")
def nocountRoute():
    """ Return the count for a url """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    count = db_connection.getCount(url)

    return makeTextRequest(count, url, None)

@app.route("/nocount/tag.svg")
def nocountTagRoute():
    """ Return svg of count """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    count = db_connection.getCount(url)

    return makeSVGRequest(count, url, None)

@app.after_request
def add_header(r):
    """
    Disable caching - https://stackoverflow.com/questions/34066804/disabling-caching-in-flask
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port)