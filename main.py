#!/usr/bin/env python
# -*- coding: gbk -*-
#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      Neutrino21
#
# Created:     22-11-2013
# Copyright:   (c) Neutrino21 2013
#-------------------------------------------------------------------------------


#import urllib2
import time
import pickle
import bookinfo
import marshal
from mailme import mailme

def readFile():
    slist=[]
    try:
        with open("db",'rb') as f:
            slist=marshal.load(f)
    except IOError:
        pass
    return slist

def writeFile(slist):
    try:
        with open("db",'wb') as f:
            marshal.dump(slist,f)
    except IOError:
        pass

def insertFile(newlist):
    try:
        sublist=readFile()
        sublist.append(newlist)
        with open("db",'wb') as f:
            marshal.dump(sublist,f)
    except IOError:
        pass

def newSubscription():
    marcNo=raw_input("marcNo:")
    book = bookinfo.BookInfo(marcNo)
    lcls = book.getLocates()
    if not lcls:
        print "û���ҵ��Ȿ��"
        return
    else:
        bookname = book.bookname.encode("GBK")
        print "�ҵ���Ŀ��%s" % bookname
    print "ѡ����ĵص㣺"
    i=0
    for lc in lcls:
        print "%d %s" % (i,lc)
        i+=1
    n=raw_input("No:")
    n=int(n)
    while n<0 or n>=i:
        print "��Ŵ���"
        n=raw_input("No:")
        n=int(n)
    locate = lcls[n]
    email=raw_input("Email:")
    email2=raw_input("Again:")
    while email != email2:
        print "���β���"
        email=raw_input("Email:")
        email2=raw_input("Again:")
    insertFile([marcNo,book.bookname,locate,email])
    print "���ĳɹ�"

def scan():
##
    with open("log.txt","a") as log:
        log.write(time.asctime())
        log.write('\n')
##
    hour=time.localtime().tm_hour
    if hour < 8 or hour > 18:
        exit(0)

    sublist=readFile()
    delItem=[]
    for marcNo,bookname,locate,email in sublist:
        book = bookinfo.BookInfo(marcNo)
        info = book.getBookAvail(locate)
		time.sleep(1)

        if info:
            text = u"�����ĵ�ͼ��\"%s\"����������1���ڹݣ��ٶȽ���\n\n%s  %s  %s" % (bookname,info[0],info[1],info[2])
            text = text.encode('utf8')
            mailme(text,email)
            delItem.append(marcNo)
    sublist = [i for i in sublist if i[0] not in delItem]
    writeFile(sublist)

def show():
    sublist=readFile()
    print "���� %d ��������Ϣ��" % len(sublist)
    for marcNo,bookname,locate,email in sublist:
        print "%s %s %s" % (bookname,locate,email)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        arg=sys.argv[1]
    else:
        arg=""
    #arg = "new"
    if arg == "scan":
        scan()
    elif arg == "new":
        newSubscription()
    else:
        show()
        print "scan ����������Ŀ new �����µĶ���"