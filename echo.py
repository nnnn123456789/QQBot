
def echo(args, groupid, qqid):
    keys  = ["抽奖", "sleep", "积分"];
    
    if not len(args) == 2: 
        return ""
    for i in keys:
        if i in args[1]:
            if not qqid == 2234748103:
                return ""
    return args[1]
