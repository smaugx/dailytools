#!/usr/bin/env python
# -*- coding:utf-8 -*-

import yagmail

def send_mail(user,password,host,port):
  yag = yagmail.SMTP(user, password, host, port)
  yag.send(user, subject = "I now can send an attachment", attachments=['a.txt', 'b.jpg'])


if __name__ == "__main__":
  user = "xxx@upai.com"
  password = "password"
  host = "smtp.gmail.com"
  port = 465

  host = "imap.gmail.com"
  port = 993 
  send_mail(user,password,host,port)

