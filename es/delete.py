#!/usr/bin/env python
#-*- coding:utf8 -*-



#connect to our cluster
import elasticsearch
import json
es = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

index = []
for ind in es.indices.get('*'):
  print "found index %s \n" % ind
  index.append(ind)

for ind in index:
  es.indices.delete(index = ind)
  print "delete index %s!!!\n" % ind


print "scan all index again! \n"
for index in es.indices.get('*'):
  print index
