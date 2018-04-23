import db
from flask import Flask

app = Flask(__name__, static_url_path='')

@app.route("/")
def homeRoute():
    """ Home + tool to create (nocount/count + url in url) """
    pass

@app.route("/count")
def homeRoute():
    """ Return the count for a url and add 1 to it """
    pass

@app.route("/count/tag.svg")
def homeRoute():
    """ Return svg of count and add 1 to url """
    pass

@app.route("/nocount")
def homeRoute():
    """ Return the count for a url """
    pass

@app.route("/nocount/tag.svg")
def homeRoute():
    """ Return svg of count """
    pass