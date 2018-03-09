#!/usr/bin/env python
#-*- coding:utf8 -*-

'''
功能：将 fio 输出结果格式化为 json 
  data.source 来自 fio 测试的结果输出，原始文件;
  data.json 把上面的原始文件转换成格式化的 json ;
'''

import os
import json
import pdb

source_file ,des_file = '',''

#仅仅需要修改type 为SATA 即可
type = 'SATA'

if  type == 'SSD':
  #ssd 数据
  source_file = './ssd_data.source'
  des_file = './ssd_data.json'
else:
  #sata  数据
  source_file = './sata_data.source'
  des_file = './sata_data.json'

STORE = {}
lines = []

with open(source_file,'r') as fin:
  lines = fin.readlines()
fin.close()

drwitem = {}
dbs  ={}
rwitem = ""
bw,iops = "",""
bw_iops = {}

for l in xrange(len(lines)):
  if ".log" in lines[l]:
    rwmode = lines[l][1:-6]
    dbs = {}

  elif "fio-" in lines[l]:
    bs = filter(str.isdigit, lines[l])
    drwitem = {}

  elif "iops" in lines[l]:
    rwitem ,bw,iops ="", "",""
    bw_iops = {}

    item = lines[l].split()
    rwitem = item[0]
    if "read" in rwitem:
      rwitem = "read"
    elif "write" in rwitem:
      rwitem = "write"
    for i in item:
      if "bw" in i:
        bw = filter(str.isdigit,i)
      elif "iops" in i:
        iops = filter(str.isdigit,i)

  if bw:
    bw_iops["bw"] = bw
    bw_iops["iops"] = iops
    drwitem[rwitem] = bw_iops
    rwitem ,bw,iops ="", "",""

  if drwitem:
    dbs[bs] = drwitem

  if dbs:
    STORE[rwmode] = dbs

S = json.dumps(STORE,indent = 4)
if not os.path.exists(des_file):
  with open(des_file ,'w') as fout:
    fout.write(S)
  fout.close()
print S
