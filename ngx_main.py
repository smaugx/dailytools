#-*- coding:utf8 -*

import os
import redis
import pdb


def getlog(path = ""):
  logpaths = []
  if not os.path.exists(path):
    return  logpaths

  for f in os.listdir(path):
    log = os.path.join(path,f)
    if os.path.isdir(log):
      for sf in os.listdir(log):
        slog = os.path.join(log,sf)
        logpaths.append(slog)

  return logpaths


def run(filename = ""):
  if not os.path.exists(filename):
    return 

  spool = redis.ConnectionPool(host='127.0.0.1', port=9579)
  sr = redis.StrictRedis(connection_pool = spool)



if __name__ == "__main__":
  logpaths = getlog('/disk/ssd1/ngx/donev2')
  print len(logpaths)
  print logpaths[-1]
