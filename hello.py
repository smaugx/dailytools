#!/usr/bin/env python
#-*- coding:utf8 -*-
#给杨晓琴的例子


import os
import sys

#打印 hello world
def hello():
  print "hello world"



#往文件里写100行 hello world
def dumphello(filename):
  #打开文件，写
  with open(filename,'w') as hellofile:
    for i in xrange(0,100,1):
      hellofile.write("hello world\n")

    hellofile.close()


#打印一个等差数列 1,2,3,4,5,,,
def dengcha123():
  i = 1
  for i in xrange(100):
    print i 
    i += 1


#打印一个斐波那契数列 0,1,1,2,3,5,8,13,21,,,
def feibo():
  result = []
  a,b = 0,1
  for i in xrange(10):
    result.append(a)
    #result.append(b)
    aa = a
    bb = b
    a = bb
    b = aa + bb
  print result


#主函数(main)
if __name__ == "__main__":
  print "call hello()"
  hello()
  print "finish call hello()"


  print "call dumphello()"
  filename = "./abc.txt"
  dumphello(filename)
  print "finish call dumphello()"
  
  #dengcha123()
  feibo()

    
    

