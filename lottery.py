from database import *;
from api import *;
import time
import random;

def get_dice(all_rewards):
    #print(all_rewards);
    now_time = time.time();
    start = 0;
    probs = [];
    for i in all_rewards:
        start = start + i[3]; 
        probs.append([start, i]);
    dice = random.randint(1,start+1);
    for i in probs:
        if dice < i[0]:
            #print (i[1])
            return (i[1]);
                
                
                
def lottery(args, groupid, qqid):
    now_time = time.time();
    lottery_limit_time_shijian = 24; #hours
    lottery_limit_time_cishu = 1;
    lottery_limit_time_lianchou = 5;

    n = execute('SELECT * FROM lottery_history WHERE qqid = %d and groupid = %d and time > %d' % (qqid, groupid, now_time - lottery_limit_time_shijian*3600))
    
    lottery_time = 1
    if(len(args) == 2):
        lottery_time = int(args[1]);
    if(lottery_time>lottery_limit_time_lianchou):
        lottery_time=lottery_limit_time_lianchou;
    if(lottery_time<1):
        lottery_time=1;
    if(n >= lottery_limit_time_cishu):
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '%s')" % (now_time, qqid, groupid, "刷屏警告"))
        db.commit()
        set_group_ban(qqid, groupid, 10 * (2 ** (n))); 
        #send_private_message(qqid, "您在过去8小时中参与抽奖%d次，已触发刷屏警告"  % n);
        return "请不要刷屏, 当前抽奖限制为：每%d小时只能抽奖%d次, 最多允许%d连抽" %(lottery_limit_time_shijian, lottery_limit_time_cishu, lottery_limit_time_lianchou)
    if(n + lottery_time >= 3):
        #lottery_time = 3 - n;
        pass
    now_points = get_points(qqid, groupid);
    if(now_points < 10):
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '%s')" % (now_time, qqid, groupid, "积分不足"))
        db.commit()        
        return "您的积分不足"
    if(now_points < 10 * lottery_time):
        lottery_time = now_points//10
        
    
    n = execute('SELECT `name`, `type`, `value`, `probab` FROM `lottery_pool` WHERE `groupid` = %d' % (groupid))
    
    #today = date.date();
    if(n == 0):
        return "奖品没有库存了"
    all_rewards = list(cursor.fetchall());
    add_points(qqid, groupid, -(10*lottery_time))
    
    #print(all_rewards)
    all_rewards.append(["none", "message", "您没有中奖", 10000]);

    print("all_rewards", all_rewards);
    results = [];
    print("抽奖次数: %d\n"  % lottery_time)

    pass;  
    for lot_i in range(lottery_time):
        results.append(get_dice(all_rewards));
        
    for result in results:
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '%s')" % (now_time, qqid, groupid, result[0]))
    db.commit()
    ret_msg = "[CQ:at,qq=%d]您中得的奖品是：" % (qqid) ;
    ban_time = 0;
    print(results)
    for result in results:
        if(result[1] == "points"):
            add_points(qqid, groupid, int(result[2]));
            #send_private_message(qqid, "您中得的奖品是："   +  result[0], group_id = groupid);
            ret_msg = ret_msg  +  result[0] + ",";
        elif(result[1] == "ban"):
            ban_time = ban_time + int(result[2])
            #send_private_message(qqid, "您中得的奖品是："   +  result[0], group_id = groupid);
            ret_msg = ret_msg  +  result[0] + ",";
        else:
            #send_private_message(qqid, "您中得的奖品是："   +  result[2], group_id = groupid);
            ret_msg = ret_msg  +  result[2] + ",";
    ret_msg = ret_msg[:-1]
    if (ban_time > 0):
        set_group_ban(qqid, groupid, ban_time);   
    return ret_msg;
    #return "[CQ:at,qq=%d]抽奖成功，请查看私聊消息" % (qqid);


def roshambo(args, groupid, qqid):
    now_time = time.time();
    n = execute('SELECT * FROM lottery_history WHERE qqid = %d and groupid = %d and time > %d' % (qqid, groupid, now_time - 8*3600))
    if(n >= 3):
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '%s')" % (now_time, qqid, groupid, "刷屏警告"))
        db.commit()
        set_group_ban(qqid, groupid, 10 * (2 ** n)); 
        return "请不要刷屏"
    now_points = get_points(qqid, groupid);
    if(now_points < 10):
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '%s')" % (now_time, qqid, groupid, "积分不足"))
        db.commit()        
        return "您的积分不足"
    add_points(qqid, groupid, -10)

    if(len(args)!= 2):
        return "参数错误"
    
    stone = ["石头", "stone", "rock", "锤子", "石", "锤", "拳头", "拳", "chuizi", "chui", "shi", "shitou", "quantou", "quan", "ling", "riot", "0", "零", "zero", "o", "O", "〇", "Ｏ", "０"]
    scissors  = ["剪刀", "scissors" , "剪", "剪子", "jiandao", "jian", "jianzi", "2", "二", "er", "two", "v", "V", "victory", "胜", "胜利", "sheng", "shengli", "Ｖ", "ｖ", "２"]
    paper = ["布", "paper", "cloth", "纸", "包", "包袱", "bu", "zhi", "bao", "baofu", "5", "五", "wu", "five", "shou", "hand", "手", "５"]
    user = 0; s = args[1];
    if s in stone:
        user = 1;
    elif s in scissors:
        user = 2;
    elif s in paper:
        user = 3
    else:
        return "[CQ:at,qq=%d]你出的东西我不认识！" % (qqid);
    dice = hash(str(time.time()) + s + str(qqid)) % 3 + 1;
    ans_pool = [[], stone, scissors, paper];
    ret = "我出" + ans_pool[dice][0];
    if user == dice:
        ret = ret + "，打平！"
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '猜拳平局')" % (now_time, qqid, groupid))
    elif (user == 1 and dice == 2) or (user == 2 and dice == 3) or (user == 3 and dice == 1):
        ret = ret + "，你赢了！"
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '猜拳获胜')" % (now_time, qqid, groupid))
        add_points(qqid, groupid, 15)
    else:
        ret = ret + "，你输了！"
        execute("INSERT INTO lottery_history (time, qqid, groupid, name) VALUES (%d, %d, %d, '猜拳输了')" % (now_time, qqid, groupid))
    db.commit();
    return ("[CQ:at,qq=%d]" % (qqid)) + ret;
