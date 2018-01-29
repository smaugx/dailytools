#!/usr/bin/env python
#-*- coding:utf8 -*-

import os
import sys
import copy
import json

ksjsonfile = './kuaishou.json'
#marcofile = './marco.json'


CONFIG = {} 
#str of json
#STORE = json.dumps(CONFIG,indent = 4)

def create_template(jsonfile):
  global CONFIG
  if os.path.isfile(jsonfile):
    with open(jsonfile) as confile:
      CONFIG = json.load(confile)


def padding_template():
  if not CONFIG:
    return

  item = copy.deepcopy(CONFIG)
  for i in item:
    item[i] = 'test'

  return item


def main():
  create_template(ksjsonfile)
  item = padding_template()
  js_item = json.dumps(item,indent = 4)
  print js_item 


def marco_main():
  create_template(marcofile)
  marco = json.dumps(CONFIG,indent = 4)
  with open('./marcomode.json','w') as of:
    of.write(marco)
    


#marco_main()
