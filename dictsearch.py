import os;
from stardict import DictCsv, open_dict;
import time;
import random;



dc = None
dc2 = None
init = False
init2 = False

def dc_init():
    global init
    init = True
    global dc
    dc = open_dict('stardict.db')


def dc2_init():
    global init2
    init2 = True
    global dc2
    dc2 = open_dict('stardict2.db')
    
def dc_getprompt(name):
    if not init:
        dc_init()
    retdict = dc.query(name)
    prompt = "单词: %s\n读音:/%s/\n释义:%s\n汉语释义:%s" % (retdict['word'], retdict['phonetic'],retdict['definition'],retdict['translation'])
    if retdict == None:
        return ""    
    return prompt
    
def dc2_getprompt(name):
    if not init2:
        dc2_init()
    retdict = dc2.query(name)
    prompt = "单词: %s\n读音:/%s/\n释义:%s\n汉语释义:%s" % (retdict['word'], retdict['phonetic'],retdict['definition'],retdict['translation'])
    if retdict == None:
        return ""    
    return prompt

def dict_search(args, groupid, qqid):
    if len(args) < 2: 
        return ""
    ret = "您查询到的结果如下: "
    for i in args[1:]:
        print("searching %s" % i)
        temp = dc_getprompt(i)
        print(temp)
        if temp:
            ret = ret + "\n\n" + temp
    return ret
    
def dict_search_id(args, groupid, qqid):
    if len(args) < 2: 
        return ""
    ret = "您查询到的结果如下: "
    for i_str in args[1:]:
        i = int(i_str)
        print("searching %d" % i)
        temp = dc_getprompt(i)
        print(temp)
        if temp:
            ret = ret + "\n\n" + temp
    return ret


def get_random_dict():
    if not init2:
        dc2_init()
    maxi = dc2.count();
    randi = random.randint(0,maxi);
    temp = dc2_getprompt(randi)
    print(temp)
    return temp


def randword(args, groupid, qqid):
    n = 1;
    if len(args) == 2:
        try:
            n = int(args[1]);
        except:
            pass;
    if n >= 10 :
        n = 10;
    if n <=1:
        n = 1;
    ret = "";
    for i in range(n):
        ret = ret + "\n\n" + get_random_dict();
    ret = ret[2:]
    return ret


