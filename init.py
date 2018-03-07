'''
init the database,you should run it first .Don't run it twice.
'''

import pymysql
import sqlquery


def initDatabase():
    conn = sqlquery.linkdata()
    cur = conn.cursor()
    cur.execute('''create table ikas
    (ikaid INT UNSIGNED AUTO_INCREMENT,
    forward int unsigned,
    time varchar(14),
    postid  bigint unsigned,
    name varchar(12),
    comment varchar(1012),
    primary key(ikaid))
    ENGINE=InnoDB DEFAULT charset=utf8;''')
    conn.close()


if __name__ == '__main__':
    initDatabase()
