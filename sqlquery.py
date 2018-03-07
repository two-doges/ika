import pymysql
import time
from end_point import *


def query_by_id(id):
    id = int(id)
    conn = pymysql.connect('localhost','root','123456','ikadata')
    cur = conn.cursor()
    cur.execute('select * from ikas where ikaid = "%d";' % (id))
    re = cur.fetchall()
    cur.close()
    conn.close()
    return Ika(re[0][0], re[0][1], re[0][2], re[0][3], re[0][4], re[0][5])


def add_ika(ik):
    conn = pymysql.connect('localhost', 'root', '123456', 'ikadata')
    cur = conn.cursor()
    sql = 'insert into ikas values(0,"%s","%s","%s","%s","%s")' % (ik.forward_ika,
     ik.post_time, ik.poster_id, ik.poster_name, ik.comment)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


def query_more(fa, be, en):
    fa = int(fa)
    maxsize = 100
    if(en<=be):
        return None
    en = min(be + maxsize + 1, en)
    conn = pymysql.connect('localhost', 'root', '123456', 'ikadata')
    cur = conn.cursor()
    ans = []
    if be == 1:
        be += 1
        stri = 'select * from ikas where ikaid="%s"'%(fa)
        cur.execute(stri)
        re = cur.fetchall()
        ans.append(Ika(re[0][0], re[0][1], re[0][2], re[0][3], re[0][4], re[0][5]))
    stri = 'select * from ikas where forward="%s"'%(fa)
    cur.execute(stri)
    re = cur.fetchall()
    if be > len(re) + 1:
        return ans
    cur.close()
    conn.close()
    for i in range(be-2,min(len(re),en-1)):
        ans.append(Ika(re[i][0], re[i][1], re[i][2], re[i][3], re[i][4], re[i][5]))
    return ans


def ins_ika(fid, pid, pna, com):
    stri = 'insert into ikas values(0,"%s",cast(n\'%s\' as datetime),"%s","%s","%s")'
    conn = pymysql.connect('localhost', 'root', '123456', 'ikadata')
    print(stri%(fid,time.strftime("%Y-%m-%d %H:%M:%S.000",time.localtime()),pid,pna,com))
    cur = conn.cursor()
    cur.execute(stri, (fid, time.strftime("%Y-%m-%d %H:%M:%S.000", time.localtime()), pid, pna, com))
    print(stri%(fid, time.strftime("%Y-%m-%d %H:%M:%S.00", time.localtime()), pid, pna, com))
    conn.commit()
    cur.close()
    conn.close()


def ika_show(ik):
    print(str(ik.ika_id)+' '+str(ik.forward_ika)+' '+str(ik.post_time)+' '+str(ik.poster_id)+
    ' '+str(ik.poster_name)+' '+str(ik.comment))


if __name__ == '__main__':
    ins_ika(1,2,'hello','balaa')
