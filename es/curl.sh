curl -XGET 'http://192.168.60.36:9200/logstash-customer_gifshow_uploadlog-2017.07.19/_search?pretty' -d '{
  "facets": {
    "terms": {
      "terms": {
        "field": "node_type.raw",
        "size": 10,
        "order": "count",
        "exclude": []
      },
      "facet_filter": {
        "fquery": {
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
                          "from": 1500479919913,
                          "to": 1500483519913
                        }
                      }
                    },
                    {
                      "range": {
                        "@timestamp": {
                          "from": 1500480000435,
                          "to": 1500481515587
                        }
                      }
                    }
                  ]
                }
              }
            }
          }
        }
      }
    }
  },
  "size": 0
}'

