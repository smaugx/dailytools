#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect('ipc://5566.ipc')
while True:
    print(socket.recv())
