import os

import MySQLdb

LOCONOMICS_USER = os.environ["MYSQL_USER"]
LOCONOMICS_PASSWORD = os.environ["MYSQL_PASSWORD"]
LOCONOMICS_HOST = os.environ["MYSQL_HOST"] or "localhost"
LOCONOMICS_DB = os.environ["MYSQL_DATABASE"]

def get_db():
    db=MySQLdb.connect(user=LOCONOMICS_USER, passwd=LOCONOMICS_PASSWORD,host=LOCONOMICS_HOST,db=LOCONOMICS_DB)
    return db
