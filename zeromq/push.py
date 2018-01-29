#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import time
context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.bind('ipc://5566.ipc')
i = 0
while True:
    i += 1
    print(i)
    socket.send(str(i))
    #time.sleep(1)
