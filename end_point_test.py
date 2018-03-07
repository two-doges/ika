'''test mod for ika'''
from rando import getno


class Ika():
    '''one comment that includes:[Ika_id, poster, forward_Ika_id]'''
    def __init__(self, ika_id, forward_ika, post_time, poster_id, poster_name='NaMe', comment="hello"):
        '''
        Ika_id is a unique id for every Ika.
        forward is the Ika id that this Ika link to
        poster id is the id belongs to poster
        name and email can be null and will set to 'NaMe' and 'Null'
        comment means content
        '''
        self.ika_id = ika_id
        self.forward_ika = forward_ika
        self.post_time = post_time
        self.poster_id = poster_id
        self.poster_name = poster_name
        self.comment = comment


def ika_gen(ika_id, forward_ika):
    '''gen Ika'''
    return Ika(ika_id, forward_ika, '===', 111, comment='Hello')


def get_ika(ika_id):
    '''
    get the spec Ika by its id
    return a Ika
    '''
    return ika_id(ika_id, 0)


def get_reply(fatherid, num_begin, num_end):
    '''
    fatherid means the first ika
    get reply for spec ika
    [num_begin, num_end)
    num_begin > 0
    return a [Ika, ...]
    '''
    if num_end > 300:
        if num_begin >= 300:
            return []
        num_end = 300
    return [ika_gen(fatherid+i, fatherid) for i in range(num_begin, num_end)]


def new_ika(forward_ika, poster_id, poster_name, comment):
    '''
    post a new ika
    return new ika id
    '''
    print(forward_ika, poster_id, poster_name, comment)
    return 0


def new_poster():
    '''
    return a unique id for each user
    return int
    '''
    return getno()
