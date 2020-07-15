#!/usr/bin/env python
#-*- coding:utf8 -*-

import json
import os
import time
import random
import requests


def MinifyHtmlUrl(html_url):
    url = 'https://minifyhtml.io/ajax/minify_url?q={0}'.format(html_url)

    myheaders = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://minifyhtml.io',
        'pragma': 'no-cache',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'referer': 'https://minifyhtml.io/?q={0}'.format(html_url),
            }

    minified_html = ''
    try:
        r = requests.get(url,  headers = myheaders)
        if r.status_code != 200:
            print('http get request failed with code:{0}'.format(r.status_code))
            return minified_html

        content = r.text
        content = json.loads(content)
        minified_html = content.get('data').get('minified')
    except Exception as e:
        print('catch exception: {0}'.format(e))

    print(minified_html)
    return minified_html




def MinifyHtmlText(html_content):
    url = 'https://minifyhtml.io/ajax/minify_text'

    myheaders = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://minifyhtml.io',
        'pragma': 'no-cache',
        'referer': 'https://minifyhtml.io/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
            }

    payload = {
            'json': html_content,
            }
    minified_html = ''
    try:
        r = requests.post(url,  headers = myheaders, data = payload)
        if r.status_code != 200:
            print('http get request failed with code:{0}'.format(r.status_code))
            return minified_html

        content = r.text
        content = json.loads(content)
        minified_html = content.get('data').get('minified')
    except Exception as e:
        print('catch exception: {0}'.format(e))

    print(minified_html)
    return minified_html


def run():
    html_content = """<!DOCTYPE html>
<html>
<head>
<title>Error</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>An error occurred.</h1>
<p>Sorry, the page you are looking for is currently unavailable.<br/>
Please try again later.</p>
<p>If you are the system administrator of this resource then you should check
the error log for details.</p>
<p><em>Faithfully yours, nginx.</em></p>
</body>
</html>"""
    MinifyHtmlText(json.dumps(html_content))

    print("\n")

    html_url = 'http://free-phone.online/hk-phone/'
    MinifyHtmlUrl(html_url)


if __name__ == '__main__':
    run()
