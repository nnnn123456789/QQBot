from api import *;
from lib import *;
from auth import *;


def sleep(args, groupid, qqid):
    set_group_ban(qqid, groupid, 8*3600);
    return ""



def sleep_v2(args, groupid, qqid):
    prompt = ""
    if len(args) == 1: 
        set_group_ban(qqid, groupid, 8*3600);
        prompt += ("%d已进入睡眠\n" % qqid)
    else:
        for qq in args[1:]:
            aimqqid = read_qqid(qq);
            if(get_authlevel(qqid, groupid)<5):
                prompt += ("禁言%d权限不足，请重试\n" % qqid)
            elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
                prompt += ("禁言%d权限不足，请重试\n" % qqid)
            else:
                set_group_ban(aimqqid, groupid, 8*3600);
                prompt += ("%d已进入睡眠\n" % aimqqid)
    return prompt[:-1]
