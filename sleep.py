from api import *;
from lib import *;
from auth import *;


def sleep(args, groupid, qqid):
    set_group_ban(qqid, groupid, 8*3600);
    return ""



def sleep_v2(args, groupid, qqid):
    if not len(args) <= 2:
        return "请求参数错误"
    if len(args) == 1: 
        aimqqid = qqid
    else:
        aimqqid = read_qqid(args[1]);
    if aimqqid == qqid:
        pass;
    elif(get_authlevel(qqid, groupid)<5):
        return "权限不足，请重试"
    elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
        return "权限不足，请重试"
    set_group_ban(aimqqid, groupid, 8*3600);
    return ""
