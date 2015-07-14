#!/usr/bin/env python  
#coding=utf-8 

from socket import *  
import os 
from sys import *

HOST = '192.168.126.99'
PORT = 7722
UPORT = '57074'
LPORT = '21000'
cookie1 = '15311_32_ad7bd04eab6c85e3'
cookie2 = '15311_31_ad7bd04eab6c85e3'
if len(argv) == 2:
    call_id = argv[1]
else:
    call_id = '76589MGU5YzZlOWE3MWFiYjM2YTVlMmI0Y2YwMGZmNTk2NnE'
u_data = cookie1 + ' Uc107,100,106,6,0,105,18,3,5,101 ' + call_id +  ' 192.168.126.99 ' + UPORT + ' 67369262;1'
l_data = cookie2 + ' Lc0,101 '+ call_id + ' 192.168.126.99 ' + LPORT + ' 67369262;1 1a13684abaedd9d8;1'

sip_rtp_addr = (HOST, PORT) 
sip_rtp_socket = socket(AF_INET, SOCK_DGRAM)

def send_U():
    '发送U命令到RTPProxy'
    print 'send: '+ u_data
    sip_rtp_socket.sendto(u_data, sip_rtp_addr) 
    print sip_rtp_socket.getsockname()
    u_recv = sip_rtp_socket.recv(2048)
    print 'recv: '+u_recv
    u_port = u_recv.split(' ')
    recv_port_addr = (HOST, int(u_port[1]))
    recv_port_socket = socket(AF_INET, SOCK_DGRAM)
    print 'U(callee)-> ' + u_port[1]

def send_L():
    '发送L命令到RTPProxy'
    print 'send: '+ l_data
    sip_rtp_socket.sendto(l_data, sip_rtp_addr) 
    l_recv = sip_rtp_socket.recv(2048)
    print 'recv: ' + l_recv
    l_port = l_recv.split(' ')
    send_port_addr = (HOST, int(l_port[1]))
    send_port_socket = socket(AF_INET, SOCK_DGRAM)
    print 'L(caller)->' + l_port[1]

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
    
get_cmd = raw_input('Enter an cmd[u/l/r(caller)/e(callee)]: ')
if (get_cmd == "u"):
    send_U();
    sip_rtp_socket.close() 
elif (get_cmd == "l"):
    send_L();
    sip_rtp_socket.close() 
elif (get_cmd == "r"):
    lport = raw_input('Enter an local port ([omitted]random [*]default): ')
    rport = raw_input('Enter an remote port: ')
    if (lport == "*"):
        lport = UPORT
    send_data(lport, int(rport))
elif (get_cmd == "e"):
    lport = raw_input('Enter an local port ([omitted]random [*]default): ')
    rport = raw_input('Enter an remote port: ')
    if (lport == "*"):
        lport = LPORT
    send_data(lport, int(rport))
