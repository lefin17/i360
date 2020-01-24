import pymysql

DB_NAME = "i360"
DB_HOST = "localhost"
DB_PASS = "nEvMqSM9"
DB_USER = "user"

con = None
cur = None

def connect_mysql():
    global con, cur
    con = pymysql.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME)
    with con:
        cur = con.cursor()
    return con, cur    
#    print (cur)
#    print (con)
