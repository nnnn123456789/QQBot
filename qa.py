from database import *;
import time;

def count_location():
    n = execute("SELECT * FROM qa_location");
    return n;


def add_location(name, text):
    index = count_location() + 1;
    execute("INSERT INTO qa_location(id, name, text) VALUES ( %d, '%s', '%s')" % (index, name, text));
    execute("INSERT INTO qa_jump(srcid, aimid, keyword, prompt) VALUES (%d, %d, '%s', '%s')" % (index, 0, "end", "结束对话"));
    execute("INSERT INTO qa_jump(srcid, aimid, keyword, prompt) VALUES (%d, %d, '%s', '%s')" % (index, index, "repeat", "复读该条消息"));
    db.commit();
    return index;


def add_jump(srcid, aimid, keyword, prompt):
    n = execute("SELECT * from qa_jump where srcid = %d and aimid = %d" % (srcid, aimid));
    if(n > 0):
        return False
    execute("INSERT INTO qa_jump(srcid, aimid, keyword, prompt) VALUES (%d, %d, '%s', '%s')" % (srcid, aimid, keyword, prompt));
    db.commit();
    return True


def locate_msg(locationid):
    n = execute("SELECT text FROM qa_location where id = %d" % locationid);
    if 0 == locationid:
        return "您的对话尚未开始或已经结束，如需开始会话请回复\"开始\""
    if(1 != n):
        return "找不到该位置，请联系管理员"
    msg = cursor.fetchone()[0] + '\n\n';
    n = execute("SELECT keyword, prompt FROM qa_jump where srcid = %d" % locationid);
    if(0 == n):
        return "找不到跳转选项，请联系管理员"
    l = cursor.fetchall();
    ll = [ "回复: \"" + i[0] + "\" : " + i[1] for i in l];
    return msg + "\n".join(ll);

    
def get_current(qqid):
    now_time = time.time();
    n = execute("SELECT aim FROM qa_log where qqid = %d and time > %d ORDER BY time DESC" % (qqid, now_time - 600));
    if 0 == n:
        return 1;
    else:
        return cursor.fetchone()[0];


def get_message(current, msg):
    if 0 == current:
        if msg == "开始":
            return (1,locate_msg(1));
        else:
            return (0,locate_msg(0));
    else:
        n = execute("SELECT aimid, keyword FROM qa_jump where srcid = %d" % current);
    jumplist = cursor.fetchall();
    #print(jumplist);
    aimid = -1;
    for i in jumplist:
        if msg == i[1]:
            aimid = i[0];
    if aimid == -1:
        return (current, "无法识别你的消息, 回复\"repeat\"可重发上一条消息");
    return (aimid, locate_msg(aimid));


def QA(args, groupid, qqid):
    if len(args) != 2:
        return "请求参数错误"
    current_location = get_current(qqid)
    aimloc, retmsg = get_message(current_location, args[1]);
    #print((aimloc, retmsg))
    execute("INSERT INTO qa_log(time, qqid, current, message, aim) VALUES (%d, %d, %d, '%s', %d)" % (time.time(), qqid, current_location, args[1], aimloc));
    db.commit()
    return "[CQ:at,qq=%d]\n%s" % (qqid, retmsg) 
    

def add_contact(name, telnum):
     number = add_location(name, "北师大" + name + ("电话: %d"%telnum))
     add_jump(2, number, name, name + "电话")





        