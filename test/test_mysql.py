#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os 
import pymysql
# import pymysql.cursor
 
for i in sys.path:
    print (i)

con = pymysql.connect('localhost', 'user', 'nEvMqSM9', 'i360')
 
with con:
    
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
 
    version = cur.fetchone()
    
    print("Database version: {}".format(version[0]))
    cur.close()
    
con.close()    