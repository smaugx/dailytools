#!/usr/bin/env python
#-*- coding:utf8 -*-

import copy

#connect to our cluster
import elasticsearch
from elasticsearch import helpers
es = elasticsearch.Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])


# make sure ES is up and running
import requests
res = requests.get('http://127.0.0.1:9200')
print(res.content)


#let's iterate over swapi people documents and index them
import json


example = {
    "name":"",
    "age":"",
    "sex":""
    }

def append(name,age,sex):
  source = copy.deepcopy(example)
  source["name"] = name
  source["age"] = age
  source["sex"] = sex
  return source 

document = {
    "_index":"",
    "_type":"",
    "_id":"",
    "_source":""
    }


action = []
def create_doc(_index,_type,_id,_source):
  oneindex = copy.deepcopy(example)
  oneindex['_index'] = _index
  oneindex['_type'] = _type
  oneindex['_id'] =  _id
  oneindex['_source'] = _source
  action.append(oneindex)
 


if __name__ == "__main__":
  print "index!!!...."
  source = append("jsper",17,"male")
  es.index(index='test', doc_type='people',id=1, body=source)
  source = append("david",18,"female")
  es.index(index='test', doc_type='people', id=2,body=source)
  source = append("enhen",19,"male")
  es.index(index='test', doc_type='people', id=3,body=source)
  print 'index  success! \n' 
  
  print "get!!!..."
  try:
    r = es.get(index='test',doc_type= 'people',id = 2)
    print json.dumps(r,indent = 4)
  except elasticsearch.exceptions.NotFoundError:
    print 'error'
  
  print "bulk\n"
  source = append("smaug",25,"male")
  create_doc("test2","people",1,source)
  source = append("ablex",24,"female")
  create_doc("test2","people",2,source)
  source = append("lucas",26,"female")
  create_doc("test2","people",3,source)



  helpers.bulk(es,action)
  print "bulk finished! " 
  r = es.get(index='test2',doc_type= 'people',id = 2)
  print json.dumps(r,indent = 4)


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
    print "not found %s" % query 

