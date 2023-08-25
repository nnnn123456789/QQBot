

import re;
import uuid
import base64
import codecs
import time

from mail import send_mail
from database import execute,db
from lib import read_qqid

bnu_list = [850472078, 1056925222, 195148269, 777013031, 638385816, 711242461, 554567155]


def is_bnugroup(groupid):
    global bnu_list
    if groupid in bnu_list:
        return True
    else:
        return False



def is_bnu_studentid(id_str):
    pattern = "20[1-2][0-9][1-3][1-6][0-9][0-9][0-9][0-9][0-9][0-9]"
    searchobj = re.search(pattern, id_str);
    if searchobj:
        return True;
    else:
        return False;



def gen_verify_code():
    return codecs.encode(codecs.decode(''.join(str(uuid.uuid4()).split('-')), 'hex'), 'base64').decode().strip()


def request_code(args, groupid, qqid):
    if not len(args) == 2:
        return "参数错误, 请输入学号"
    id_str = args[1];
    if not is_bnu_studentid(id_str):
        return "学号校验失败，请重试"
    
    now_time = time.time();
    n = execute('SELECT * FROM verify_code WHERE req_qqid = %d and time > %d' % (qqid, now_time - 10*60))
    if(n >= 3):
        return "近期请求过多，请稍后重试"
    
    code = gen_verify_code()
    execute("INSERT INTO `verify_code`(`code`, `stuid`, `time`, `req_qqid`, `used`, `abolish`)  VALUES ('%s', %d, %d, %d, 0,0)" % (code, int(id_str), now_time, qqid))
    db.commit()

    email_title = "您的BNU验证码是：%s" % code 
    email_receiver = "%s@mail.bnu.edu.cn" % id_str
    email_content = "%s, 验证码有效期60分钟\n可使用\"#reg %s\"验证您的BNU身份" % (email_title, code)

    send_mail(email_receiver, email_title, email_content)
    return "已向%d提供的BNU邮箱发送验证码，如收到，可使用\"#reg xxx\"认证群内BNU身份. 若查询不到邮件，可检查您的邮箱垃圾箱或再次请求。若担忧隐私泄露，可撤回学号消息，不影响认证功能" % qqid


def register_BNU(args, groupid, qqid):
    if not len(args) == 2:
        return "参数错误"
    
    code = args[1]
    now_time = time.time();
    sql_str = 'SELECT * FROM verify_code WHERE `code` = "%s" and `time` > %d and `used` = 0' % (code, now_time - 3600)
    print(sql_str)
    n = execute(sql_str)
    if n == 0 :
        return "%d的验证码校验失败，请核对后重新输入" % qqid 
    if n > 1 :
        return "内部错误"
    n = execute('UPDATE `verify_code` SET `used` = %d WHERE code = "%s"' % (qqid, code))
    db.commit()
    return "%d的BNU身份已验证成功" % qqid


def verify_BNU(args, groupid, qqid):
    if not len(args) == 2:
        return "参数错误"
    aimqqid = read_qqid(args[1]);
    n = execute('SELECT * FROM verify_code WHERE `used` = %d AND `abolish`=0' % (aimqqid,))
    if n > 0 :
        return "%d的BNU身份已确认" % aimqqid
    else :
        return "%d的BNU身份未确认" % aimqqid



def remove_BNU(args, groupid, qqid):
    prompt = ""
    now_time = time.time();
    if len(args) == 1: 
        return "请求参数错误"
    else:
        for qq in args[1:]:
            try:
                aimqqid = read_qqid(qq);
                execute('UPDATE `verify_code` SET `abolish` = %d WHERE `used` = %d AND `abolish` = 0' % (qqid, aimqqid))
                prompt += ("%d的BNU身份已注销\n" % aimqqid)
            except BaseException as ex:
                print(ex)
                prompt += "执行错误\n"
    db.commit();
    return prompt[:-1]


def add_BNU(args, groupid, qqid):
    prompt = ""
    now_time = time.time();
    if len(args) == 1: 
        return "请求参数错误"
    else:
        for qq in args[1:]:
            try:
                aimqqid = read_qqid(qq);
                execute("INSERT INTO `verify_code`(`code`, `stuid`, `time`, `req_qqid`, `used`, `abolish`)  VALUES ('%d', 0, %d, %d, %d, 0)" % (qqid, now_time, qqid, aimqqid ))
                prompt += ("%d的BNU身份已添加\n" % aimqqid)
            except BaseException as ex:
                print(ex)
                prompt += "执行错误\n"
    db.commit();
    return prompt[:-1]

    