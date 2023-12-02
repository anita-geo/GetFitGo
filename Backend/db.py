import pymysql
from flask import g

def get_db():
        if 'db' not in g:
                g.connection = pymysql.connect(
                                        host = 'localhost',
                                        user = 'root',
                                        password = 'password',
                                        database = 'getFitGo',
                                        autocommit=True)
        return g.connection
        
    