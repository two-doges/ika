'''endpoint for ika'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config
import datetime
from user_hash import gen_user_id, verify_user_id


# db init and return app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# da orm topic
class Ika_topic(db.Model):
    '''Ika topic orm'''
    # topic id < 0 for each topic
    # but id store in db is > 0
    topic_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # topic title
    topic_title = db.Column(db.String(20), nullable=False)
    # topic shortcut
    shortcut = db.Column(db.String(10), nullable=False)
    # last reply ika id
    last_ika_id = db.Column(db.Integer)


# db orm class
class Ika(db.Model):
    '''Ika class for orm'''
    # auto increase int primary id
    ika_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # forward ika id
    # if this ika is under root, fid <= 0 (and in behalf of topic id)
    # else fid > 0 always
    forward_ika_id = db.Column(db.Integer, nullable=False)
    # announcer name
    name = db.Column(db.String(80))
    # announcer id
    user_id = db.Column(db.String(120), nullable=False)
    # ika title
    title = db.Column(db.String(120))
    # post time use utc
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # image url (not must)
    image_url = db.Column(db.String(100))
    # last reply ika id
    last_ika_id = db.Column(db.Integer)
    # saga means lock by admin.
    # only ika under root can be sage
    # saga ika will not show in ika list
    # but you can still get it by url
    saga = db.Column(db.Boolean, default=False)
    # ika text less than 10000
    text = db.Column(db.Text(10000), nullable=False)


def get_ika_number(ika_id):
    '''
    get the ika number under spec ika
    return int
    '''
    # under root
    if ika_id is 0:
        return Ika.query.filter_by(saga=False).count()
    # under a ika or a topic
    return Ika.query.filter_by(forward_ika_id=ika_id).count()


def get_ika(ika_id):
    '''
    get the spec Ika by its id
    return a Ika
    '''
    return Ika.query.filter_by(ika_id=ika_id).first()


def get_reply(fatherid, num, offset):
    '''
    fatherid means the first ika
    get reply for spec ika
    [offset+1, offset+num+1]
    return a [Ika, ...]
    '''
    # if this is a Ika
    if fatherid > 0:
        # return father itself
        return [get_ika(fatherid)] + Ika.query.filter_by(forward_ika_id=fatherid).order_by(Ika.ika_id).limit(num).offset(offset).all()
    # return all for 0 -> timeline
    if fatherid is 0:
        return Ika.query.filter(Ika.forward_ika_id<=0).order_by(Ika.last_ika_id.desc()).limit(num).offset(offset).all()
    # elif a topic
    return Ika.query.filter_by(forward_ika_id=fatherid).order_by(Ika.last_ika_id.desc()).limit(num).offset(offset).all()


def new_ika(forward_ika, user_id, name, title, image_url, text):
    '''
    post a new ika
    return ika_id
    '''
    # check if there is a forward_ika or topic
    # reply to a ika
    forward_ika = int(forward_ika)
    if forward_ika > 0:
        f_ika = Ika.query.filter_by(ika_id=forward_ika).first()
    # a new ika under a topic
    elif forward_ika < 0:
        f_ika = Ika_topic.query.filter_by(topic_id=forward_ika*-1).first()
    # no ika under 0. 0 means timeline
    else:
        return None
    # if f_ika don't exist
    if not f_ika:
        return None
    # resolve None
    if not name:
        name = '名前'
    # create ika
    ika = Ika(
        forward_ika_id=forward_ika,
        user_id=user_id,
        name=name,
        title=title,
        image_url=image_url,
        text=text
    )
    # must commit once to get the AI id
    db.session.add(ika)
    db.session.commit()
    # resolve with last reply id
    f_ika.last_ika_id = ika.ika_id
    ika.last_ika_id = ika.ika_id
    db.session.commit()
    return ika.ika_id


def get_topic(shortcut):
    '''get topic by shortcut'''
    return Ika_topic.query.filter_by(shortcut=shortcut).first_or_404()


def get_topics():
    '''get all topics'''
    return Ika_topic.query.order_by(Ika_topic.topic_id).all()
