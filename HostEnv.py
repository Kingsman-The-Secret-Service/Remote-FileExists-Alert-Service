import os, json
import JsonFile
from DHandler import DbHandler

class ServerEnvironment():
    def __init__(self):
        # super(ServerEnvironment, self).__init__()
        self.ipAddress = ''
        self.username = ''
        self.password = ''
        self.port = ''
        self.dir_path = ''
        self.filename = ''
        self.email = ''

    def addServer(self, ipAddress, username, password, port, dir_path, filename, email):
        self.ipAddress = ipAddress
        self.username = username
        self.password = password
        self.port = port
        self.dir_path = dir_path
        self.filename = filename
        self.email = email

    def createJsonFile(self):
        datas = {
            "ip_address": self.ipAddress,
            "username": self.username,
            "password": self.password,
            "port": self.port,
            "dir_path": self.dir_path,
            "file_name": self.filename,
            "email":self.email
        }
        a = {}
        a['host'] = []
        if os.path.isfile('test.json'):
            if not os.stat("test.json").st_size == 0:
                config = json.loads(open('test.json').read())
                config['host'].append(datas)
                JsonFile.writeJson(config)
        else:
            a['host'].append(datas)
            JsonFile.writeJson(a)

    def removeHostServer(self, obj, index):
        try:
            obj.deleteData(index)
            # data = JsonFile.readJson()
            # del data['host'][index]
            # JsonFile.writeJson(data)
            print 'Succesfully removed host.\n'
        except (IndexError, IOError):
            print 'Host not found'