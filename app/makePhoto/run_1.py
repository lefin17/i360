APP = "/home/lefin/work/i360/"

import sys
import os

sys.path.append(os.path.abspath(APP + "classes"))
# from photo_service import *
from mysql_connect import *
import json
# import pymysql.cursors
WORKPLACE = 'NOTE-1'

def first_run():
    options = json.dumps({'cameras': 1, 'hdr': 0, 'step':50, 'steps': 10})
    query = "INSERT INTO `i360_roadmap` (`i360_roadmap_created_at`, `i360_roadmap_command`, `i360_roadmap_options`, `i360_roadmap_workplace`) VALUES (NOW(), 'photo', %s, %s)";
    cur.execute(query, (options, WORKPLACE))
    con.commit()


con, cur = connect_mysql()
first_run()

cur.close()
con.close()