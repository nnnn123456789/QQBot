from auth import *;
from api import *;
from lib import *;

def ban(args, groupid, qqid):
    if not len(args) == 3:
        return "请求参数错误"
    aimqqid = read_qqid(args[1]);
    if aimqqid == qqid:
        pass;
    elif(get_authlevel(qqid, groupid)<5):
        return "权限不足，请重试"
    elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
        return "权限不足，请重试"
    set_group_ban(aimqqid, groupid, int(args[2]));
    return ""


def unban(args, groupid, qqid):
    if not len(args) == 2:
        return "请求参数错误"
    aimqqid = read_qqid(args[1]);
    if(get_authlevel(qqid, groupid)<5):
        return "权限不足，请重试"
    set_group_ban(aimqqid, groupid, 0);
    return ""


def kick(args, groupid, qqid):
    if not len(args) == 2:
        return "请求参数错误"
    aimqqid = read_qqid(args[1]);
    if aimqqid == qqid:
        pass;
    elif(get_authlevel(qqid, groupid)<7):
        return "权限不足，请重试"
    elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
        return "权限不足，请重试"
    set_group_kick(aimqqid, groupid);
    return ""


def callback(args, groupid, qqid):
    print(args);
    if not (len(args) == 2 or len(args) == 3):
        return "请求参数错误"
    replymsg = "";
    if "[CQ:reply," in args[1]:
        replymsg = args[1];
    elif "[CQ:reply," in args[2]:
        replymsg = args[2];
    else:
        return "未找到引用的消息，请重试"
    msgid = int(replymsg.split("[CQ:reply,id=")[1].split(']')[0]);
    aimqqid = get_msg_sender(msgid);
    if(qqid == aimqqid):
        pass;
    elif(get_authlevel(qqid, groupid)<5):
        return "权限不足，请重试"
    elif(get_authlevel(qqid, groupid)<=get_authlevel(aimqqid, groupid)):
        return "权限不足，请重试"
    delete_msg(msgid);
    #set_group_kick(aimqqid, groupid);
    return ""
    

def tell_groupid(args, groupid, qqid):
    return "%d" % groupid