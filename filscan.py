#!/usr/bin/env python
#-*- coding:utf8 -*-

# -author:smaugx-

import csv
import json
import copy
import requests
import time
import random

filename = './filscan.csv'

def filscan(begin,end):
    url = 'https://api.filscan.io:8700/rpc/v1'
    my_headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=UTF-8',
            'Host': 'api.filscan.io:8700',
            'Origin': 'https://filscan.io',
            'Referer': 'https://filscan.io/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
            }

    my_data = {
            "id":1,
            "jsonrpc":"2.0",
            "params": [
                {
                    "method":"",
                    "address":"f02301",
                    "from_to":"",
                    "offset_range":
                    {
                        "start": begin,
                        "count": end
                    }
                }
            ],
            "method":"filscan.MessageByAddress"
        }

    data = []
    print("spider page begin={0} end={1}".format(begin, end))
    try:
        res = requests.post(url, headers = my_headers,data = json.dumps(my_data), timeout = 5)
        if res.status_code == 200:
            result = res.json().get('result')
            if result:
                data = result.get('data')
    except Exception as e:
        print("catch exception:{0}", e)

    template = {
            'MessageID': '',
            'Height': '',
            'Time': '',
            'From':'',
            'To':'',
            'Value':'',
            'Receipt':'',
            'Method':''
            }
    new_data = []
    for item in data:
        new_item = copy.deepcopy(template)
        new_item['MessageID'] = item.get('cid')
        new_item['Height'] = item.get('height')
        block_time = int(item.get('block_time'))
        time_local = time.localtime(block_time)
        dt = time.strftime('%Y-%m-%d %H:%M:%S', time_local)
        new_item['Time'] = dt
        new_item['From'] = item.get('from')
        new_item['To'] = item.get('to')
        new_item['Value'] = '{0} FIL'.format(int(item.get('value'))  * pow(10,-18))
        new_item['Receipt'] = 'OK'
        new_item['Method'] = item.get('method_name')
        new_data.append(new_item)

    print("spider page begin={0} end={1} get {2} items".format(begin, end, len(new_data)))
    return new_data


def json2csv(data, append=False):
    if not append:
        f = open(filename, 'w')
        csv_write = csv.writer(f)
        csv_write.writerow(data[0].keys())
        for row in data:
            csv_write.writerow(row.values())
        print("dump {0} items to file:{1}".format(len(data), filename))
        f.close()
    else:
        f = open(filename, 'a')
        csv_write = csv.writer(f)
        for row in data:
            csv_write.writerow(row.values())
        print("dump {0} items to file:{1}".format(len(data), filename))

    return

def run():
    total = 0
    step = 25
    begin = 0
    end = begin + step
    append = True
    for i in range(100):
        data = filscan(begin, end)
        total += len(data)
        if i == 0:
            append = False
        else:
            append = True
        json2csv(data, append)
        begin = end
        end += step
        print("\n")

    print("spider done, total items:{0}, data in file:{1}".format(total, filename))


if __name__ == "__main__":
    run()
