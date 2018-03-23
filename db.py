import os

import MySQLdb

LOCONOMICS_USER = "root"
LOCONOMICS_PASSWORD = ""
LOCONOMICS_HOST = os.environ["DB_HOST"] or "localhost"
LOCONOMICS_DB = 'loco_sales'

def get_db():
    db=MySQLdb.connect(user=LOCONOMICS_USER, passwd=LOCONOMICS_PASSWORD,host=LOCONOMICS_HOST,db=LOCONOMICS_DB)
    return db
