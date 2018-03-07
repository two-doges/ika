'''the front-end blueprint'''
import flask


frontend = flask.Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    '''the index page of ika'''
    return flask.render_template('index.html')


@frontend.route('/ika')
def ika_list():
    '''return the ika list'''


@frontend.route('/ika/<int:ika_id>')
def ika_page():
    '''return the spec page of ika'''
    pass
