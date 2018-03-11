'''the front-end blueprint'''
import datetime
import flask
from flask import render_template as render
from flask import url_for, redirect, request
from requests import post
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
    l_p = url_for('frontend.ika_list', t=t, page=page-1)
    n_p = url_for('frontend.ika_list', t=t, page=page+1)
    if page <= 0:
        page = 0
        l_p = None
    if page >= max_page:
        n_p = None
        page = max_page
    ikas = endpoint.get_reply(tid, 20, page*20)
    # t means topic, again
    return render('ika_list.html',
                  fid=tid, ikas=ikas, l_p=l_p, n_p=n_p,
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
    l_p = url_for('frontend.ika_page', ika_id=ika_id, page=page-1)
    n_p = url_for('frontend.ika_page', ika_id=ika_id, page=page+1)
    if page <= 0:
        page = 0
        l_p = None
    if page >= max_page:
        page = max_page
        n_p = None
    ikas = endpoint.get_reply(ika_id, 20, page*20)
    return render('ika_list.html',
                  ikas=ikas, l_p=l_p, fid=ika_id, n_p=n_p,
                  topics=endpoint.get_topics())


@frontend.route('/ika/', methods=['POST'])
def ika_post():
    '''post a new ika'''
    user_id = flask.request.cookies.get('user_id', '')
    try:
        user_hash = endpoint.verify_user_id(user_id)
    except RuntimeError:
        # get user ip (bypass nginx)
        user_id = endpoint.gen_user_id(request.remote_addr)
        user_hash = endpoint.verify_user_id(user_id)
    forward_id = request.form.get('forward_id')
    name = request.form.get('name')
    title = request.form.get('title')
    comment = request.form.get('comment')
    # resolve with image
    image = request.files.get('image')
    if image:
        url = 'https://sm.ms/api/upload'
        res = post(url, files={'smfile': image})
        if res.json()['code'] == 'success':
            image = res.json()['data']['url']
        else:
            raise flask.app.InternalServerError
    if not comment and not image:
        return render('post_error.html', error='请输入内容',
                      topics=endpoint.get_topics())
    try:
        endpoint.new_ika(forward_id, user_hash, name, title, image, comment)
    except RuntimeError as err:
        return render('post_error.html', error=err,
                      topics=endpoint.get_topics())
    res = flask.make_response(render('post_success.html',
                                     topics=endpoint.get_topics()))
    outdate = datetime.datetime.today() + datetime.timedelta(days=30)
    res.set_cookie('user_id', user_id, expires=outdate)
    return res
