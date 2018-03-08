'''the front-end blueprint'''
import flask
from flask import render_template as render
from flask import url_for, redirect
import end_point


frontend = flask.Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    '''the index page of ika'''
    return render('index.html')


@frontend.route('/ika/', methods=['GET'])
def ika_list():
    '''return the ika list under root'''
    target_ika = end_point.get_ika(0)
    # set the max page
    if target_ika.number == 0:
        max_page = 0
    else:
        max_page = (target_ika.number-1) // 20
    # page range is [0, (target_ika.number-1)/20]
    page = int(flask.request.args.get('page', '0'))
    if page < 0:
        page = 0
    elif page > max_page:
        page = max_page
    if page < 0:
        page = 0
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
    if not comment:
        return render('post_error.html', error='请输入内容')
    end_point.new_ika(forward_id, user_id, poster_name, comment)
    res = flask.make_response(render('post_success.html'))
    res.set_cookie('user_id', str(user_id))
    return res


@frontend.route('/ika/<int:ika_id>/')
def ika_page(ika_id):
    '''return the spec page of ika'''
    target_ika = end_point.get_ika(ika_id)
    # redir to the root is no this ika
    if not target_ika:
        return redirect(url_for('ika_list'))
    # redir to the forward_ika if this ika's fid is not root
    if target_ika.forward_ika != 0:
        return redirect(url_for('ika_page', ika_id=target_ika.forward_ika))
    # set the max page
    if target_ika.number == 0:
        max_page = 0
    else:
        max_page = (target_ika.number-1) // 20
    # resolve page
    page = int(flask.request.args.get('page', '0'))
    if page < 0:
        page = 0
    elif page > max_page:
        page = max_page
    ikas = end_point.get_reply(ika_id, page*20+1, page*20+21)
    return render('ika_page.html', ikas=ikas, page=page, ika_id=ika_id)
