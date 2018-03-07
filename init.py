'''
init the database,you should run it first .Don't run it twice.
'''

import pymysql


def initDatabase():
    conn = pymysql.connect('localhost','root','123456','ikadata')
    cur = conn.cursor()
    cur.execute('''create table ikas
    (ikaid INT UNSIGNED AUTO_INCREMENT,
    forward int unsigned,
    time datetime,
    postid  bigint unsigned,
    name varchar(12),
    comment varchar(116),
    primary key(ikaid))
    ENGINE=InnoDB DEFAULT charset=utf8;''')
    conn.close()


if __name__ == '__main__':
    initDatabase()
