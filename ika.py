'''the main mod of ika'''
import flask
from flask_bootstrap import Bootstrap
from frontend import frontend


app = flask.Flask(__name__)
Bootstrap(app)
app.register_blueprint(frontend)


if __name__ == '__main__':
    app.run(debug=True)
