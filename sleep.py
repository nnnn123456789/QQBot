from api import *;


def sleep(args, groupid, qqid):
    set_group_ban(qqid, groupid, 8*3600);
    return ""
