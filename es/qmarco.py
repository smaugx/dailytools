#!/usr/bin/env python

import pdb
import time, os
from datetime import datetime
from elasticsearch import Elasticsearch
import  elasticsearch 

host="192.168.60.36"
interval= 60 * 60 * 1000

def get_qbodya(match, range):
    qbody = {
        "query" : {
            "filtered" : {
                "filter" : {
                    "range" : range
                },
                "query" : {
                    "match" : match
                }
            }
        }
    }
    return qbody

# MUST: AND; SHOULD: OR; MUST_NOT:NOT
def get_qbody(match, range):
    qbody = {
        "query" : {
        "bool": {
        #"must":[{"term":{"node_type":"customer_gifshow_uploadlog"}},{"term":{"content_length":0}}]
        "should":[{"term":{"node_type":"customer_gifshow_uploadlog"}},{"term":{"retry":"false"}}]
        #"should":[{"term":{"bucket":"yd-image"}}]
        #"must_not":[]
        }
        }
    }
    return qbody


es = Elasticsearch([host])

def query_es(index, qbody):
    try:
        #res = es.search(index = index, doc_type = 'customer_gifshow_uploadlog',body = qbody,scroll='2m',search_type='scan',size=1000)
        res = es.search(index = index, body = qbody)
        if res['hits'].has_key('total'):
            return res['hits']['total'] ,res['hits']['hits']
    except:
        print "query es failed"

def get_fmt():
    timestamp = time.time()
    tt = time.localtime(timestamp)
    fmt = time.strftime('%Y.%m.%d', tt)
    return fmt

def do():
    index="logstash-marco_access_tiebavideo-{0}"
    index="logstash-customer_gifshow_uploadlog-{0}"
    index_fmt=get_fmt()

    endtime = "2017-07-20 00:30:00"
    end = int(time.mktime(time.strptime(endtime,'%Y-%m-%d %H:%M:%S')))
    end_time = end * 1000
    #end_time = int(time.time()*1000)
    start_time = end_time - interval
    range={"@timestamp" : { "from":start_time, "to":end_time}}

    condition_match={"node_type":"customer_gifshow_uploadlog"}
    qbody=get_qbodya(condition_match, range)
    index = index.format(index_fmt)
    index = 'logstash-customer_gifshow_uploadlog-2017.07.19'
    #print index
    total,array  = query_es(index, qbody)
    #print total

    _id = []
    #print array[0]
    for s in array:
        _id.append(s.get('_id'))


    print len(_id)
    for i in _id:
        #es.indices.delete(index = index,doc_type = ")
        try:
            es.delete(index= index ,doc_type="customer_gifshow_uploadlog",id=i)
            print "delete %s " % i
        except elasticsearch.exceptions.NotFoundError:
            break

#while(True):
do()
