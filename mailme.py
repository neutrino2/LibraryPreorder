#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        mailme
# Purpose:
#
# Author:      Neutrino21
#
# Created:     22-11-2013
# Copyright:   (c) Neutrino21 2013
#-------------------------------------------------------------------------------

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from email.utils import COMMASPACE,formatdate
from email import encoders

import os

#server['name'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]):

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = subject
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(text))

    for file in files:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload( open(file,"rb").read() )
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file))
        msg.attach(part)

    import smtplib
    smtp = smtplib.SMTP(server['name'])
    smtp.login(server['user'], server['passwd'])
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


def mailme(text,email):
    server={}
    server['name'] = ''#smtp 服务器地址
    server['user'] = '' # 用户名
    server['passwd'] = '' # 密码
    fro = '' # 发件人
    to = [email]
    subject = "订阅的图书已到"
    files = []
    send_mail(server, fro, to, subject, text, files)