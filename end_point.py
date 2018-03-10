'''the Api for backend'''
from rando import getno
from sqlquery import query_by_id
from sqlquery import query_more
from sqlquery import ins_ika
from sqlquery import get_total


def get_ika_number():
    '''
    get the ika number under root
    return int
    '''
    return get_total()


def get_ika(ika_id):
    '''
    get the spec Ika by its id
    return a Ika
    '''
    return query_by_id(ika_id)


def get_reply(fatherid, num_begin, num_end):
    '''
    fatherid means the first ika
    get reply for spec ika
    [num_begin, num_end)
    num_begin > 0
    return a [Ika, ...]
    '''
    return query_more(fatherid, num_begin, num_end)


def new_ika(forward_ika, poster_id, poster_name, comment):
    '''
    post a new ika
    return None
    '''
    ins_ika(forward_ika, poster_id, poster_name, comment)


def new_poster():
    '''
    return a unique id for each user
    return int
    '''
    return getno()
