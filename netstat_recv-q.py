#!/usr/bin/env python  
#coding=utf-8

import commands 
import re
import datetime
import time

interval= 0.5
while 1:
    start_time = datetime.datetime.utcnow()
    (start_status, start_output)= commands.getstatusoutput('netstat -ap | grep rtp')

    time.sleep(interval)
    (end_status, end_output)= commands.getstatusoutput('netstat -ap | grep rtp')
    end_time = datetime.datetime.utcnow()

    start_ret = re.split(' *', start_output);
    end_ret = re.split(' *', end_output);
    for i in range(1, len(start_ret), 6):
        if (int(start_ret[i]) != 0 or int(start_ret[i]) != 0):
            ret = int(end_ret[i]) - int(start_ret[i])
            break
    if i > len(start_ret)-8:
        ret = int(end_ret[1]) - int(start_ret[1])

    print 'time:  ' + str(end_time - start_time)
    print 'count: ' + str(ret)
    print 'start data:\n' + start_output
    print 'end data:  \n' + end_output
    print '\n'


