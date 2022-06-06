from msilib.schema import Error
import requests;
import json;

global group_ans_pool2;
group_ans_pool2 = {}

host_addr = 'http://127.0.0.1:5700/'


class CommandError(Exception):
    pass
class Executer:
    
    def __init__(self):
        self.handle_dict = {};

    
    def add(self, name:str, func):
        self.handle_dict["name"] = func

    
    def __call__(self, api_name : str, paras : dict):
        func = self.handle_dict.get(api_name);
        if func == None:
            raise CommandError("command not found")
        return func(paras)


class Event:

    def __init__(self, handle, api_request = [], **kwargs):
        self.api_request = api_request
        self.handle = handle
        self.executer = None
    

    def set_executer(self, executer : Executer):
        self.executer = executer

    
    def __call__(self, user_id, channel_id, *args):
        return self.handle(user_id, channel_id, self.executer, *args)


class event_pool:

    def __init__(self):
        self.cmdpool = {}
        self.apipool = {}

    def add(self, command : str, event : Event):
        api_exec = Executer()
        #for i in 




def get_group_ans_pool():
    return group_ans_pool2;


def send_private_message (user_id, message, auto_escape=False, group_id = 0):
    if(len(message) >=128):
        r1 = send_private_message (user_id, message[:120], auto_escape, group_id)
        r2 = send_private_message (user_id, message[120:], auto_escape, group_id)
        return r1 + r2;
    group_id = 0; ##disallow private msg via group
    #return;
    url = host_addr + 'send_private_msg'
    if (group_id == 0):
        d = {'user_id':user_id,'message': message,'auto_escape': auto_escape}
    else:
        d = {'user_id':user_id, 'group_id':group_id,'message': message,'auto_escape': auto_escape}
    r = requests.post(url, data=d)
    return [json.loads(r.text)["data"]]


def send_private_message_by_group (user_id, group_id, message, auto_escape=False):
    #return;
    url = host_addr + 'send_private_msg'
    d = {'user_id':user_id, 'group_id':group_id,'message': message,'auto_escape': auto_escape}
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"]
    
    
def send_group_message(group_id, message, auto_escape=False):
    #return;
    url = host_addr + 'send_group_msg'
    d = {'group_id':group_id,'message': message,'auto_escape': auto_escape}
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"]


def send_discuss_message(discuss_id, message, auto_escape=False):
    url = host_addr + 'send_group_msg'
    d = {'discuss_id':discuss_id,'message': message,'auto_escape': auto_escape}
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"]


def get_group_member_info(groupid, qqid):
    url = host_addr + 'get_group_member_info'
    d = {'group_id':groupid, 'user_id':qqid,'no_cache':True}
    r = requests.post(url, data=d)
    js = json.loads(r.text);
    #print(js);
    return js["data"]

# "owner" "admin" "member"
def get_group_member_role(groupid, qqid):
    data = get_group_member_info(groupid, qqid);
    return data["role"]


def set_group_ban(qqid, groupid, duration):
    url = host_addr + 'set_group_ban'
    d = {'group_id':groupid,'user_id': qqid,'duration': duration}
    #print(d);
    r = requests.post(url, data=d)


def get_group_member_title(groupid, qqid):
    data = get_group_member_info(groupid, qqid);
    d = data['title'];
    #print(data);
    return d


def get_group_member_card(groupid, qqid):
    data = get_group_member_info(groupid, qqid);
    d = data['card'];
    #print(data);
    return d


def clean_cache():
    url = host_addr + 'clean_cache'
    d = {}
    r = requests.post(url, data=d)
    return {}


def set_group_kick(qqid, groupid):
    url = host_addr + 'set_group_kick'
    d = {'group_id':groupid,'user_id': qqid,'reject_add_request': False}
    r = requests.post(url, data=d)
    return {};


def delete_msg(msgid):
    url = host_addr + 'delete_msg'
    d = {'message_id':msgid}
    r = requests.post(url, data=d)
    return {};


def get_msg(msgid):
    url = host_addr + 'get_msg'
    d = {'message_id':msgid}
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"];


def get_msg_sender(msgid):
    data = get_msg(msgid);
    #print(data)
    return data["sender"]["user_id"];

    
def set_group_add_request(flag, type, approve = True, reason = ""):
    url = host_addr + 'set_group_add_request'
    d = {'flag':flag,'type':type,'approve':approve,'reason':reason }
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"];



def set_group_card(group_id, user_id, card = ""):
    url = host_addr + 'set_group_card'
    d = {'group_id':group_id,'user_id':user_id,'card':card}
    r = requests.post(url, data=d)
    return json.loads(r.text)["data"];








    