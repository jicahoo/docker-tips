import datetime
import mysql.connector

host='172.17.0.3'
cnx = mysql.connector.connect(user='root', password='123456',
                              host=host,
                              database='meters')
cursor = cnx.cursor()

query = ("SELECT name FROM temp")


cursor.execute(query)

for x in cursor:
    print x
cursor.close()
cnx.close()
