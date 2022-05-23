from database import get_var, set_var
from api import get_group_ans_pool;
#from api import *;


def commands_allow(args, groupid, qqid):
    set_var(groupid, "allow_commands", "True")
    return "已允许命令执行"


def commands_disallow(args, groupid, qqid):
    set_var(groupid, "allow_commands", "False")
    return "已禁止命令执行"


def fun_allow(args, groupid, qqid):
    set_var(groupid, "allow_fun", "True")
    return "已允许娱乐功能"


def fun_disallow(args, groupid, qqid):
    set_var(groupid, "allow_fun", "False")
    return "已禁止娱乐功能"


def local_allow(args, groupid, qqid):
    if len(args) != 2:
        return "请求参数错误"
    keys = get_group_ans_pool().keys()
    print(keys);
    if args[1] not in keys:
        return "找不到该命令"
    varname = "allow_%s" % args[1]
    set_var(groupid, varname, "True")
    return "已启用命令%s" % args[1]
        
        
def local_disallow(args, groupid, qqid):
    if len(args) != 2:
        return "请求参数错误"
    keys = get_group_ans_pool().keys()
    print(keys);
    if args[1] not in keys:
        return "找不到该命令"
    varname = "allow_%s" % args[1]
    set_var(groupid, varname, "False")
    return "已禁用命令%s" % args[1]

