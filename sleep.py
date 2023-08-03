from api import *;
from lib import *;
from auth import *;


def sleep(args, groupid, qqid):
    set_group_ban(qqid, groupid, 8*3600);
    return ""



def sleep_v2(args, groupid, qqid):
    if len(args) == 1: 
        set_group_ban(qqid, groupid, 8*3600);
    else:
        for qq in args[1:]:
            aimqqid = read_qqid(args[1]);
            if(get_authlevel(qqid, groupid)<5):
                return "权限不足，请重试"
            elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
                return "权限不足，请重试"
            set_group_ban(aimqqid, groupid, 8*3600);
    return ""
