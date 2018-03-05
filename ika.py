import flask

App = flask.Flask(__name__)

@App.route('/')
def ika():
    return 'Hello World'
