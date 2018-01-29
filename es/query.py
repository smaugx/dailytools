#!/usr/bin/env python
#-*- coding:utf8 -*-



#connect to our cluster
import elasticsearch
import json
es = elasticsearch.Elasticsearch([{'host': '192.168.60.36', 'port': 9200}])

import requests
res = requests.get('http://192.168.60.36:9200')
print(res.content)

query = {
    "query":{
      "match":{
        "node_type": "marco_access_baidu-yd"
        }
      }
    }

try:
  #res = es.search(index = 'marco_access_customer_gifshow_report',body = json.dumps(query))
  #res = es.search(index = 'logstash-marco_access_customer_gifshow_report',body = json.dumps(query))
  #res = es.search(index = 'sw',body = json.dumps(query))
  #res = es.search(index = 'logstash-marco_access_baidu-yd',body = json.dumps(query))
  res = es.search(index = 'marco_access_baidu-yd',body = json.dumps(query))
  RES = json.dumps(res,indent = 2)
  print RES
except elasticsearch.exceptions.NotFoundError:
  print "not found %s" % query 
