#!/usr/bin/env python3
import os
import sys
import pymysql
import warnings

warnings.filterwarnings(action='ignore')

character = sys.argv[1]
date = sys.argv[2]

hostname = 'db.hostname.com'
user = 'id'
password = 'pw'
db_name = 'db'

connection = pymysql.connect(host=hostname,
                             user=user,
                             password=password,
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = f'''UPDATE `Sword`.`Summon` SET `Face` = {character}, `Date` = {date} WHERE (`Num` = '1');'''
        cursor.execute(sql)
        result = cursor.fetchall()
finally:
    connection.close()