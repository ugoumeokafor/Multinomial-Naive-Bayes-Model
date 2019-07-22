######################################################
#this script provides conn services for other scripts.
######################################################

import psycopg2
__author__ ="ugo"


class postgres():
    def __init__(self,host='localhost',database='postgres',schema='francis',user='postgres',passwd='***'):
        self.host = host
        self.database = database
        self.schema = schema
        self.user = user
        self.passwd = passwd
        self.conn=None
        self.cur=None

    def connect(self):
        try:
            self.conn = psycopg2.connect(host=self.host,database=self.database,user=self.user,password=self.passwd)
            self.cur = self.conn.cursor()
        except Exception as err:
            print "---------->error happened at opening geolife database"
            print err.message

    def execute(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
    def executemany(self,sql,dict):
        self.cur.executemany(sql,dict)
        self.conn.commit()
    def select(self,sql):
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        if rows==[] or rows==[()]:
            rows=None
        elif rows[0].__len__()==1:
            rows = map(lambda x:x[0],rows)
        else:
            pass
        return rows

    def del_conn(self):
        if self.cur:
            del self.cur
        if self.conn:
            self.conn.close()
