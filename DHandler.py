import os
import sqlite3
from Constant import HostConstant
from Obj import DataObj, MailData

class DbHandler:
    def connectDb(self):
        return sqlite3.connect('host.db')

    def __init__(self):
        dbExists = os.path.exists('host.db')
        conn = self.connectDb()

        if not dbExists:
            conn.execute('''CREATE TABLE IF NOT EXISTS %s ''' % HostConstant.tName + '''\
                                              (''' + HostConstant.did + ''' Integer PRIMARY KEY AUTOINCREMENT,\
                                             ''' + HostConstant.host + ''' TEXT NOT NULL,\
                                             ''' + HostConstant.uname + ''' TEXT NOT NULL,\
                                             ''' + HostConstant.pwd + ''' TEXT NOT NULL,\
                                             ''' + HostConstant.port + ''' INT,\
                                             ''' + HostConstant.dirpath + ''' TEXT NOT NULL,\
                                             ''' + HostConstant.fname + ''' TEXT,\
                                              ''' + HostConstant.email + ''' TEXT,\
                                             ''' + HostConstant.fwatch + ''' TEXT);''')

            conn.execute('''CREATE TABLE IF NOT EXISTS %s ''' % HostConstant.mTName + '''\
                                                      (''' + HostConstant.smtp + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.smtp_port + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.email + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.pwd + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.receiver + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.sub + ''' TEXT);''')

    def saveData(self, obj):
        conn = self.connectDb()
        conn.execute("INSERT INTO "+HostConstant.tName+" VALUES (NULL,'"+obj['hostname']+"', '"+obj['username']+"', '"+obj['password']+"',"+obj['port']+",'"+obj['dir']+"','"+obj['file_name']+"','"+obj['mail']+"','"+obj['fwatcher']+"' )")
        conn.commit()
        conn.close()

    def updateAllData(self, host, uname,pwd, port, dpath,fname, email,did):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+HostConstant.host+" = '"+host+"', "+HostConstant.uname+" = '"+uname+"', "+HostConstant.pwd+" = '"+pwd+"', "+HostConstant.port+" = '"+port+"', "+HostConstant.dirpath+" = '"+dpath+"', "+HostConstant.fname+" = '"+fname+"', "+HostConstant.email+" = '"+email+"' where "+HostConstant.did+" = '"+did+"'")
        conn.commit()
        conn.close()

    def updateData(self, column, value, did):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+column+" = '"+value+"' where  "+HostConstant.did+" = '"+did+"'")
        conn.commit()
        conn.close()

    def updateFileData(self,fileData, host):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+HostConstant.fwatch+" = '"+fileData+"' where  "+HostConstant.host+" = '"+host+"'")
        conn.commit()
        conn.close()

    def readFileData(self,host):
        conn = self.connectDb()
        cursor = conn.execute("SELECT " + HostConstant.fwatch +" FROM "+ HostConstant.tName+ " WHERE " + HostConstant.host + " = '" + host + "'")
        mylist = cursor.fetchone()
        myFS = mylist[0]
        cursor.close()
        conn.close()
        return myFS

    def deleteData(self, did):
        conn = self.connectDb()
        conn.execute("DELETE from "+HostConstant.tName+" where  "+HostConstant.did+" = "+str(did)+";")
        conn.commit()
        conn.close()

    def deleteHostData(self, host):
        conn = self.connectDb()
        conn.execute("DELETE from "+HostConstant.tName+" where  "+HostConstant.host+" = '"+ host +"'")
        conn.commit()
        conn.close()

    def selectQueryMethod(self):
        conn = self.connectDb()
        list = []
        cursor = conn.execute('SELECT '+HostConstant.did+', '+HostConstant.host+', '+HostConstant.uname+', '+HostConstant.pwd+', '+HostConstant.port+','+HostConstant.dirpath+','+HostConstant.fname+','+HostConstant.email+' from '+HostConstant.tName)
        for row in cursor:
            dbObj = DataObj(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7],'')
            list.append(dbObj)
        cursor.close()
        conn.close()
        return list

    def getServerGrouped(self):
        conn = self.connectDb()
        cursor = conn.execute("SELECT "+HostConstant.host+", count("+HostConstant.host+") as count FROM "+HostConstant.tName+" group by "+HostConstant.host+"")
        groups = cursor.fetchall()
        serverGroupedData = {}
        for group in groups:
            serverGroupedData[group[0]] = {}
            serverGroupedData[group[0]]['list'] = self.getSeverByGroup(group[0])
            serverGroupedData[group[0]]['count'] = group[1]
        return serverGroupedData

    def getSeverByGroup(self, hostname):
        conn = self.connectDb()
        cursor = conn.execute("SELECT * FROM "+HostConstant.tName+" where "+HostConstant.host+" = '" + hostname + "'")
        return cursor.fetchall()

    def selectMethod(self, did):
        conn = self.connectDb()
        cursor = conn.execute('SELECT '+HostConstant.did+','+HostConstant.host+', '+HostConstant.uname+', '+HostConstant.pwd+', '+HostConstant.port+','+HostConstant.dirpath+','+HostConstant.fname+','+HostConstant.email+' from '+HostConstant.tName +' where '+HostConstant.did+' = '+did)
        mylist = cursor.fetchone()
        dbObj = DataObj(mylist[0],mylist[1],mylist[2],str(mylist[3]),str(mylist[4]),mylist[5],mylist[6],mylist[7],'')
        cursor.close()
        conn.close()
        return dbObj

    def saveMailData(self, smtp, port, email, pwd, receiver, sub):
        conn = self.connectDb()
        conn.execute("INSERT INTO "+HostConstant.mTName+" VALUES ('"+smtp+"', '"+port+"', '"+email +"','"+pwd+"','"+receiver+"','"+sub+"' )")
        conn.commit()
        conn.close()

    def updateMailData(self, mid, smtp, port, email, pwd, receiver, sub):
        conn = self.connectDb()
        print("UPDATE " + HostConstant.mTName + " set " + HostConstant.smtp + " = '" + smtp + "', " + HostConstant.smtp_port + " = '" + port + "', " + HostConstant.email + " = '" + email + "', " + HostConstant.pwd + " = '" + pwd + "', " + HostConstant.receiver + " = '" + receiver + "', " + HostConstant.sub + " = '" + sub + "' where " + HostConstant.email + " = " + mid+"'")
        conn.execute("UPDATE " + HostConstant.mTName + " set " + HostConstant.smtp + " = '" + smtp + "', " + HostConstant.smtp_port + " = '" + port + "', " + HostConstant.email + " = '" + email + "', " + HostConstant.pwd + " = '" + pwd + "', " + HostConstant.receiver + " = '" + receiver + "', " + HostConstant.sub + " = '" + sub + "' where "+HostConstant.email+" = '"+mid+"'")
        conn.commit()
        conn.close()

    def readMailCountData(self):
        conn = self.connectDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+HostConstant.mTName)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return len(result)

    def readMailData(self):
        conn = self.connectDb()
        mObj = None
        cursor = conn.execute("SELECT "+ HostConstant.smtp +","+ HostConstant.smtp_port +","+ HostConstant.email +","+ HostConstant.pwd +","+ HostConstant.receiver +","+ HostConstant.sub +" FROM "+HostConstant.mTName)
        mylist = cursor.fetchone()
        mObj = MailData(str(mylist[0]), str(mylist[1]), str(mylist[2]), str(mylist[3]), str(mylist[4]), str(mylist[5]))
        cursor.close()
        conn.close()
        return mObj