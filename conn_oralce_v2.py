import cx_Oracle

import os
print 'LD_LIBRARY_PATH:%s' % os.environ['LD_LIBRARY_PATH']
#con = cx_Oracle.connect('system', 'oralce', 'your DB alias on your TNSNAMES.ORA file ')
port='1521'
host='127.0.0.1'
host='172.17.0.2'
con = cx_Oracle.connect("system", "oracle", "%s:%s/XE" % (host, port))
cur = con.cursor()
if cur.execute('select * from dual'):
    print "finally, it works!!!"
else:
    print "facepalm"
con.close()
