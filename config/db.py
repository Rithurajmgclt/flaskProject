import mysql.connector

condb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='2234035mgr',
    database='maindb'
)

newcursor=condb.cursor(dictionary=True, buffered=True)

