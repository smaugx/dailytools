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


jstr = {
          "kind": "SERVER",
          "traceId": "4514fe141b1ba266",
          "timestamp_millis": 1508486936305,
          "localEndpoint": {
            "serviceName": "backend2",
            "ipv4": "10.0.1.177",
            "port": 9001
          },
          "timestamp": 1508486936305128,
          "tags": {
            "http.uri": "/api",
            "http.uri.qs": "/api",
            "response_status_code": "200"
          },
          "parentId": "9b044e95c5cb49dc",
          "duration": 351,
          "shared": 'true',
          "id": "11b57bc4ea3ce588",
          "name": "get /api"


}
es.index(index='zipkin:span-2017-10-20', doc_type='span', id='AV83vN0P59KmtfooZAc2', body=jstr)

