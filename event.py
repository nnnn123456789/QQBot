from api import *

import requests
import json
import autoreply
import lib
import echo
import jrrp
import sign
import database
import sleep
import lottery
from database import *
from random_bonus import random_bonus as rand_bon
import time
import auth
import ban
import qa
import group_silent
import ticket
import quiz
import dictsearch
import reply
import bnu
from bnu import is_bnugroup, is_bnu_studentid



class Command:
    # exec as function handle(args, groupid, qqid)
    # auth_level as authority
    # cmd_level as integer,
    # 0 for basic, such as shutdown, restart
    # 1 for group-manager, such as T, ban
    # 2 for fun, such as lottery
    def __init__(self, handle, auth, level, name = "default_name"):
        self.execute = handle
        self.auth_level = auth
        self.cmd_level = level
        self.cmd_name = name

    def __call__(self, args, groupid, qqid):
        if self.cmd_level >= 1:
            allow_commands = database.get_var(groupid, "allow_commands", "True")
            if allow_commands == "False":
                return ""
        if self.cmd_level == 2:
            allow_fun = database.get_var(groupid, "allow_fun", "True")
            if allow_fun == "False":
                return ""
        if not (self.cmd_name == "default_name"):
            varname = "allow_%s" % self.cmd_name;
            local_allow_fun = database.get_var(groupid, varname , "True", False);
            if local_allow_fun == "False":
                return ""
        user_auth = auth.get_authlevel(qqid, groupid)
        if(user_auth < self.auth_level):
            return "权限不足, 请重试"

        try:
            ret = self.execute(args, groupid, qqid)
        except Exception as e:
            print(e)
            ret = "执行出现错误"
        return ret


group_ans_pool = {}
#global group_ans_pool2
#group_ans_pool2 = {}
group_ans_pool3 = {}


group_ans_pool2["#允许命令"] = Command(group_silent.commands_allow, 11, 0)
group_ans_pool2["#禁止命令"] = Command(group_silent.commands_disallow, 11, 0)

group_ans_pool2["#添加自动回复"] = Command(autoreply.add_auto_reply, 11, 1)
group_ans_pool2["#执行"] = Command(database.literal_execute, 12, 1)
group_ans_pool2["#禁言"] = Command(ban.ban, 1, 1)
group_ans_pool2["#踢"] = Command(ban.kick_v2, 1, 1)
group_ans_pool2["#解禁"] = Command(ban.unban, 5, 1)
group_ans_pool2["#t"] = Command(ban.kick_v2, 1, 1)
group_ans_pool2["#撤回"] = Command(ban.callback, 1, 1, "#撤回")
group_ans_pool2["#查群号"] = Command(ban.tell_groupid, 1, 1)

group_ans_pool2["#允许娱乐"] = Command(group_silent.fun_allow, 9, 1)
group_ans_pool2["#禁止娱乐"] = Command(group_silent.fun_disallow, 9, 1)

group_ans_pool2["#echo"] = Command(echo.echo, 5, 2)
group_ans_pool2["#jrrp"] = Command(jrrp.jrrp, 1, 2, "#jrrp")
group_ans_pool2["#签到"] = Command(sign.sign, 1, 2, "#签到")
group_ans_pool2["#积分查询"] = Command(sign.getpoints, 1, 2)
group_ans_pool2["#积分排名"] = Command(sign.getlist, 1, 2)
group_ans_pool2["#加分"] = Command(sign.add, 1, 2)
group_ans_pool2["#sleep"] = Command(sleep.sleep_v2, 1, 2, "#sleep")
group_ans_pool2["#sieep"] = Command(sleep.sleep_v2, 1, 2, "#sleep")
group_ans_pool2["#抽奖"] = Command(lottery.lottery, 1, 2, "#抽奖")
group_ans_pool2["#权限"] = Command(auth.showauth, 1, 2)
group_ans_pool2["#我出"] = Command(lottery.roshambo, 1, 2)
group_ans_pool2["#撤"] = Command(ban.callback, 1, 2, "#撤回")
group_ans_pool2["#qa"] = Command(qa.QA, 1, 2)
group_ans_pool2["#转账"] = Command(sign.transfer, 1, 2, "#转账")
group_ans_pool2["#转"] = Command(sign.transfer, 1, 2, "#转账")
group_ans_pool2["#transfer"] = Command(sign.transfer, 1, 2, "#转账")
#group_ans_pool2["#quiz"] = Command(quiz.quiz, 1, 2, "#quiz")



