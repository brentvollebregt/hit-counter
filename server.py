import config
import db
import utils
from flask import Flask, request, send_file, make_response

app = Flask(__name__, static_url_path='')
db_connection = db.DbAccess(config.DATABASE_FILENAME)

@app.route("/")
def homeRoute():
    """ Home + tool to create (nocount/count + url in url) """
    render_template('index.html')


@app.route("/count")
def countRoute():
    """ Return the count for a url and add 1 to it """
    url = utils.getURL(request)
    if url is None:
        return "", 404

    cookie = utils.getCookie(request, url)
    db_connection.addView(url, cookie)
    count = db_connection.getCount(url)
    db_connection.commit()

    response = make_response(str(count), 200)
    response.set_cookie(url, cookie)
    return response

@app.route("/count/tag.svg")
def countTagRoute():
    """ Return svg of count and add 1 to url """
    # svg = StringIO()
    # svg.write(getSVG(count))
    # svg.seek(0)
    # return send_file(svg, mimetype='image/svg+xml')
    pass

@app.route("/nocount")
def nocountRoute():
    """ Return the count for a url """
    pass

@app.route("/nocount/tag.svg")
def nocountTagRoute():
    """ Return svg of count """
    pass

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    print("Site starting on http://" + ip + ":" + str(port))
    app.run(host=ip, port=port)