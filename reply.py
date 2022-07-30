import date
from lib import *;
from auth import *;
from database import *;

allow_group_list = [195148269, 711242461]

def reply_private(args, groupid, qqid):
    if groupid not in allow_group_list:
        return "该功能不对本群开放"
    if(len(args) != 3):
        return "参数错误"
    elif(len(args) == 3):
        aim_qqid = args[1]
        remsg = "%s向您发送了一条回复消息如下:\n%s" % (qqid, args[2])
        send_private_message(aim_qqid, remsg)
        return "回复成功"


def reply_temp(args, groupid, qqid):
    if groupid not in allow_group_list:
        return "该功能不对本群开放"
    if(len(args) != 4):
        return "参数错误"
    elif(len(args) == 4):
        aim_qqid = args[1]
        aim_groupid = args[2]
        remsg = "%s向您发送了一条回复消息如下:\n%s" % (qqid, args[3])
        send_private_message(qqid, remsg)
        send_private_message_by_group (aim_qqid, aim_groupid, remsg)
        return "回复行为未返回异常"