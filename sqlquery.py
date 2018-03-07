import pymysql
import time
import config
from cla import Ika


def linkdata():
    conn = pymysql.connect(config.address, config.user, config.password, 'ikadata',charset='utf8')
    return conn


def query_by_id(id):
    id = int(id)
    conn = linkdata(name)
    cur = conn.cursor()
    cur.execute('select * from ikas where ikaid = "%d";' % (id))
    re = cur.fetchall()
    cnt = 1
    if not re:
        return None
    if re[0][1] == 0:
        cur.execute('select * from cnts where ikaid = "%d";' %(id))
        cc = cur.fetchall()
        cnt = int(cc[0][1])
    cur.close()
    conn.close()
    return Ika(*re[0], cnt)


'''
def add_ika(ik):
    conn = linkdata()
    cur = conn.cursor()
    sql = 'insert into ikas values(0,%s,%s,%s,%s,%s)' % (ik.forward_ika,
     ik.post_time, ik.poster_id, ik.poster_name, ik.comment)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
'''


def query_more(fa, be, en):
    fa = int(fa)
    be = int(be)
    en = int(en)
    maxsize = 100
    if(en<=be):
        return None
    en = min(be + maxsize + 1, en)
    conn = linkdata()
    cur = conn.cursor()
    ans = []
    if be == 1 and fa > 0:
        be += 1
        stri = 'select * from ikas where ikaid="%s"'%(fa)
        cur.execute(stri)
        re = cur.fetchall()
        ans.append(Ika(*re[0]))
    stri = 'select * from ikas where forward="%s"'%(fa)
    cur.execute(stri)
    re = cur.fetchall()
    if be > len(re) + 1:
        return ans
    cur.close()
    conn.close()
    no = 2
    ll = len(re)
    if fa == 0:
        no = 1
        reversed(re)
    #print("!!!!!"+str(fa))
    for i in range(be-no,min(ll,en-1)):
        ans.append(Ika(*re[i]))
    return ans


def ins_ika(fid, pid, pna, com):
    conn = linkdata()
    cur = conn.cursor()
    fid = int(fid)
    if fid < 0:
        return
    elif fid > 0:
        cur.execute('select * from cnts where ikaid = "%s"'%(fid))
        res = cur.fetchall()
        #print (fid)
        #print(res)
        if not res:
            return
    stri = 'insert into ikas values(0,%s,'+time.strftime("%Y%m%d%H%M%S", time.localtime())+',%s,%s,%s)'
    cur.execute(stri, (fid, int(pid), pna, com))
    conn.commit()
    cur.execute('select last_insert_id();')
    re = cur.fetchall()
    no = fid
    if no == 0:
        no = int(re[0][0])
        #print('?????')
        cur.execute('insert into cnts values("%s",1)'%(no))
        conn.commit()
    else:
        cur.execute('select * from cnts where ikaid = "%s" for update'%(no))
        nu = cur.fetchall()
        nu = int(nu[0][1])
        nu += 1
        cur.execute('update cnts set ikaid = "%s",number = "%s" where ikaid = "%s"'
        %(no, nu, no))
        conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    ins_ika(0,12,'bb','123')
    ins_ika(1,11,'aa','456')
    ins_ika(1,1,'sss','789')
    re = query_more(1,2,3)
    for i in re:
        ika_show(i)
