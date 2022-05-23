import date
from lib import *;
from auth import *;
from database import *;
from dictsearch import get_random_dict;


def gen_jrrp(qqid):
    s = str(date.date()) + str(qqid)
    ret = 1 + hash(s)%100;
    #print(ret);
    return ret;



def get_jrrp(qqid):
    today = date.date()
    n = cursor.execute('SELECT val FROM jrrp WHERE qqid = %d and date = %d' % (qqid, today))
    ret = 0;
    if(n == 0):
        ret = gen_jrrp(qqid);
        execute('INSERT INTO jrrp(qqid, date, val) VALUES(%d, %d, %d)' % (qqid, today, ret))
        db.commit()
    else:
        ret = cursor.fetchone()[0]
    print(ret);
    return ret


# def jrrp(args, groupid, qqid):
#     if not len(args) == 1: 
#         return ""
#     print(get_jrrp(qqid))
#     return "[CQ:at,qq=%d]的人品值是：%d" %(qqid, get_jrrp(qqid))



def jrrp(args, groupid, qqid):
    rand_dict = ""
    if(len(args) == 1):
        return "[CQ:at,qq=%d]的人品值是：%d" %(qqid, get_jrrp(qqid))
    elif(len(args) == 2):
        aimqqid = read_qqid(args[1]);
        if(get_authlevel(qqid, groupid)<5):
            return "权限不足，请重试"
        elif(get_authlevel(qqid, groupid)<get_authlevel(aimqqid, groupid)):
            return "权限不足，请重试"
        else:
            n = get_jrrp(aimqqid);
        return "%d的人品值是：%d" %(aimqqid, n);

