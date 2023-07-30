from database import *;
from api import *;
from lib import *;

#-2 (global block list)
#-1 (group block list)
#0 (common user)
#1 (named)
#2 (group white list)
#3 (global white list)
#4 (labeled  群主给头衔)
#5 (group junior manager)
#6 (global junior manager)
#7 (group manager)
#8 (group senior manager)
#9 (global senior namager)
#10 (bot manager)
#11 (group owner)
#12 (bot owner)


def get_global_authlevel(qqid):
    n = execute('SELECT level FROM user_level WHERE qqid = %d and groupid = 0' % (qqid))
    if(0 == n):  
        execute('INSERT INTO user_level (qqid, groupid, level) values (%d, 0, 0)' % (qqid))
        db.commit();
        return 0;
    else:
        return cursor.fetchone()[0];
        

def get_native_authlevel(qqid, groupid):
    role = get_group_member_role(groupid, qqid);
    if role == "owner":
        ret = 11;
    elif role == "admin":
        ret = 7;
    elif get_group_member_title(groupid, qqid) != "":
        ret = 4;
    elif get_group_member_card(groupid, qqid) != "":
        ret = 1;
    else:
        ret = 0;
    return ret;      

        
def get_defined_authlevel(qqid, groupid):
    n = execute('SELECT level FROM user_level WHERE qqid = %d and groupid = %d' % (qqid, groupid))
    if(0 == n):
        return 0;
    else:
        return cursor.fetchone()[0];

   
def get_local_authlevel(qqid, groupid):
    return max(get_defined_authlevel(qqid, groupid), get_native_authlevel(qqid, groupid))
        

def get_authlevel(qqid, groupid):
    gl = get_global_authlevel(qqid);
    lo = get_local_authlevel(qqid, groupid);
    #print((get_global_authlevel(qqid), get_defined_authlevel(qqid, groupid), get_native_authlevel(qqid, groupid)))
    if(gl == 0 or lo == 0):
        return gl + lo;
    elif(gl * lo < 0):
        return lo;
    else:
        return max(gl,lo);


def set_global_authlevel(qqid, level):
    n = execute('SELECT level FROM user_level WHERE qqid = %d and groupid = 0' % (qqid))
    if(0 == n):
        execute('INSERT INTO user_level (qqid, groupid, level) values (%d, 0, %d)' % (qqid, level))
    else:
        execute('UPDATE user_level SET level = %d WHERE qqid = %d and groupid = 0' % (level, qqid))
    db.commit();
    return n;
    

def set_local_authlevel(qqid, groupid, level):
    n = execute('SELECT level FROM user_level WHERE qqid = %d and groupid = %d' % (qqid, groupid))
    if(0 == n):
        execute('INSERT INTO user_level (qqid, groupid, level) values (%d, %d, %d)' % (qqid, groupid, level))
    else:
        execute('UPDATE user_level SET level = %d WHERE qqid = %d and groupid = %d' % (level, qqid, groupid))
    db.commit();
    return n;
    


def showauth(args, groupid, qqid):
    clean_cache();
    print(get_authlevel(qqid, groupid))
    if(len(args) == 1):
        return get_authlevel(qqid, groupid);
    elif(len(args) == 2):
        aimqqid = read_qqid(args[1]);
        print(get_authlevel(aimqqid, groupid))
        if(get_authlevel(qqid, groupid)<5):
            return "权限不足，请重试"
        elif(get_authlevel(qqid, groupid)<get_authlevel(aimqqid, groupid)):
            return "权限不足，请重试"
        else:
            n = get_authlevel(aimqqid, groupid);
        return "%d的权限值是：%d" %(aimqqid, n);