group_ans_pool2["#允许"] = Command(group_silent.local_allow, 10, 1)
group_ans_pool2["#禁止"] = Command(group_silent.local_disallow, 10, 1)

#group_ans_pool2["#兑换"] = Command(ticket.ticket, 1, 2, "#兑换")
group_ans_pool2["#兑"] = Command(ticket.ticket, 1, 2, "#兑换")
group_ans_pool2["#dict"] = Command(dictsearch.dict_search, 1, 1)
group_ans_pool2["#dictid"] = Command(dictsearch.dict_search_id, 1, 1)
group_ans_pool2["#word"] = Command(dictsearch.randword, 1, 1, "#背单词")
group_ans_pool2["#背单词"] = Command(dictsearch.randword, 1, 1, "#背单词")

group_ans_pool2["#mall"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#mali"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#mail"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#maii"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#ma1l"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#ma1i"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#ma11"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#mal1"] = Command(ticket.mall, 1, 2, "#积分商城")
group_ans_pool2["#mai1"] = Command(ticket.mall, 1, 2, "#积分商城")

group_ans_pool2["#回私"] = Command(reply.reply_private, 1, 1)
group_ans_pool2["#回临"] = Command(reply.reply_temp, 11, 1)

group_ans_pool2["#reg"] = Command(bnu.register_BNU, 1, 1)
group_ans_pool2["#verify"] = Command(bnu.verify_BNU, 1, 1)
group_ans_pool2["#code"] = Command(bnu.request_code, 1, 1)
group_ans_pool2["#+bnu"] = Command(bnu.add_BNU, 7, 1)
group_ans_pool2["#bnu+"] = Command(bnu.add_BNU, 7, 1)
group_ans_pool2["#-bnu"] = Command(bnu.remove_BNU, 7, 1)
group_ans_pool2["#bnu-"] = Command(bnu.remove_BNU, 7, 1)


def on_group_message(m):
    #return;
    rawmsg = m["raw_message"]
    execute("INSERT INTO group_msg_log (time, qqid, groupid, msg) VALUES (%d, %d, %d, '%s')" % (
        time.time(), m["user_id"], m["group_id"], lib.add_backslash(rawmsg)))
    print("原始文本： " + rawmsg)
    if(len(rawmsg) >= 15):
        rand_bon(m["user_id"], m["group_id"])
    autoans = autoreply.get_autoans(rawmsg, m["group_id"])

    if not autoans == "":
        send_group_message(m["group_id"],  autoans)
    if "[CQ:reply," in rawmsg:
        templist = rawmsg.split(' ')
        realblock = templist[1:] + templist[0:1]
        rawmsg = ' '.join(realblock)
    args = lib.div_args(rawmsg)
    # print(args[0])
    if len(args) == 0:
        return
    cmd = group_ans_pool2.get(args[0].lower())
    # print(cmd)
    if not cmd == None:
        ans = cmd(args, m["group_id"], m["user_id"])
        if not ans == "":
            send_group_message(m["group_id"], ans)
    pass



def on_private_message(m):
    send_private_message(m['user_id'], m['raw_message'])
    print(m)
    if 'group_id' in m['sender']:
        prompt = "收到来自%s(%d)经由群%d的临时消息， 内容如下： \n%s\n可使用\"#回临 qq号 群号 消息内容\"回复" % (m['sender']['nickname'], m["user_id"], m['sender']['group_id'], m["raw_message"])
    else:
        prompt = "收到来自%s(%d)的私聊消息， 内容如下： \n%s\n可使用\"#回私 qq号 消息内容\"回复" % (m['sender']['nickname'], m["user_id"], m["raw_message"])
    monitor_group_list = [195148269, 711242461]
    for i in monitor_group_list:
        send_group_message(i, prompt)
    pass
    send_private_message(2234748103, prompt);


def on_group_manager_change(m):
    pass





def on_group_users_add(m):
    #return;
    print("新人加群")

    sql_str = "INSERT INTO group_increase_log (time, sub_type, group_id, operator_id, user_id) VALUES (%d, '%s', %d, %d, %d)" % (
        int(time.time()), m["sub_type"], m["group_id"],  m["operator_id"],  m["user_id"])
    print(sql_str)
    execute(sql_str)
    bnu_wel_msg = "欢迎新同学，改个群名片，向大家介绍一下自己吧。名片格式为 入学年-院系专业-昵称，如" + '"22-法学-张三"' + "，注意【不要使用自己的真实姓名】。\n" + \
        "院系群号，培养方案，转专业，大学英语，师大地图等基本问题相关信息请在群文件中自取。\n" +  \
        "除了随录取通知书发放的学宿费缴费通知外，师大及各部院系不会以任何理由收取任何费用，所有交钱可以选老师/交钱可以选宿舍的都是谎言，谨防诈骗。\n" +  \
        "除了热情和求知以外，独立解决问题，自行搜索信息也是大学必备技能！\n" + \
        "有任何困难或者问题也可以私戳群里的师兄师姐。\n" + \
        "此消息为机器人自动生成，请勿回复。"
    allow_fun = get_var(m["group_id"], "allow_fun", "True")
    if allow_fun == "False":
        return;
    if is_bnugroup(m["group_id"]):
        #send_private_message(m["user_id"], bnu_wel_msg, group_id = m["group_id"]);
        #send_group_message(m["group_id"], ("[CQ:at,qq=%d]" % int(m["user_id"])) + bnu_wel_msg);
        #set_group_card(m["group_id"],m["user_id"], U"??-??-请修改群名片")
        pass
    else:
        pass
        #ret = send_group_message(m["group_id"], "欢迎新同学[CQ:at,qq=%d]，改个群名片，向大家介绍一下自己吧" % int(m["user_id"]))
    #set_group_ban(m["user_id"], m["group_id"], 5 * 60)
    print("欢迎成功")
    db.commit()


def on_group_users_delete(m):
    allow_fun = get_var(m["group_id"], "allow_fun", "True")
    if allow_fun == "False":
        return;
    if m["sub_type"] == "leave":
        ret = send_group_message(m["group_id"], "成员%d已退出该群" % int(m["user_id"]));
    elif m["sub_type"] == "kick":
        ret = send_group_message(m["group_id"], "成员%d已被管理员踢出" % int(m["user_id"]));
    #print(ret);
    print("人员离群")
    pass


def on_group_ban(m):
    pass


def on_group_document_upload(m):
    pass


def on_request_friend_add(m):
    pass


#申请或邀请
def on_request_group_invite(m):
    print(m)
    comment = m["comment"]
    groupid = m["group_id"]
    #flag = m["flag"]
    sub_type =  m["sub_type"]

    execute("INSERT INTO group_request_log (time, sub_types, group_id, user_id, comment) VALUES (%d, '%s', %d, %d, '%s' )" % (
        int(time.time()), sub_type, groupid,  m["user_id"], comment))
    
    db.commit()



    # if (is_bnu_studentid(comment) and is_bnugroup(groupid)):
    #     set_group_add_request(flag, sub_type, True);
    #     print("依照学号放人成功");
    #     return
    # if (sub_type == "invite" and is_bnugroup(groupid)):
    #     set_group_add_request(flag, sub_type, True);
    #     print("邀请放人成功");
    #     return
    #if ("答案：21新生" in comment and 1056925222 == groupid):
    #    set_group_add_request(flag, sub_type, True);
    #    print("21新生放人成功");
    #    return   
        
    pass


def on_group_message_recall(m):
    msg = ""
    if(m["user_id"] == m["operator_id"]):
        msg = "[CQ:at,qq=%ld]不许撤回，我看到啦！" % m["user_id"]
        return
    else:
        return
    ret = send_group_message(m["group_id"], msg)
    print(ret)
    pass


def on_private_message_recall(m):
    pass


def on_heartbeat(m):
    pass

