class Ika():
    '''one comment that includes:[Ika_id, poster, forward_Ika_id]'''
    def __init__(self, ika_id, forward_ika, post_time, poster_id, poster_name='NaMe'):
        '''
        Ika_id is a unique id for every Ika.
        ika_type can be ['post', 'reply']
        forward is the Ika id that this Ika link to
        poster id is the id belongs to poster
        name and email can be null and will set to 'NaMe' and 'Null'
        '''
        pass


def get_ika(ika_id):
    '''
    get the spec Ika by its id
    return a Ika
    '''
    pass


def get_reply(ika_id, num_begin, num_end):
    '''
    get reply for spec ika
    [num_begin, num_end)
    return a [Ika, ...]
    '''
    pass


def new_ika(ika_type, forward_ika, poster_id, poster_name):
    '''
    post a new ika
    return None
    '''
    pass


def new_poster():
    '''
    return a unique id for each user
    return int
    '''
    pass
