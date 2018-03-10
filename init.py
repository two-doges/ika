'''
init the database,you should run it first .Don't run it twice.
'''
from endpoint import db
from endpoint import Ika_topic as t


db.create_all()
timeline = t(topic_title='时间线', shortcut='t')
main = t(topic_title='综合版', shortcut='m')
ika = t(topic_title='Ika 研究院', shortcut='i')
db.session.add_all([timeline, main, ika])
db.session.commit()
timeline.topic_id = 0
db.session.commit()
