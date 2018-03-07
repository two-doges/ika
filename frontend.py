'''the front-end blueprint'''
import flask
from flask import render_template as render
import end_point


frontend = flask.Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    '''the index page of ika'''
    return render('index.html')


@frontend.route('/ika/', methods=['GET'])
def ika_list():
    '''return the ika list under root'''
    page = int(flask.request.args.get('page', '0'))
    ikas = end_point.get_reply(0, page*20+1, page*20+21)
    return render('ika_list.html', ikas=ikas, page=page)


@frontend.route('/ika/', methods=['POST'])
def ika_post():
    '''post a new ika'''
    user_id = flask.request.cookies.get('user_id', '')
    if user_id == '':
        user_id = end_point.new_poster()
    forward_id = flask.request.form['forward_id']
    poster_name = flask.request.form['name']
    comment = flask.request.form['comment']
    end_point.new_ika(forward_id, user_id, poster_name, comment)
    res = flask.make_response(render('post_success.html'))
    res.set_cookie('user_id', str(user_id))
    return res


@frontend.route('/ika/<int:ika_id>/')
def ika_page(ika_id):
    '''return the spec page of ika'''
    page = int(flask.request.args.get('page', '0'))
    ikas = end_point.get_reply(ika_id, page*20+1, page*20+21)
    return render('ika_page.html', ikas=ikas, page=page, ika_id=ika_id)
