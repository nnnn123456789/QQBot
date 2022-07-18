from database import *;
from date import *;
from api import *;
from lib import *;
from jrrp import *;
from auth import *;

def get_signpoints(qqid, groupid, contdays):
	return 20 + 5 * min(15,contdays) + get_jrrp(qqid)//20;

def sign(args, groupid, qqid):
    n = cursor.execute('SELECT lastsign, contdays FROM sign WHERE qqid = %d and groupid = %d' % (qqid,groupid))
    today = date.date();
    if(n == 0):
        execute('INSERT INTO sign(qqid, groupid, lastsign, contdays) VALUES(%d, %d, %d, 1)' % (qqid, groupid, today))
        contdays = 1;
    else:
        lastsign, contdays = cursor.fetchone();
        if(lastsign == today-1):
            contdays = contdays+1;
        elif (lastsign == today):
            #send_private_message(qqid, "已经签到过了" , group_id = groupid);
            return "[CQ:at,qq=%d]已经签到过了" % qqid; 
        else:
            contdays = 1;
        execute('UPDATE sign SET lastsign=%d, contdays=%d WHERE qqid = %d AND groupid = %d' % (today, contdays, qqid, groupid));
    point = get_signpoints(qqid, groupid, contdays);
    add_points(qqid, groupid, point);  
    db.commit()                     #db.commit()
    #send_private_message(qqid, "签到成功，本次获得积分%d点" % point, group_id = groupid);
    return "[CQ:at,qq=%d]签到成功, 连续签到%d天, 本次获得积分%d点" % (qqid, contdays, point);



def getpoints(args, groupid, qqid):
    if(len(args) == 1):
        n = get_points(qqid, groupid);
        return "[CQ:at,qq=%d]当前积分为：%d" % (qqid, n);
    elif(len(args) == 2):
        aimqqid = read_qqid(args[1]);
        if(get_authlevel(qqid, groupid)<5):
            return "权限不足，请重试"
        elif(get_authlevel(qqid, groupid)<get_authlevel(aimqqid, groupid)):
            return "权限不足，请重试"
        else:
            n = get_points(aimqqid, groupid);
        return "%d的当前积分为：%d" % (aimqqid, n);


def getlist(args, groupid, qqid):
    return "群积分排名请询问管理员";
    db.commit()
    sql_text = 'SELECT * FROM (SELECT * FROM `points` WHERE `groupid`=%d ORDER BY `points` DESC) temp ORDER BY `points` DESC LIMIT 5' % groupid;
    n = execute(sql_text)
    result = cursor.fetchall();
    ranks = [("%10d: %5d" %(x[0], x[2])) for x in result];
    output = '\n'.join(ranks);
    return "群积分排名： \n%s" % output;


def add(args, groupid, qqid):
    role = get_group_member_role(groupid, qqid);
    if not len(args) == 3:
        return "请求参数错误"
    aimqqid = read_qqid(args[1]); 

    if(get_authlevel(qqid, groupid)<=10):
        if(aimqqid == qqid and int(args[2]) < 0):
            add_points(aimqqid, groupid, int(args[2]))
            return "执行成功，%d当前的积分为%d" % (aimqqid, get_points(aimqqid, groupid))
        else:
            return "权限不足，请重试"

    add_points(aimqqid, groupid, int(args[2]));
    return "执行成功，%d当前的积分为%d" % (aimqqid, get_points(aimqqid, groupid))


def tax_of_transfer(groupid, qqid1, qqid2, point):
    return int((point + 1)/2);
    if point == 1:
        return 1;
    if point < 10:
        return int(point/2)
    elif point < 85:
        return int(point/5)+3
    else:
        return 20
        


def transfer_points(groupid, qqid1, qqid2, point, taxfree = False):
    if (point == 0) :
        return 0
    fromqqid = qqid1 if point > 0 else qqid2
    aimqqid = qqid1 if point < 0 else qqid2
    abspoint = point if point > 0 else -point
    frompoint = get_points(fromqqid, groupid)
    if( frompoint < point):
        return -1
    add_points(fromqqid, groupid, -abspoint)
    tax = tax_of_transfer(groupid, fromqqid, aimqqid, abspoint);
    if taxfree:
        tax = 0;
    add_points(aimqqid, groupid, abspoint - tax)
    return tax


def transfer(args, groupid, qqid):
    if not len(args) == 3: 
        return "请求参数错误"
    try:
        aimqqid = read_qqid(args[1]);
        point = abs(int(args[2]));
    except:
        return "请求错误"
    ret = transfer_points(groupid, qqid, aimqqid, point)
    if (ret<0):
        return "余额不足，请重试"
    else:
        return "转账成功，税费%d" % ret;
    
    
    
    
