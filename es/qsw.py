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
        if res['hits'].has_key('total'):
            return res['hits']['total']
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
    index="logstash-marco_access_tiebavideo-{0}"
    index_fmt=get_fmt()

    end_time = int(time.time()*1000)
    start_time = end_time - interval
    range={"@timestamp" : { "from":start_time, "to":end_time}}

    condition_match={"bucket":"tiebavideo"}
    qbody=get_qbody(condition_match, range)
    index = index.format(index_fmt)
    total = query_es(index, qbody)

    condition_match={"status":"499"}
    qbody=get_qbody(condition_match, range)
    err_499 = query_es(index, qbody)

    groupid=102

    if not total or not err_499:
        send_warning(groupid, "[ERR]: baidu tieba es data is null")
        return

    ratio = err_499 * 100.0 / total
    if ratio >= 1.5:
        send_warning(groupid, "[ERR]: baidu tieba 499 ratio: {}%. total:{}, erro_499:{}".format(ratio, total, err_499))

while True:
    do()
    time.sleep(interval)
