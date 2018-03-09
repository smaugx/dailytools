#!/usr/bin/env python
#-*- coding:utf8 -*-
'''
  将格式化之后的 json 文件解析后，以 key 的方式存入 redis
'''

import json
import os
import redis



lpool = redis.ConnectionPool(host='127.0.0.1', port=9999)
lr = redis.StrictRedis(connection_pool = lpool)

des_file = ''
#SSD仅仅需要修改type 为SATA 即可
type = 'SATA'

if  type == 'SSD':
  des_file = './ssd_data.json'
else:
  des_file = './sata_data.json'

SETNAME="FIODISK"
STORE = {}

with open(des_file ,'r') as fin:
  STORE = json.loads(fin.read())
fin.close()


count = 0
for (rwmode,dbs) in STORE.items():
  for (bs,drwitem) in dbs.items():
    for (rwitem,bw_iops) in drwitem.items():
      bw = bw_iops.get("bw")
      iops = bw_iops.get("iops")

      # 比如: SSD_rw_read_1024 或者 SSD_read_write_512
      hkey = "%s_%s_%s_%s" % (type,rwmode , rwitem, bs)
      count += 1
      if not lr.sismember(SETNAME,hkey):
        lr.sadd(SETNAME,hkey)

      lr.hset(hkey,"iops",iops)
      lr.hset(hkey,"bw",bw)
      lr.hset(hkey,"bs",bs)

      print "insert %s to redis" % hkey

print "总计：插入 %s 个 hash key to redis:9999,所有 hash key 可以在无序列表 %s 里找到" % ( count,SETNAME)
