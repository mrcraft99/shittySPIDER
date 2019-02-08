#encoding=utf-8
import itchat

def init():
    itchat.auto_login()

def send_msg_friend(msg, name):
    friends = itchat.search_friends(name=name) #nickname
    itchat.send(msg, friends[0]['UserName'])

def send_msg_group(msg, name):
    #TODO
    pass
