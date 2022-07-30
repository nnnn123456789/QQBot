from api import *
from event import *;
import websocket
import json


def on_message(ws, message):
	msg = json.loads(message)
	#print(msg);
	print(" ");
	#print(" ");
	if (msg["post_type"] == "message"):
		if(msg["message_type"] == "private"):
			on_private_message(msg);
		elif(msg["message_type"] == "group"):
			on_group_message(msg);
	elif(msg["post_type"] == "notice"):
		#print(msg);
		if(msg["notice_type"] == "group_admin"):
			on_group_manager_change(msg);
		elif(msg["notice_type"] == "group_increase"):
			on_group_users_add(msg);
		elif(msg["notice_type"] == "group_decrease"):
			on_group_users_delete(msg);		
		elif(msg["notice_type"] == "group_ban"):
			on_group_ban(msg);		
		elif(msg["notice_type"] == "group_upload"):
			on_group_document_upload(msg);	
		elif(msg["notice_type"] == "group_recall"):
			on_group_message_recall(msg);	
		elif(msg["notice_type"] == "friend_recall"):
			on_private_message_recall(msg);				
	elif(msg["post_type"] == "request"):		
		if(msg["request_type"] == "friend"):
			on_request_friend_add(msg);
		elif(msg["request_type"] == "group"):
			on_request_group_invite(msg);
	elif(msg["post_type"] == "meta_event"):
		if(msg["meta_event_type"] == "heartbeat"):
			on_heartbeat(msg);


def on_error(ws, error):
    print(ws)
    print(error)

    


def on_close(ws):
    print(ws)
    print("### closed ###")


websocket.enableTrace(True)
ws = websocket.WebSocketApp("ws://127.0.0.1:6700/",
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

ws.run_forever()