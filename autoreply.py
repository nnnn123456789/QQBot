import time
from bnu import is_bnugroup;


def my_seek(key, msg):
    keys = key.split(" ")
    if len(keys) == 0 :
        return False
    for k in keys:
        if msg.find(k) == -1:
            return False
    return True


def get_autoans(msg, groupid = 0):
    if is_bnugroup(groupid) == False:
        return ""
    for i in autoans_pool:
        k,v,t = i
        if my_seek(k, msg) :
            if(time.time() - 600 >= t):
                print( t)
                i[2] = time.time()
                return v.replace('\\n', '\n')
    return ""

#autoans_pool = [['招生办 电话', '北师大招生办电话：010-58807962', 0], ['保卫处 电话', '北师大保卫处24小时报警电话：010-58806110', 0], ['后勤 电话', '北师大后勤服务中心电话：010-58801111', 0], ['搜索引擎', '[CQ:image,file=fe828c62595577d364d46355216b9c60.image]', 0], ['校医院 电话', '北师大校医院电话：010-58805581，010-58808223', 0], ['图书馆 电话', '北师大图书馆电话：010-58809911', 0], ['节能办 电话', '北师大节能办电话：010-58808275', 0], ['师大地图', '师大高清校园地图见群文件', 0], ['学校 地图', '师大高清校园地图见群文件', 0], ['wei, zaima', '滚，不在', 0], ['教务电话本', '[CQ:image,file=26da040988c67e1aa8bf79d700e95e1a.image]', 0], ['麦当劳 电话', '北师大东门麦当劳电话：010-58802867', 0], ['？', '?', 0], ['小白鼠', '谁在叫 我？', 0]]
autoans_pool = []

def read_from_file():
    global autoans_pool
    #autoans_pool = []
    f = open("autoreply.txt","r")
    lines = f.readlines()
    #print(lines)
    f.close()
    for line in lines:
        l = line[:-1].split('\t')
        if not len(l) == 2:
            continue
        autoans_pool.append(l + [0])
    #print(autoans_pool)
    


def write_to_file():
    lines = [i[0] + '\t' + i[1] for i in autoans_pool]
    print(lines)
    buf = '\n'.join(lines) + '\n'
    f = open("autoreply.txt","w")
    f.write(buf)
    f.close()


def add_auto_reply(args, groupid, qqid):
    if not qqid == 2234748103:
        return "权限不足"
    if not len(args) == 3:
        return "参数错误"
    autoans_pool.append([args[1].strip(), args[2].replace('\r\n', '\n').replace('\n', '\\n'), 0])
    write_to_file()
    return "添加成功"
    
    
read_from_file()
write_to_file()
print(autoans_pool)