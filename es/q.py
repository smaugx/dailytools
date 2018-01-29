#!/usr/bin/env python

import time, os
from datetime import datetime
from elasticsearch import Elasticsearch

host="192.168.60.36"
interval= 15 * 60 * 1000

def get_qbody(match, range):
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

es = Elasticsearch([host])

def query_es(index, qbody):
    try:
        res = es.search(index = index, body = qbody)
        print res
        if res['hits'].has_key('total'):
            return res['hits']['total']
    except:
        print "query es failed"

def get_fmt():
    timestamp = time.time()
    tt = time.localtime(timestamp)
    fmt = time.strftime('%Y.%m.%d', tt)
    return fmt

def do():
    index="logstash-customer_gifshow_report-{0}"
    index_fmt=get_fmt()

    end_time = int(time.time()*1000)
    start_time = end_time - interval
    range={"@timestamp" : { "from":start_time, "to":end_time}}

    #condition_match={"bucket":"tiebavideo"}
    condition_match={"area":"beijing"}
    qbody=get_qbody(condition_match, range)
    index = index.format(index_fmt)
    print index
    total = query_es(index, qbody)
    print total

do()
