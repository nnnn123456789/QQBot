
import re



def div_args(str):
    div1 = str.split('"')
    temp = [ [div1[i], i%2==0] for i in range(len(div1))]
    ret = []
    for s, b in temp:
        if b:
            ret = ret + s.split(' ')
        else:
            ret = ret + [s]
    ret2 = []
    for i in ret:
        if not i == '':
            ret2 = ret2 + [i]
    return ret2


def read_qqid(str):
    return int(str.split('=')[-1].split(']')[0]);


def add_backslash(str):
    ret = "";
    for i in str:
        if i == '\'' or i == '\"' or i == '\\':
            ret = ret + '\\' + i;
        else:
            ret = ret + i;
    return ret;

