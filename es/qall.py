#!/usr/bin/env python

import pdb
import time, os
from datetime import datetime
from elasticsearch import Elasticsearch
import logging


host="192.168.60.36"
interval= 60 * 60 * 1000

tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))
es = Elasticsearch([host])



def get_qbodya(match, range):
    qbody = {
        "query" : {
            "filtered" : {
                "filter" : {
            "range":range
                },
                "query" : {
                    "match" : match
                }
            }
        }
    }
    return qbody

def get_qbodyb(match, range):
    qbody = {
        "query" : {
                    "match_all":{} 
        }
    }

    return qbody

def get_qbody(match, range):
    qbody = {
        "query" : {
            "filtered" : {
                "filter" : {
            "term": {"bucket":"yd-image"},
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


def query_es(index, qbody):
    try:
        pdb.set_trace()
        content = []
        #res = es.search(index = index, body = qbody)
        res = es.search(index = index, body = qbody,scroll='2m',search_type='scan',size=1000)
        sid = res['_scroll_id']
        print sid
        print res
        scroll_size = res['hits']['total']
        while (scroll_size > 0):
            print "Scrolling..."
            page = es.scroll(scroll_id = sid, scroll = '2m')
            # Update the scroll ID
            sid = page['_scroll_id']
            # Get the number of results that we returned in the last scroll
            scroll_size = len(page['hits']['hits'])
            content.extend(page['hits']['hits'])
            print "scroll size: " + str(scroll_size)
            print page['hits']['hits']
            return content
    except:
        print "query es failed"

def get_fmt():
    timestamp = time.time()
    tt = time.localtime(timestamp)
    fmt = time.strftime('%Y.%m.%d', tt)
    return fmt

def send_warning(groupid, msg):
    cmd=" curl -XPOST -H'Content-Type: application/json' localhost:9595/upwarning -d '{\"group\": %s, \"msg\": \" %s \"}'" % (groupid, msg)
    os.system(cmd)

def do():
    index="logstash-customer_gifshow_uploadlog-{0}"
    index_fmt=get_fmt()

    endtime = "2017-07-20 00:30:00"
    end = int(time.mktime(time.strptime(endtime,'%Y-%m-%d %H:%M:%S')))
    end_time = end * 1000
    #end_time = int(time.time()*1000)
    start_time = end_time - interval
    range={"@timestamp" : { "from":start_time, "to":end_time}}

    condition_match={"node_type":"customer_gifshow_uploadlog"}
    qbody=get_qbodyb(condition_match, range)
    index = index.format(index_fmt)
    index = 'logstash-customer_gifshow_uploadlog-2017.07.19'
    r = query_es(index, qbody)
    urls=[]
    if not r:
        return

    for v in r:
        urls.append(v['_source']['request_uri'])

    with open("xuejun.txt","a+") as f:
        for k in r:
            f.write(str(k))
            f.write("\n")
            s = set(urls)
    with open("xuejun_uniq.txt","a+") as f:
        for k in s:
            f.write(k)
            f.write("\n")

do()
