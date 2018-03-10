'''the front-end blueprint'''
import flask
from flask import render_template as render
from flask import url_for, redirect
import endpoint


frontend = flask.Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    '''the index page of ika'''
    return render('index.html', topics=endpoint.get_topics())


@frontend.route('/t/<string:t>', methods=['GET'])
def ika_list(t):  # t means topic
    '''return the ika list under root'''
    # if no topic endpoint will raise 404
    topic = endpoint.get_topic(t)
    tid = topic.topic_id * -1
    ika_number = endpoint.get_ika_number(tid)
    # set the max page
    if ika_number is 0:
        max_page = 0
    else:
        # page range is [0, (target_ika.number-1)//20]
        max_page = (ika_number-1) // 20
    page = int(flask.request.args.get('page', '0'))
    # next page
    n_p = True
    if page < 0:
        page = 0
    if page >= max_page:
        n_p = False
        page = max_page
    ikas = endpoint.get_reply(tid, 20, page*20)
    # t means topic, again
    return render('ika_list.html',
                  fid=tid, ikas=ikas, page=page, next_page=n_p,
                  t=topic.topic_title, topics=endpoint.get_topics())


@frontend.route('/ika/<int:ika_id>/')
def ika_page(ika_id):
    '''return the spec page of ika'''
    target_ika = endpoint.get_ika(ika_id)
    # redir to the root is no this ika
    if not target_ika:
        flask.abort(404)
    # redir to the forward_ika if this ika's fid is not root
    if target_ika.forward_ika_id > 0:
        nika_id = target_ika.forward_ika_id
        # find the spec ika
        url = url_for('frontend.ika_page', ika_id=nika_id)+'#'+str(ika_id)
        return redirect(url)
    # set the max page
    ika_number = endpoint.get_ika_number(ika_id)
    if ika_number == 0:
        max_page = 0
    else:
        max_page = (ika_number-1) // 20
    # resolve page
    page = int(flask.request.args.get('page', '0'))
    # if there is a next page n_p = next page
    n_p = True
    if page < 0:
        page = 0
    if page >= max_page:
        page = max_page
        n_p = False
    ikas = endpoint.get_reply(ika_id, 20, page*20)
    return render('ika_list.html',
                  ikas=ikas, page=page, fid=ika_id, next_page=n_p,
                  topics=endpoint.get_topics())


@frontend.route('/ika/', methods=['POST'])
def ika_post():
    '''post a new ika'''
    user_id = flask.request.cookies.get('user_id', '')
    if user_id == '':
        user_id = endpoint.new_user_id()
    forward_id = flask.request.form['forward_id']
    name = flask.request.form['name']
    title = flask.request.form['title']
    comment = flask.request.form['comment']
    if not comment:
        return render('post_error.html', error='请输入内容',
                      topics=endpoint.get_topics())
    endpoint.new_ika(forward_id, user_id, name, title, None, comment)
    res = flask.make_response(render('post_success.html',
                                     topics=endpoint.get_topics()))
    res.set_cookie('user_id', str(user_id))
    return res
