#!/usr/bin/python 
# -*- coding:utf-8 -*-
'''
参数解析
'''

import sys
import argparse

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('-a', action="store_true", default=False)
parser.add_argument('-b', action="store", dest="b")
parser.add_argument('-c', action="store", dest="c", type=int)
parser.add_argument('-d', nargs='+')


args =  parser.parse_args()


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "too fewer arguments,see -h option!"
    sys.exit()

  print args

