#!/usr/bin/env python
#-*- coding:utf8 -*-
import os


def getlog(path = ""):
  logpaths = []
  if not os.path.exists(path):
    return  logpaths

  for f in os.listdir(path):
    if f.endswith('a') or f.endswith('b'):
      log = os.path.join(path,f)
      logpaths.append(log)

  return logpaths

def splitfile(filepath,linesize=3000):
    partfilelist = []
    filedir,name = os.path.split(filepath)
    name,ext = os.path.splitext(name)
    filedir = os.path.join(filedir,name)
    if not os.path.exists(filedir):
        os.mkdir(filedir)

    partno = 0
    #stream = open(filepath,'r', encoding='utf-8')
    stream = open(filepath,'r')
    while True:
        partfilename = os.path.join(filedir,name + '_' + str(partno) + ext)
        print('write start %s' % partfilename)
        #part_stream = open(partfilename,'w', encoding='utf-8')
        part_stream = open(partfilename,'w')
        partfilelist.append(partfilename)

        read_count = 0
        while read_count < linesize:
            read_content = stream.readline()
            if read_content:
                #part_stream.write(read_content)
                None
            else:
                break
            read_count += 1

        part_stream.close()
        if(read_count < linesize) :
            break
        partno += 1

    print('done')
    return partfilelist

def getfinal(logpaths = []):
  splogpaths = []
  if not logpaths:
    return splogpaths

  for p in logpaths:
    partfilelist = splitfile(p,500000)
    splogpaths.extend(partfilelist)

  return splogpaths



if __name__ == "__main__":
  logpaths = getlog('/disk/ssd1/ngx/donev2')
  splogpaths = getfinal(logpaths)
  print splogpaths
  print  len(splogpaths)
