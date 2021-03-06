#!/usr/bin/env python  
#coding=utf-8 

from socket import *  
import os 
from sys import *
from random import Random

HOST = '192.168.126.99'
PORT = 7722
UPORT = '57074'
LPORT = '21000'

sip_rtp_addr = (HOST, PORT) 
sip_rtp_socket = socket(AF_INET, SOCK_DGRAM)

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str

def send_U(u_data):
    '发送U命令到RTPProxy'
    '''print 'send: '+ u_data'''
    sip_rtp_socket.sendto(u_data, sip_rtp_addr) 
    '''print sip_rtp_socket.getsockname()'''
    u_recv = sip_rtp_socket.recv(2048)
    '''print 'recv: '+u_recv'''
    u_port = u_recv.split(' ')
    recv_port_addr = (HOST, int(u_port[1]))
    recv_port_socket = socket(AF_INET, SOCK_DGRAM)
    print ' \tU(callee)-> ' + u_port[1]

def send_L(u_data):
    '发送L命令到RTPProxy'
    '''print 'send: '+ l_data'''
    sip_rtp_socket.sendto(l_data, sip_rtp_addr) 
    l_recv = sip_rtp_socket.recv(2048)
    '''print 'recv: ' + l_recv'''
    l_port = l_recv.split(' ')
    send_port_addr = (HOST, int(l_port[1]))
    send_port_socket = socket(AF_INET, SOCK_DGRAM)
    print ' \tL(caller)-> ' + l_port[1]

def send_data(local_port, remote_port):
    i = 0
    send_port_addr = (HOST, int(remote_port))
    send_port_socket = socket(AF_INET, SOCK_DGRAM)
    if (local_port != ""):
        send_port_socket.bind(("", int(local_port)))
    fd = open('rtpdata','r')
    try:
        data = fd.read()
    finally:
        fd.close()
    while 1:
        send_port_socket.sendto(data, send_port_addr)
        (my_addr, my_port) = send_port_socket.getsockname()
        if (i == 0):
            print 'local_port= ' + str(my_port) + ' remote_port= ' + str(remote_port)
            i = 1
    send_port_socket.close()
    
cookie = raw_input('Enter the  ()default cookie (*)random cookie: ')
if (cookie == ''):
    cookie = '12345'
elif (cookie == '*'):
    cookie = random_str()
else:
    print 'cookie parameter error!'
    exit(-1);
command = raw_input('Enter the command [u/l]: ')
if (command == 'u'):
    call_id = random_str() 
    print 'call_id: ' + call_id
    u_data = cookie + ' Uc107,100,106,6,0,105,18,3,5,101 ' + call_id +  ' 192.168.126.99 ' + UPORT + ' 67369262;1'
    send_U(u_data);
elif (command == 'l'):
    call_id = raw_input('Enter the call_id: ')
    l_data = cookie + ' Lc0,101 '+ call_id + ' 192.168.126.99 ' + LPORT + ' 67369262;1 1a13684abaedd9d8;1'
    send_L(l_data);
else:
    print 'comman error!'
    exit(-1)
