import sqlite3
from Constant import HostConstant
from Obj import DataObj

class DbHandler:
    def __init__(self):
        conn = self.connectDb()
        conn.execute('''CREATE TABLE IF NOT EXISTS %s ''' % HostConstant.tName + '''\
                                          (''' + HostConstant.did + ''' Integer PRIMARY KEY AUTOINCREMENT,\
                                         ''' + HostConstant.host + ''' TEXT NOT NULL,\
                                         ''' + HostConstant.uname + ''' TEXT NOT NULL,\
                                         ''' + HostConstant.pwd + ''' TEXT NOT NULL,\
                                         ''' + HostConstant.port + ''' INT,\
                                         ''' + HostConstant.dirpath + ''' TEXT NOT NULL,\
                                         ''' + HostConstant.fname + ''' TEXT,\
                                         ''' + HostConstant.email + ''' TEXT);''')
    def connectDb(self):
        return sqlite3.connect('host.db')
    # host, uname, pwd, port, dpath, fname, email
    def saveData(self, obj):
        conn = self.connectDb()
        conn.execute("INSERT INTO "+HostConstant.tName+" VALUES (NULL,'"+obj.getHost()+"', '"+obj.getUname()+"', '"+obj.getPwd()+"',"+obj.getPort()+",'"+obj.getDpath()+"','"+obj.getFname()+"','"+obj.getEmail()+"' )")
        conn.commit()
        conn.close()

    def updateAllData(self, host, uname,pwd, port, dpath,fname, email,did):
        conn = self.connectDb()
        conn.execute("UPDATE '"+HostConstant.tName+"' set '"+HostConstant.host+"' = '"+host+"', '"+HostConstant.uname+"'='"+uname+"', '"+HostConstant.pwd+"' = '"+pwd+"', '"+HostConstant.port+"' = '"+port+"', '"+HostConstant.dirpath+"' = '"+dpath+"', '"+HostConstant.fname+"' = '"+fname+"', '"+HostConstant.email+"' = '"+email+"' where '"+HostConstant.did+"' = '"+did+"'")
        conn.commit()
        conn.close()

    def updateData(self, column, value, did):
        conn = self.connectDb()
        conn.execute("UPDATE '"+HostConstant.tName+"' set '"+column+"' = '"+value+"' where  '"+HostConstant.did+"' = '"+did+"'")
        conn.commit()
        conn.close()

    def deleteData(self, did):
        conn = self.connectDb()
        conn.execute("DELETE from "+HostConstant.tName+" where  "+HostConstant.did+" = "+str(did)+";")
        conn.commit()
        conn.close()

    def selectQueryMethod(self):
        conn = self.connectDb()
        list = []
        cursor = conn.execute('SELECT '+HostConstant.did+', '+HostConstant.host+', '+HostConstant.uname+', '+HostConstant.pwd+', '+HostConstant.port+','+HostConstant.dirpath+','+HostConstant.fname+','+HostConstant.email+' from '+HostConstant.tName)
        for row in cursor:
            dbObj = DataObj(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            list.append(dbObj)
        cursor.close()
        conn.close()
        return list

    def selectMethod(self, did):
        conn = self.connectDb()
        dbObj = None
        cursor = conn.execute('SELECT '+HostConstant.host+', '+HostConstant.uname+', '+HostConstant.pwd+', '+HostConstant.port+','+HostConstant.dirpath+','+HostConstant.fname+','+HostConstant.email+' from '+HostConstant.tName +' where '+HostConstant.did+' = '+did)
        for row in cursor:
            dbObj = DataObj(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        cursor.close()
        conn.close()
        return dbObj