#!/usr/bin/env python
# -*- coding:utf8 -*-

import requests
import os
import json
import pdb

import time, os
from datetime import datetime
from elasticsearch import Elasticsearch
import  elasticsearch 

host="192.168.60.36"
total = 0


#curl -XGET 'http://uplog.s.upyun.com:80/logstash-customer_gifshow_uploadlog-2017.07.19/_search?pretty' -d 

def do():
    url = 'http://uplog.s.upyun.com:80/logstash-customer_gifshow_uploadlog-2017.07.19/_search?pretty'
    url =  'http://192.168.60.36:9200/logstash-customer_gifshow_uploadlog-2017.07.19/_search?pretty' 
    querybody = {
      "query": {
        "filtered": {
          "query": {
            "bool": {
              "should": [
                {
                  "query_string": {
                    "query": "*"
                  }
                },
                {
                  "query_string": {
                    "query": "*"
                  }
                }
              ]
            }
          },
          "filter": {
            "bool": {
              "must": [
                {
                  "range": {
                    "@timestamp": {
                      "from": 1500479700097,
                      "to": 1500481800097
                    }
                  }
                }
              ]
            }
          }
        }
      },
      "highlight": {
        "fields": {},
        "fragment_size": 2147483647,
        "pre_tags": [
          "@start-highlight@"
        ],
        "post_tags": [
          "@end-highlight@"
        ]
      },
      "size": 10000,
      "sort": [
        {
          "_id": {
            "order": "desc",
            "ignore_unmapped": True 
          }
        },
        {
          "@timestamp": {
            "order": "desc",
            "ignore_unmapped": True 
          }
        }
      ]
    }
    
    
    
    r = requests.post(url,data = json.dumps(querybody))
    store = r.json()
    
    #jsondata = json.dumps(store,indent = 4)
    #print jsondata
    
    _idlist = []
    hits = store['hits']['hits']    #list
    for h in hits:
        s = h['_id']
        _idlist.append(s)
    
    
    index = hits[0]['_index']
    type = hits[0]['_type']
    
    singlen = len(_idlist)
    global total

    print singlen
#    total += singlen
    #print index,type
    
    
    es = Elasticsearch([host])
    
    print "begin delete\n"
    for i in _idlist:
        #es.indices.delete(index = index,doc_type = ")
        try:
            es.delete(index= index ,doc_type= type,id=i)
            total += 1
            print "delete %s " % i
        except elasticsearch.exceptions.NotFoundError:
            break



while(True):
    do()
    print "finish do once, total delete %s " % total
    time.sleep(1)


#do()
#print "finish do once, total delete %s " % total
