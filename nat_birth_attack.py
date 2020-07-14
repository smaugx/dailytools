#!/usr/bin/env python
#-*- coding:utf8 -*-


import os
import math
from decimal import *

getcontext().prec = 6

def birthday_attack(total, rate):
    k = 0
    while True:
        k += 1
        a,t = 1,1
        for i in range(k):
            a = a * (total - i)
            t = t *  total

        np = Decimal(a) / Decimal(t)
        p = 1 - np
        if p > rate:
            print('p: {0} > rate:{1} k: {2} success'.format(p, rate, k))
            break
        else:
            #print('p: {0} < rate:{1} failed, continue...'.format(p, rate))
            continue

    return k



if __name__ == '__main__':
    total_samples = 365
    rate = 0.5
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok\n".format(total_samples, rate, min_k))


    total_samples = 65536
    rate = 0.5
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok\n".format(total_samples, rate, min_k))


    total_samples = 65536
    rate = 0.7
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok\n".format(total_samples, rate, min_k))


    total_samples = 65536
    rate = 0.8
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok\n".format(total_samples, rate, min_k))


    total_samples = 65536
    rate = 0.9
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok\n".format(total_samples, rate, min_k))


    total_samples = 65536 - 1024
    rate = 0.99
    min_k =  birthday_attack(total_samples, rate)
    print("when total_samples is {0}, if request for rate greater than {1}, then try at least {2} times is ok".format(total_samples, rate, min_k))


