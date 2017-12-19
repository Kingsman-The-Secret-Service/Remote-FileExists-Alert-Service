import os
import sqlite3
from Constant import HostConstant

class DbHandler:
    def connectDb(self):
        return sqlite3.connect('host.db')

    def __init__(self):
        # dbExists = os.path.exists('host.db')
        conn = self.connectDb()

        conn.execute('''CREATE TABLE IF NOT EXISTS %s ''' % HostConstant.tName + '''\
                                                      (''' + HostConstant.did + ''' Integer PRIMARY KEY AUTOINCREMENT,\
                                                     ''' + HostConstant.host + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.uname + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.pwd + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.port + ''' INT,\
                                                     ''' + HostConstant.dirpath + ''' TEXT NOT NULL,\
                                                     ''' + HostConstant.fname + ''' TEXT,\
                                                      ''' + HostConstant.email + ''' TEXT,\
                                                     ''' + HostConstant.fwatch + ''' TEXT, \
                                                     ''' + HostConstant.iswatch + ''' TEXT);''')

        conn.execute('''CREATE TABLE IF NOT EXISTS %s ''' % HostConstant.mTName + '''\
                                                              (''' + HostConstant.smtp + ''' TEXT NOT NULL,\
                                                             ''' + HostConstant.smtp_port + ''' TEXT NOT NULL,\
                                                             ''' + HostConstant.email + ''' TEXT NOT NULL,\
                                                             ''' + HostConstant.pwd + ''' TEXT NOT NULL,\
                                                             ''' + HostConstant.receiver + ''' TEXT NOT NULL,\
                                                             ''' + HostConstant.sub + ''' TEXT);''')

    def saveData(self, obj):
        conn = self.connectDb()
        conn.execute("INSERT INTO "+HostConstant.tName+" VALUES (NULL,'"+obj['hostname']+"', '"+obj['username']+"', '"+obj['password']+"',"+obj['port']+",'"+obj['dir']+"','"+obj['file_name']+"','"+obj['mail']+"','"+obj['fwatcher']+"','"+obj['is_watching']+"' )")
        conn.commit()
        conn.close()

    def updateAllData(self, data,did):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+HostConstant.host+" = '"+data['hostname']+"', "+HostConstant.uname+" = '"+data['username']+"', "+HostConstant.pwd+" = '"+data['password']+"', "+HostConstant.port+" = '"+data['port']+"', "+HostConstant.dirpath+" = '"+data['dir']+"', "+HostConstant.fname+" = '"+data['file_name']+"', "+HostConstant.email+" = '"+data['mail']+"' where "+HostConstant.did+" = '"+did+"'")
        conn.commit()
        conn.close()

    def editData(self, hostValue):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+HostConstant.host+" = '"+hostValue['hostname']+"', "+HostConstant.uname+" = '"+hostValue['username']+"', "+HostConstant.pwd+" = '"+hostValue['password']+"', "+HostConstant.port+" = '"+str(hostValue['port'])+"', "+HostConstant.dirpath+" = '"+hostValue['dir']+"', "+HostConstant.fname+" = '"+hostValue['file_name']+"', "+HostConstant.email+" = '"+hostValue['mail']+"' where "+HostConstant.did+" = '"+str(hostValue['did'])+"'")
        conn.commit()
        conn.close()

    def updateData(self, column, value, did):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+column+" = '"+value+"' where  "+HostConstant.did+" = '"+did+"'")
        conn.commit()
        conn.close()

    def updateFileData(self,fileData,isWatch, host):
        conn = self.connectDb()
        conn.execute("UPDATE "+HostConstant.tName+" set "+HostConstant.fwatch+" = '"+fileData+"',"+HostConstant.iswatch+" = '"+isWatch+"' where  "+HostConstant.host+" = '"+host+"'")
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

    def selectHostDetail(self):
        conn = self.connectDb()
        cursor = conn.execute("SELECT * FROM "+HostConstant.tName)
        list = []
        for row in cursor:
            hostServer = {'did': row[0], 'hostname': row[1], 'username': row[2], 'password': row[3],'port': row[4], 'dir': row[5], 'file_name': row[6], 'mail': row[7], 'fwatch':row[8], 'iswatch':row[9]}
            list.append(hostServer)
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

    def getHostDetail(self, hostname):
        conn = self.connectDb()
        cursor = conn.execute("SELECT * FROM "+HostConstant.tName+" where "+HostConstant.host+" = '" + hostname + "'")
        datas = cursor.fetchone()
        hostServer  = {'did':datas[0], 'hostname':datas[1],'username':datas[2],'password':datas[3],'port':datas[4], 'dir':datas[5],'file_name':datas[6],'mail':datas[7], 'fwatch':datas[8], 'iswatch':datas[9]}
        return hostServer

    def selectMethod(self, did):
        conn = self.connectDb()
        cursor = conn.execute('SELECT '+HostConstant.did+','+HostConstant.host+', '+HostConstant.uname+', '+HostConstant.pwd+', '+HostConstant.port+','+HostConstant.dirpath+','+HostConstant.fname+','+HostConstant.email+' from '+HostConstant.tName +' where '+HostConstant.did+' = '+did)
        mylist = cursor.fetchone()
        dbObj = {'did': mylist[0], 'hostname': mylist[1], 'username': mylist[2], 'password': mylist[3],'port': mylist[4], 'dir': mylist[5], 'file_name': mylist[6], 'mail': mylist[7]}
        cursor.close()
        conn.close()
        return dbObj

    def readHostCountData(self):
        conn = self.connectDb()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+HostConstant.tName)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return len(result)

    def saveMailData(self,mailData):
        conn = self.connectDb()
        conn.execute("INSERT INTO "+HostConstant.mTName+" VALUES ('"+mailData['smtp']+"', '"+mailData['smtpPort']+"', '"+mailData['smtpMail'] +"','"+mailData['mailPwd']+"','"+mailData['receiver']+"','"+mailData['subject']+"' )")
        conn.commit()
        conn.close()

    def updateMailData(self, mid, data):
        conn = self.connectDb()
        conn.execute("UPDATE " + HostConstant.mTName + " set " + HostConstant.smtp + " = '" + data['smtp'] + "', " + HostConstant.smtp_port + " = '" + data['smtpPort'] + "', " + HostConstant.email + " = '" + data['smtpMail'] + "', " + HostConstant.pwd + " = '" + data['mailPwd'] + "', " + HostConstant.receiver + " = '" + data['receiver'] + "', " + HostConstant.sub + " = '" + data['subject'] + "' where "+HostConstant.email+" = '"+mid+"'")
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
        data = None
        cursor = conn.execute("SELECT "+ HostConstant.smtp +","+ HostConstant.smtp_port +","+ HostConstant.email +","+ HostConstant.pwd +","+ HostConstant.receiver +","+ HostConstant.sub +" FROM "+HostConstant.mTName)
        mylist = cursor.fetchone()
        if mylist:
            data = {'smtp':str(mylist[0]),'smtpPort': str(mylist[1]),'smtpMail': str(mylist[2]),'mailPwd': str(mylist[3]),'receiver': str(mylist[4]),'subject': str(mylist[5])}
        cursor.close()
        conn.close()
        return data