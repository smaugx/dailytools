#!/usr/bin/env python
#-*- coding:utf-8 -*-
#脚本探测网卡流入带宽,循环输出

import os
import time

filename = '/newadd/bandwidth.log'

def get_rx():
  ethrs = 0
  cmd = 'cat /proc/net/dev'
  r = os.popen(cmd).readlines()
  if len(r) < 4:
    print "error: can't find eth interface"
    return ethrs
  ethr = r[3] #可能是 eth0,也可能是其他的，具体可以修改这里实现探测不同的网卡
  #ethrs表示接收到的字节数
  ethrs = int(ethr.split()[1])    # 接收字节总数
  return ethrs


def iftop_eth0():
  begin = int(time.time())
  beginrx = get_rx()
  while True:
    time.sleep(2)
    endrx = get_rx()
    end = int(time.time())
    rxrate = float((endrx - beginrx)) / (end - begin)  * 8 
    tl = time.localtime(end)
    date = time.strftime('%m-%d %H:%M:%S', tl)
    cout = "%s  rx(rate) = %s Mbps\n" % (date,rxrate / 1000000)
    
    fout = open(filename,'a')
    fout.write(cout)
    fout.close()
    
    #print cout
    
    #重新赋值，进入再次循环
    begin,beginrx = end,endrx


if __name__ == "__main__":
  iftop_eth0()
