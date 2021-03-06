class DataObj(object):
    def __init__(self, did, host, uname, pwd, port, dpath, fname, email, fwatch):
        self._did = did
        self._host = host
        self._uname = uname
        self._pwd = pwd
        self._port = port
        self._dpath = dpath
        self._fname = fname
        self._email = email
        self._fwatch = fwatch

    def getDid(self):
        return self._did

    def setDid(self, idValue):
        self._did = idValue

    def getHost(self):
        return self._host

    def setHost(self, host):
        self._host = host

    def getUname(self):
        return self._uname

    def setUname(self, uname):
        self._uname = uname

    def getPwd(self):
        return self._pwd

    def setPwd(self, pwd):
        self._pwd = pwd

    def getPort(self):
        return self._port

    def setPort(self, port):
        self._port = port

    def getDpath(self):
        return self._dpath

    def setDpath(self, dpath):
        self._dpath = dpath

    def getFname(self):
        return self._fname

    def setFname(self, fname):
        self._fname = fname

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getFwatch(self):
        return self._fwatch

    def setFwatch(self, fwatch):
        self._fwatch = fwatch

class MailData:
    def __init__(self, smtp, port, email, pwd, receiver, sub):
        self._smpt = smtp
        self._port = port
        self._email = email
        self._pwd = pwd
        self._receiver = receiver
        self._sub = sub

    def getSmtp(self):
        return self._smpt

    def getSmtpPort(self):
        return self._port

    def getEmail(self):
        return self._email

    def getPwd(self):
        return self._pwd

    def getReceiver(self):
        return self._receiver

    def getSub(self):
        return self._sub