#!/usr/bin/env python
#-*- coding:utf8 -*
#循环执行top命令,输出某一个进程的cpu百分比(个性需求,故不是过滤/proc/pid/stat)

import os
import time

filename = '/newadd/edgetopcpu.log'

def get_top_cpu(service):
  sercpu = []
  cpu = ''
  cmd = 'top -b -n 3 -d 8'
  ret = os.popen(cmd).readlines()
  for r in ret:
    if service in r:
      sercpu.append(r)

  if len(sercpu) != 3:
    print "top excuate error!"
    return 0.0
  
  line = sercpu[-1]
  line = line.split()
  if line:
    cpu = line[8]

  return float(cpu)
    
    

def top_continue(service):
  minute_cpu = []
  tbegin = time.strftime('%H:%M',time.localtime(time.time()))
  while True:
    now = time.strftime('%H:%M',time.localtime(time.time()))
    cpu = get_top_cpu(service)
    if now == tbegin:
      minute_cpu.append(cpu)
    else:
      cpusum = 0.0
      for u in xrange(len(minute_cpu)):
        cpusum += minute_cpu[u]
      s_cpu = cpusum / len(minute_cpu)
      cout = '%s %s top_cpu  =  %s\n' % (tbegin,service,s_cpu)
      
      fout = open(filename,'a')
      fout.write(cout)
      fout.close()
      
      #print '%s %s top_cpu  =  %s' % (now,service,cpu)
      
      #clear  minute_cpu for next count
      minute_cpu[:] = []
      minute_cpu.append(cpu)
      tbegin = now
   
    
    #time.sleep(10)
  

if __name__ == "__main__":
  top_continue('edge')
