#!/usr/bin/env python
#-*- coding:utf8 -*-
'''
  从 redis 查数据，组织数据格式为 highcharts 所需格式
  TODO
'''


import os
import redis
import json
import operator
import copy
import pdb


rfilename = '/root/iruka/tempextra/fiodisk/result'


#以每秒为单位进行统计
def queryredis(r,param):
  series = []
  # 标识类型: SSD 或者 SATA
  type_select  = ["SSD","SATA"]
  # 读写模式：顺序读、顺序写、顺序读写、随机读、随机写、随机读写(read,write,rw,randread,randwrite,randrw)
  rwmode_select = ["read","write","rw","randread","randwrite","randrw"]
  if not r:
    return series 

  type = param.get("type")
  rwmode = param.get("rwmode")
  if type not in type_select or  rwmode not in rwmode_select:
    return series 

  hkeys = r.smembers("FIODISK")
  hkeys = list(hkeys)

  finalkeys = []
  disk_mode = type + "_" + rwmode      #形如: SSD_rw 、SSD_read
  for hk in hkeys:
    if hk.startswith(disk_mode):
      finalkeys.append(hk)
      
  ri,wi = {},{}
  for fk in finalkeys:
    fksp = fk.split("_")
    ditem = r.hmget(fk,"bs","iops","bw")
    if ditem[0] != None:
      if fksp[2] == 'read':
        ri[int(ditem[0])] = ditem[1:]     # {1024:['4407','141500']}
      else:   # 'write'
        wi[int(ditem[0])] = ditem[1:]     # {1024:['4407','141500']}

  #按照 bs 大小从小至大排序 (4,8,16,32,...)
  sortri  = sorted(ri.items(),key = operator.itemgetter(0),reverse=False)
  sortwi  = sorted(wi.items(),key = operator.itemgetter(0),reverse=False)

  #针对 read
  laiops_r,labw_r = [],[]
  for _ri in range(len(sortri)):
    lbiops,lbbw = [],[]
    lbiops.append(int(sortri[_ri][0]))    #追加 bs 字段
    lbbw.append(int(sortri[_ri][0]))    #追加 bs 字段
    lbiops.append(int(sortri[_ri][1][0]))  # 追加 iops 字段

    _bwmb = int(sortri[_ri][1][1])
    _bwmb = float('%.1f' % (_bwmb / 1024.0))
    lbbw.append(_bwmb)  # 追加 bw 字段,单位 MB/s,精度为小数点后一位
    #lbbw.append(int(sortri[_ri][1][1]))  # 追加 bw 字段

    laiops_r.append(lbiops)
    labw_r.append(lbbw)


  # 针对 write
  laiops_w,labw_w = [],[]
  for _wi in range(len(sortwi)):
    lbiops,lbbw = [],[]
    lbiops.append(int(sortwi[_wi][0]))    #追加 bs 字段
    lbbw.append(int(sortwi[_wi][0]))    #追加 bs 字段
    lbiops.append(int(sortwi[_wi][1][0]))  # 追加 iops 字段

    _bwmb = int(sortwi[_wi][1][1])
    _bwmb = float('%.1f' % (_bwmb / 1024.0))
    lbbw.append(_bwmb)  # 追加 bw 字段,单位 MB/s,精度为小数点后一位
    #lbbw.append(int(sortwi[_wi][1][1]))  # 追加 bw 字段

    laiops_w.append(lbiops)
    labw_w.append(lbbw)

  #read 和 write 的总和
  laiops,labw = copy.deepcopy(laiops_r),copy.deepcopy(labw_r)
  if not laiops or not labw:   #read 为空
    laiops,labw = copy.deepcopy(laiops_w),copy.deepcopy(labw_w)
  else:
    for s in xrange(len(laiops_w)):
      laiops[s][1]  += laiops_w[s][1]
    for w in xrange(len(labw_w)):
      labw[w][1]  += labw_w[w][1]
   
  #到此为止，laiops,laiops_r,laiops_w; labw,labw_r,labw_w 是我们所需要的几个list
  temp1 = {}
  temp1["name"] = "IOPS"
  temp1["data"] = laiops
  series.append(temp1)

  temp2 = {}
  temp2["name"]  = "BW"
  temp2["data"] = labw
  series.append(temp2)

  temp3 = {}
  temp3["name"] = "IOPS(read)"
  temp3["data"] = laiops_r
  series.append(temp3)

  temp4 = {}
  temp4["name"] = "BW(read)"
  temp4["data"] = labw_r
  series.append(temp4)

  temp5 = {}
  temp5["name"] = "IOPS(write)"
  temp5["data"] =  laiops_w
  series.append(temp5)

  temp6 = {}
  temp6["name"] = "BW(write)"
  temp6["data"] = labw_w
  series.append(temp6)

  return series 


def load(params):
  #cache statictis result db
  lpool = redis.ConnectionPool(host='127.0.0.1', port=9999)
  lr = redis.StrictRedis(connection_pool = lpool)
  global rfilename

  result = {}
  series = []
  
  '''
  params = {}
  params["type"] = "SSD"
  params["rwmode"] = "rw"
  '''
  flag = params.get("type") + "_" + params.get("rwmode")

  STORE = {}
  if os.path.isfile(rfilename):
    STORE = json.loads(open(rfilename).read())

  series = STORE.get(flag)
  if series:
    result[flag] = series
    print "found in %s" % rfilename
    return result 

  series = queryredis(lr,params)
  if series:
    result[flag] = series
    STORE[flag] = series
    ret = json.dumps(STORE,indent = 4)
    with open(rfilename,'w') as fout:
      fout.write(ret)
    fout.close()
    print 'dump to %s success' % rfilename
  else: # type or rwmode not right
    result['error'] = "params not right!"
  
  return result



if __name__ == "__main__":
  '''
  params = {'type':'SATA','rwmode':'randrw'}
  result = load(params)
  print json.dumps(result)
  '''

  pall = {'type':'','rwmode':''}
  _ltype = ['SSD','SATA']
  _lrwmode = ['rw','read','write','randrw','randread','randwrite']

  for t in _ltype:
    for m in _lrwmode:
      pall['type'] = t
      pall['rwmode'] = m
      load(pall)
 
  #None
