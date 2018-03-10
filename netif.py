#!/usr/bin/env python
#-*- coding:utf-8 -*-
#脚本探测网卡流入带宽,循环输出

import os
import time
import pdb

filename = './bandwidth.log'

'''
[root@~]$ cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
    lo: 1144779885672 14057281982    0    0    0     0          0         0 1144779885672 14057281982    0    0    0     0       0          0
  eth0:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
  eth1:       0       0    0    0    0     0          0         0        0       0    0    0    0     0       0          0
  eth2: 26686495240 203608963    0    0    0     0          0         1 78529414436 193724479    0    0    0     0       0          0
  eth3: 10038847365 82467612    0    0    0     0          0         0 26209215795 64571217    0    0    0     0       0          0
 bond0: 36725342605 286076575    0    0    0     0          0         1 104738630231 258295696    0    0    0     0       0          0
'''

def get_rx(interface = 'eth0'):
  rsbytes = [] 
  cmd = 'cat /proc/net/dev'
  r = os.popen(cmd).readlines()
  if len(r) < 4:
    print "error: can't find eth interface"
    return rsbytes 
  interface_dict = {}
  for i in xrange(2,len(r),1): #从 lo 开始
    interface_name = r[i].split()[0].split(':')[0]
    interface_dict[interface_name] = i

  if interface in interface_dict:
    position = interface_dict.get(interface)
    recvbytes = r[position].split()[1]
    sendbytes = r[position].split()[9]
    rsbytes.append(int(recvbytes))
    rsbytes.append(int(sendbytes))

  return rsbytes 


def iftop_interface(interface = 'eth0'):
  begin = int(time.time())
  beginrs = get_rx(interface)
  if not beginrs:
    print 'error: can not find interface %s' % interface
    return 
  while True:
    time.sleep(2)
    endrs = get_rx(interface)
    end = int(time.time())
    rxrate = float((endrs[0] - beginrs[0])) / (end - begin)  * 8 
    sxrate = float((endrs[1] - beginrs[1])) / (end - begin)  * 8 
    tl = time.localtime(end)
    date = time.strftime('%m-%d %H:%M:%S', tl)
    cout = "%s  [recv(rate) = %s Mbps] [send(rate) = %s Mbps] \n" % (date,rxrate / 1000000,sxrate / 1000000)
    
    fout = open(filename,'a')
    fout.write(cout)
    fout.close()
    
    print cout
    
    #重新赋值，进入再次循环
    begin,beginrs = end,endrs


if __name__ == "__main__":
  iftop_interface('ens33')
