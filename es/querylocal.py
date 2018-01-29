#!/usr/bin/env python
#-*- coding:utf8 -*-



#connect to our cluster
import elasticsearch
import json
es = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

import requests
res = requests.get('http://127.0.0.1:9200')
print(res.content)

print "finding index...\n"
index = []
for ind in es.indices.get('*'):
  print "found index %s \n" % ind
  index.append(ind)

for ind in index:
  #es.indices.delete(index = ind)
  print "delete index %s!!!\n" % ind


print "search\n"
qbody = {
    "query":{
      "match_all":{}
      }
    }
try:
  #res = es.search(index = 'test2',body = json.dumps(qbody))
  res = es.search(index = 'zipkin:span-2017-10-20',body = json.dumps(qbody))
  RES = json.dumps(res,indent = 2)
  print RES 
except elasticsearch.exceptions.NotFoundError:
  print "not found %s" % qbody 

hits = res["hits"]["hits"]  # list
for i in xrange(len(hits)):
  _id='AV843eaX59KmtfooZ45%s' % i
  #h dict
  h = hits[i]
  source = h.get("_source") # dict
  source["tags"]["smaug"] = "smaug"
  source["testsmaug"] = "testsmaug"
  port = source["localEndpoint"]["port"]
  if port == 9001:
    source["id"] = source["id"][:-2] + "45"
    es.index(index='zipkin:span-2017-10-20', doc_type='span', id=_id, body=source)


