from database import *;
import time;
from api import *;
from jrrp import *;
from bnu import is_bnugroup;

def get_random_bonus(qqid, groupid, actioncount):
    return (4 + get_jrrp(qqid))//5;


def random_bonus(qqid, groupid):
    if not is_bnugroup(groupid):
        return ""
    allow_fun = get_var(groupid, "allow_fun", "True")
    if allow_fun == "False":
        return ""
    now_time = time.time();
    s = str(now_time);
    dice = hash(s) % 20;
    if 0 == dice:
        today = int((now_time+8*3600)/86400);
        n = execute('SELECT * FROM random_bonus where qqid = %d and groupid = %d and date = %d' % (qqid, groupid, today));
        if(n>=5):
            return;
        else:
            bonus = get_random_bonus(qqid, groupid,n);
            execute('INSERT INTO random_bonus (qqid, groupid, date, time, value) VALUES (%d, %d, %d, %d, %d)' % (qqid, groupid, today, now_time, bonus));
            add_points(qqid, groupid, bonus);
            msg = "[CQ:at,qq=%d]获得发言积分%d分" % (qqid, bonus);
            send_group_message(groupid, msg)
    else:
        pass;
       