#!/usr/bin/env python
#-*- coding:utf8 -*-



#connect to our cluster
import copy 
import elasticsearch
from elasticsearch import helpers
es = elasticsearch.Elasticsearch([{'host': 'localhost', 'port': 9200}])


# make sure ES is up and running
import requests
res = requests.get('http://localhost:9200')
print(res.content)


#let's iterate over swapi people documents and index them
import json
example = {
    "_index":"",
    "_type":"",
    "_id":"",
    "_source":""
    }


action = []
def append(_index,_type,_id,_source):
  oneindex = copy.deepcopy(example)
  oneindex['_index'] = _index
  oneindex['_type'] = _type
  oneindex['_id'] =  _id
  oneindex['_source'] = _source
  action.append(oneindex)
  
print "index!!!...."
i = 1
while i < 20:
  res = requests.get('http://swapi.co/api/people/'+ str(i))
  if res.status_code == 200:
    source = json.loads(res.content)
    append('sw','people',i,source)
    #es.index(index='sw', doc_type='people', id=i, body=source)
    print 'index %d success! \n' % i
  i += 1

i = i-1
helpers.bulk(es,action)
print "bulk: %s counts " % i

