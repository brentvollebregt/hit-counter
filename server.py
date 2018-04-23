import config
import db
import utils
from flask import Flask, request, send_file, make_response, render_template

app = Flask(__name__, static_url_path='')
db_connection = db.DbAccess(config.DATABASE_FILENAME)

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

    # Respond with count and status of 200 and give cookie back
    response = make_response(str(count), 200)
    response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

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

    svg = utils.getSVG(count).encode('utf-8')
    response = make_response(svg, 200)
    response.content_type = 'image/svg+xml'
    response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

@app.route("/nocount")
def nocountRoute():
    """ Return the count for a url """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    cookie = utils.getCookie(request, url)
    db_connection.clean()
    count = db_connection.getCount(url)
    db_connection.commit()

    response = make_response(str(count), 200)
    response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

@app.route("/nocount/tag.svg")
def nocountTagRoute():
    """ Return svg of count """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    cookie = utils.getCookie(request, url)
    db_connection.clean()
    count = db_connection.getCount(url)
    db_connection.commit()

    svg = utils.getSVG(count).encode('utf-8')
    response = make_response(svg, 200)
    response.content_type = 'image/svg+xml'
    response.set_cookie(url, cookie, expires=utils.getExpiration())
    return response

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port)