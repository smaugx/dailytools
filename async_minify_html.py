#!/usr/bin/env python
#-*- coding:utf8 -*-

import asyncio
import aiohttp
import json
import os
import time
import uvloop
import random


async def MinifyHtmlUrl(async_session, html_url):
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
        async with async_session.get(url,  headers = myheaders) as r:
            if r.status != 200:
                print('http get request failed with code:{0}'.format(r.status))
                return minified_html

            content = await r.text()
            content = json.loads(content)
            minified_html = content.get('data').get('minified')
    except Exception as e:
        print('catch exception: {0}'.format(e))

    return minified_html




async def MinifyHtmlText(async_session, html_content):
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
            'json': json.dumps(html_content),
            }
    minified_html = ''
    try:
        async with async_session.post(url,  headers = myheaders, data = payload) as r:
            if r.status != 200:
                print('http get request failed with code:{0}'.format(r.status))
                return minified_html

            content = await r.text()
            content = json.loads(content)
            minified_html = content.get('data').get('minified')
    except Exception as e:
        print('catch exception: {0}'.format(e))

    return minified_html

async def dump_minify_html(minified_html, dest_file):
    with open(dest_file, 'w') as destF:
        destF.write(minified_html)
    return

async def MinifyHtmlTextDir(async_session, src_dir, dest_dir):
    for item in os.listdir(src_dir):
        abs_item  = os.path.join(src_dir, item)
        new_abs_item = os.path.join(dest_dir, item)
        if os.path.isdir(abs_item):
            if not os.path.exists(new_abs_item):
                os.makedirs(new_abs_item)
            await MinifyHtmlTextDir(async_session, abs_item, new_abs_item)
        else:
            if not item.endswith('.html'):
                continue
            html_content = ''
            with open(abs_item, 'r') as srcF:
                html_content = srcF.read()

            minified_html = await MinifyHtmlText(async_session, html_content)
            if not minified_html:
                print("#################################### html: {0} minify failed".format(abs_item))
            else:
                print("html: {0} minify success".format(abs_item))
                await dump_minify_html(minified_html, new_abs_item)

    print("minify-html all done")
    return



async def run_test():
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, enable_cleanup_closed = True),
            timeout=aiohttp.ClientTimeout(total=60)) as async_session:
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
        await MinifyHtmlText(async_session, json.dumps(html_content))

        print("\n")

        html_url = 'http://free-phone.online/hk-phone/'
        await MinifyHtmlUrl(async_session, html_url)


async def run():
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False, enable_cleanup_closed = True),
            timeout=aiohttp.ClientTimeout(total=60)) as async_session:
        src_dir = "./website_src/sms1"
        dest_dir = "./website_src/sms1"
        await MinifyHtmlTextDir(async_session, src_dir, dest_dir)



if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
