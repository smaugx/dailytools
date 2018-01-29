#!/usr/bin/env  python
# -*- coding:utf-8 -*-

import os

def count_each_softirq(line):
  sumcpu = 0.0
  for c in line[1:]:
    sumcpu += float(c)
  return sumcpu


def get_total_softirq():
  cmd = 'cat /proc/softirqs'
  lines = os.popen(cmd).readlines()
  if len(lines) == 1 : 
    return 

  SOFTNUM = {}
  sumcpu = 0.0

  for line in lines[1:]:
    line = line.split()
    sumcpu = count_each_softirq(line)
    key = line[0][:-1]
    SOFTNUM[key] = sumcpu

  print SOFTNUM 
  return SOFTNUM

get_total_softirq()

