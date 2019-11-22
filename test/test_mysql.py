#!/usr/bin/python3
# -*- coding: utf-8 -*-
 
import pymysql
 
con = pymysql.connect('localhost', 'user', 'nEvMqSM9', 'i360')
 
with con:
    
    cur = con.cursor()
    cur.execute("SELECT VERSION()")
 
    version = cur.fetchone()
    
    print("Database version: {}".format(version[0]))