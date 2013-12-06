#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     22-11-2013
# Copyright:   (c) Administrator 2013
#-------------------------------------------------------------------------------
import urllib2
import re

class BookInfo:

    def __init__(self,marc_no):
        if len(marc_no) == 10:
            self.url = "http://210.45.242.5:8080/opac/item.php?marc_no=" + marc_no
        elif marc_no.find("http") == 0:
            self.url = marc_no
        else:
            self.url = None
        self.result = []
        self.locates = []
        self.bookname = ""

    def getBookAvail(self,locate):
        if not self.result:
            self.FetchWebPage()
        if type(locate)==type(0):
            if not self.locates:
                self.getLocates()
            locate = self.locates[locate]
        for book in self.result:
            if book[1] == locate and book[2] == u"可借":
                return book
        return None

    def getLocates(self):
        if not self.result:
            self.FetchWebPage()
        if not self.locates:
            l=set()
            for book in self.result:
                l.add(book[1])
            self.locates = list(l)
        return self.locates

    def FetchWebPage(self):
        if not self.url:
            return
        findstr = "<td >索书号</td>"

        re_td = re.compile("<td.+?>(?:<.+?>)?(.*?)(?:</\w+>||\s)?</td>")
        html=urllib2.urlopen(self.url).read()

        temp = html.find(findstr)
        if temp == -1:
            return
        inb = html.find("\"",len(html)-300)
        ine = html.find("\"",inb+1)
        self.bookname = html[inb+1:ine].decode("utf8")

        idxBegin =html.find("<tr",temp)
        idxEnd =html.find("</table>",idxBegin)

        parsePart=html[idxBegin:idxEnd].decode('utf8')

        scaner = re_td.scanner(parsePart)
        match = scaner.search()
        self.result=[]
        while match:
            temp=[]
            for i in xrange(6):
                if i==0 or i==3 or i==4:
                    temp.append(match.groups()[0])
                match = scaner.search()
            self.result.append(temp)