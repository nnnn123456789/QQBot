import pymysql
import configparser
from api import *;

cf=configparser.ConfigParser()
cf.read("settings.ini")

db = pymysql.connect(cf.get('database', 'address'), cf.get('database', 'username'), cf.get('database', 'passwd'), cf.get('database', 'sqlname'))
cursor = db.cursor()
#execute = cursor.execute


def execute(str):
    db.ping(reconnect=True)
    return cursor.execute(str)


def sql_close():
    db.close()
    
    
def sql_commit():
    db.commit()
    

def get_points(qqid, groupid):
    n = execute('SELECT POINTS FROM points WHERE qqid = %d and groupid = %d' % (qqid,groupid))
    if(0 == n):
        execute('INSERT INTO points (qqid, groupid, points) values (%d, %d, 0)' % (qqid, groupid))
        db.commit()
        return 0
    elif(1 == n):
        return cursor.fetchone()[0]
    elif(n > 1):
        retlist = cursor.fetchall()
        retlist = [i[0] for i in retlist[:]]
        ret = max(retlist);
        db.commit()
        SQL_text = 'DELETE FROM `points` WHERE qqid = %d and groupid = %d'  % (qqid, groupid)
        execute(SQL_text)
        execute('INSERT INTO points (qqid, groupid, points) values (%d, %d, %d)' % (qqid, groupid, ret))
        db.commit()
        return ret
        

def set_points(qqid, groupid, value):
    n = execute('UPDATE points SET points = %d WHERE qqid = %d and groupid = %d' % (value, qqid, groupid))
    if(0 == n):
        execute('INSERT INTO points (qqid, groupid, points) values (%d, %d, 0)' % (qqid, groupid, value))
        db.commit()
    return n
    

def add_points(qqid, groupid, value):
    n = execute('UPDATE points SET points = points + %d WHERE qqid = %d and groupid = %d' % (value, qqid, groupid))
    if(0 == n):
        execute('INSERT INTO points (qqid, groupid, points) values (%d, %d, %d)' % (qqid, groupid, value))
    db.commit()
    return n


def minus_points(qqid, groupid, value):
    n = execute('UPDATE points SET points = points - %d WHERE qqid = %d and groupid = %d' % (value, qqid, groupid))
    if(0 == n): 
        execute('INSERT INTO points (qqid, groupid, points) values (%d, %d, %d)' % (qqid, groupid, -value))
    db.commit()
    return n


def literal_execute(args, groupid, qqid):
    if(get_authlevel(qqid, groupid)<12):
        return "权限不足"
    elif not len(args) == 2: 
        return "参数错误"
    return str(eval(args[1]))


def set_var(groupid, varname, value):
    n = execute('SELECT * FROM vars WHERE name = \'%s\' and groupid = %d' % (varname, groupid))
    if n == 0:
        execute('INSERT INTO vars (groupid, name, value) values (%d, \'%s\', \'%s\')' % (groupid, varname, value))
    else:
        execute('UPDATE vars SET value = \'%s\' WHERE name = \'%s\' and groupid = %d' % (value, varname, groupid)) 
    db.commit()
    return


def get_var(groupid, varname, default = "", autoset = True):
    n = execute('SELECT value FROM vars WHERE name = \'%s\' and groupid = %d' % (varname, groupid))
    if n == 0:
        if autoset:
            execute('INSERT INTO vars (groupid, name, value) values (%d, \'%s\', \'%s\')' % (groupid, varname, default))
            db.commit()
        return default
    else:
        return cursor.fetchone()[0]


