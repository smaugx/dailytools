#!/usr/bin/env python
#-*- coding:utf8 -*-

import pdb


#connect to our cluster
import elasticsearch
es = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


# make sure ES is up and running
import requests
res = requests.get('http://127.0.0.1:9200')
print(res.content)


#let's iterate over swapi people documents and index them
import json

print "index!!!...."
i = 1
while i < 3:
  res = requests.get('http://swapi.co/api/people/'+ str(i))
  if res.status_code == 200:
    source = json.loads(res.content)
    es.index(index='sw', doc_type='people', id=i, body=source)
    print 'index %d success! \n' % i
  i += 1

i = i-1
print "get!!!..."
try:
  while i > 0:
    r = es.get(index='sw',doc_type= 'people',id = i)
    print json.dumps(r,indent = 4)
    i -= 1
except elasticsearch.exceptions.NotFoundError:
  print 'error'

