from database import *;
from api import *;
import time
from auth import *;
from sign import *;

#-1 cannot find
#-2 兑奖错误
#0 success 
#positive > 10000 means has already used.
def exec_ticket(qqid, key):
    n = execute('SELECT * FROM ticket WHERE id = \"%s\"' % key)
    if (0 == n):
        return -1;
    (id, groupid,type,value,name,use) = list(cursor.fetchall())[0];
    print((groupid,type,value,name,use))
    if (int(use) != 0):
        return int(use);
    
    if (type == "points"):
        add_points(qqid, groupid, int(value));
        #send_private_message(qqid, "您已兑得: " + name , group_id = groupid);
        execute('UPDATE ticket SET `use` = %d WHERE id = \"%s\"' % (qqid, key))
        return 0;
    if (type == "msg"):
        #send_private_message(qqid, "您已兑得: " + value, group_id = groupid);
        execute('UPDATE ticket SET `use` = %d WHERE id = \"%s\"' % (qqid, key))
        return 0;
    if (type == "help"):
        #send_private_message(qqid, "您的奖品" + name + "兑奖通知已经发送给兑奖负责人，请联系QQ" + value , group_id = groupid);
        #send_private_message(int(value), "%d已成功兑取%s奖品， 请注意发奖" % (qqid, name) , group_id = groupid);
        execute('UPDATE ticket SET `use` = %d WHERE id = \"%s\"' % (qqid, key))
        return 0;
    return -1;
        
        
def ticket(args, groupid, qqid):
    if(len(args)!= 2):
        return "参数错误"
    key = args[1];
    ret = exec_ticket(qqid, key);
    if (ret == 0):
        return "[CQ:at,qq=%d]已成功兑换" % qqid
        
    if (ret == -1):
        return "[CQ:at,qq=%d]找不到该奖券" % qqid
    
    if (ret == -2):
        return "[CQ:at,qq=%d]兑换错误[CQ:at,qq=2234748103]" % qqid   
    
    if (ret > 10000):
        return "[CQ:at,qq=%d]该奖券已被%d兑走" % (qqid, ret);
    
    return "未知兑换错误"   
    

def mall(args, groupid, qqid):
    if(len(args)==1):
        return "本群积分兑换列表请询问管理员";
        #https://yuanzm.com/bot/mall?groupid=%d
    #return "参数错误"
        
    key = args[1];
    
    if(key == "添加"):
        if(len(args) != 5):
            return "[CQ:at,qq=%d]参数错误，请使用\"添加 物品名称 消耗积分 物品个数\"来添加物品。" % qqid;
        (name, cost, bal) = args[2:];
        bal = int(bal);
        cost = int(cost);
        if cost <= 0:
            return "价格必须为正"
        n = execute('SELECT * FROM `mall` WHERE `name` = \'%s\' and `groupid` = %d' % (name, groupid));
        if n > 0:
            return "商品名称冲突，请考虑添加后缀"
        if (bal == 0) or (bal <= -2):
            return "[CQ:at,qq=%d]物品个数有误" % (qqid); 
        my_auth = get_authlevel(qqid, groupid);
        if my_auth < 7:
            return "[CQ:at,qq=%d]权限不足，您无法发行商城商品，请联系管理员代发" % (qqid); 
        SQL_text = 'INSERT INTO `mall`(`name`, `balance`, `groupid`, `owner`, `value`, `cost`) VALUES ("%s",%d,%d,%d,"%s",%d)' % (name, bal, groupid, qqid, name, cost);
        n = execute(SQL_text);
        db.commit()
        return "[CQ:at,qq=%d]添加成功" % (qqid);
    if(key == "兑换"):
        if(len(args) != 3):
            return "[CQ:at,qq=%d]参数错误，请使用\"兑换 物品名称\"来兑换物品。" % (qqid);
        SQL_text = 'SELECT `balance`,`owner`,`value`,`cost` FROM `mall` WHERE `name`=\'%s\' and `groupid` = %d' % (args[2], groupid)

        n = execute('SELECT `balance`,`owner`,`value`,`cost` FROM `mall` WHERE `name`=\'%s\' and `groupid` = %d' % (args[2], groupid));
        if (n == 0):
            return "[CQ:at,qq=%d]找不到该物品。" % (qqid);
        (balance, owner, value, cost) = list(cursor.fetchall())[0];
        if (balance == 0):
            return "[CQ:at,qq=%d]该奖券已被兑完" % (qqid);
        now_points = get_points(qqid, groupid);
        if(now_points < cost):       
            return "您的积分不足"
        
        next_balance = balance - 1;
        if (balance == -1):
            next_balance = -1;
        if (owner == 0):
            # msg
            add_points(qqid, groupid, -cost);
            execute('UPDATE `mall` SET `balance` = %d WHERE `name`=\'%s\' and `groupid` = %d' % (next_balance, args[2], groupid));
            db.commit()
            return "[CQ:at,qq=%d]您已兑得：%s" % (qqid, value);
        elif (owner == -1):
            # ban
            add_points(qqid, groupid, -cost);
            execute('UPDATE `mall` SET `balance` = %d WHERE `name`=\'%s\' and `groupid` = %d' % (next_balance, args[2], groupid));
            db.commit()
            set_group_ban(qqid, groupid, int(value)); 
            return "[CQ:at,qq=%d]您已兑得：%s" % (qqid, args[2]);
        else:
            try:
                transfer_points(groupid, qqid, owner, cost, True)
            except:
                return "转账时出现错误"
            execute('UPDATE `mall` SET `balance` = %d WHERE `name`=\'%s\' and `groupid` = %d' % (next_balance, args[2], groupid));
            db.commit()
            return "[CQ:at,qq=%d]您已兑得：%s, 积分已交付, 请找[CQ:at,qq=%d]兑奖吧" % (qqid, args[2], owner);
        
        name = args[2];
        ##TODO
        return ""
    if(key == "添加自动兑换"):
        if(get_authlevel(qqid, groupid)<7):
            return "[CQ:at,qq=%d]权限不足"    
        if(not len(args) in [4,5]):
            return "[CQ:at,qq=%d]参数错误"
        if(not args in ["禁言", "消息"]):
            return "[CQ:at,qq=%d]参数错误"            
        name = args[2];
        ##TODO
        return ""        
    if(key == "删除"):
        if(get_authlevel(qqid, groupid)<10):
            return "[CQ:at,qq=%d]权限不足"    
        if(len(args) < 3):
            return "[CQ:at,qq=%d]参数错误，请使用\"删除 物品名称\"来删除物品。" % (qqid);
        names = args[2:];
        
        names = [(' `name` = "%s" ' % i ) for i in names]
        print(names)
        sql_suffix = ' OR '.join(names);
        sql_text = 'DELETE FROM `mall` WHERE `groupid` = %d AND (%s)' % (groupid, sql_suffix);
        execute(sql_text)
        print (sql_text)
        db.commit()

        return "[CQ:at,qq=%d]删除成功"  % qqid;
        
    
    return "未知兑换命令"   

        
        