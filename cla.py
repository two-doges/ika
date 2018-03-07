class Ika():
    '''one comment that includes:[Ika_id, poster, forward_Ika_id]'''
    def __init__(self, ika_id, forward_ika, post_time, poster_id, poster_name='NaMe', comment="hello" ,number = None):
        '''
        Ika_id is a unique id for every Ika.
        forward is the Ika id that this Ika link to
        poster id is the id belongs to poster
        name and email can be null and will set to 'NaMe' and 'Null'
        comment means content
        number means the number of ika
        '''
        self.ika_id = ika_id
        self.forward_ika = forward_ika
        self.post_time = post_time
        self.poster_id = poster_id
        self.poster_name = poster_name
        self.comment = comment
        self.number = None
