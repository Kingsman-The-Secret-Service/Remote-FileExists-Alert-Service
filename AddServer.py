import json
import os.path
import threading
import paramiko
import smtplib
import JsonFile
import Validations

class ServerEnvironment:
    def __init__(self):
        self.ipAddress = ''
        self.username = ''
        self.password=''
        self.port = ''

    def addServer(self, ipAddress, username, password, port):
        self.ipAddress = ipAddress
        self.username = username
        self.password = password
        self.port = port

    def createJsonFile(self):
        datas = {
            "ip_address": self.ipAddress,
            "username": self.username,
            "password": self.password,
            "port": self.port
        }
        a = {}
        a['host'] = []
        if os.path.isfile('test.json'):
            if not os.stat("test.json").st_size == 0:
                config = json.loads(open('test.json').read())
                config['host'].append(datas)
                with open('test.json', 'w') as f:
                    json.dump(config, f)
        else:
            a['host'].append(datas)
            with open('test.json', 'w') as f:
                json.dump(a, f)

    def removeHostServer(self, index):
        try:
            data = JsonFile.readJson()
            del data['host'][index]
            JsonFile.writeJson(data)
        except IndexError, IOError:
            print 'Host not found'

class SSHClient:
    def mailAler(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('dummy.letsmeditate@gmail.com', 'lets@2858')
        msg = "\nFile Created!"  # Thdummy.letsmeditate@gmail.come /n separates the message from the headers (which we ignore for this example)
        server.sendmail("dummy.letsmeditate@gmail.com", "akkravikumar@gmail.com", msg)

    def connect_host(self, server, username, password, port):
            server, username, password = (server, username, password)
            ssh = paramiko.SSHClient()
            paramiko.util.log_to_file("ssh.log")
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server, username=username, password=password)
            sftp = ssh.open_sftp()
            try:
                list = sftp.listdir("/home/anji/sample")
                if not list == []:
                    self.mailAler()
                else:
                    print 'No files in this directory.'
                for element in list:
                    print '=', element
            except IOError as e:
                print e
            finally:
                # threading.Timer(10.0, self.connect_host, args=(server, username, password, port,)).start()
                sftp.close()
                ssh.close()


class Switcher(ServerEnvironment, SSHClient):
    def numbers_to_options(self, argument):
        if int(argument) == 1:
            method_name = 'addHost'
        elif int(argument) == 2:
            method_name = 'removeHost'
        elif int(argument) == 3:
            method_name = 'runHost'
        elif int(argument) == 4:
            method_name = 'editHostConfiguration'
        elif int(argument) == 5:
            method_name = 'viewHost'
        else:
            print 'No options found'
            return

        method = getattr(self, method_name, lambda: "Invalid Options")
        return method()

    def addHost(self): #Add Host
        ipAddress = raw_input("Enter the host: ")
        while not Validations.checkValidIp(ipAddress):
            ipAddress = raw_input("Enter the valid ip address: ")
        userName = raw_input("Enter userName: ")
        while not Validations.checkIsEmpty(userName):
            userName = raw_input("Please enter the username: ")
        password = raw_input("Enter password: ")
        while not Validations.checkIsEmpty(password):
            password = raw_input('Please enter the password: ')
        port = raw_input("Enter port: ")
        if not port:
            port = '22'
        self.addServer(ipAddress, userName, password, port)
        self.createJsonFile()

    def removeHost(self): #Remove host
        try:
            jsonFile = open('test.json', 'r')
            conn_string = json.load(jsonFile)
            listsHost= []
            if conn_string['host'] ==[]:
                print 'No IP Address found, try Again'
                return
            print '---------------------'
            for index,element in enumerate(conn_string['host']):
                print '(',index+1, ').', element['ip_address']
                listsHost.append(str(element['ip_address']))
            print '---------------------'
            host = raw_input('Enter the host to remove: ')
            while not Validations.checkIsInteger(host):
                host = raw_input("Enter the host to remove: ")
            self.removeHostServer(int(host) - 1)
        except IOError, IndexError:
            print 'Hosts not found'

    def runHost(self):
        try:
            conn_string = JsonFile.readJson()
            if not conn_string or conn_string['host'] ==[]:
                print 'No IP Address found, try Again'
                return
            print '---------------------'
            for index,element in enumerate(conn_string['host']):
                print '(',index+1, ').', element['ip_address']
            print '---------------------'
            userAction = raw_input('Enter the option to connect to host: ')
            while not Validations.checkIsInteger(userAction):
                userAction = raw_input("Enter the option to connect to host: ")

            hostDetails = conn_string['host'][int(userAction)-1]
            self.connect_host(hostDetails['ip_address'],hostDetails['username'],hostDetails['password'],hostDetails['port'])
        except IndexError, IOError:
            print 'Host not found'

    def editHostConfiguration(self):
        try:
            conn_string = JsonFile.readJson()
            if conn_string['host'] == []:
                print 'No IP Address found, try Again'
                return
            print '--------Hosts--------'
            for index, element in enumerate(conn_string['host']):
                print '(', index + 1, ').', element['ip_address']
            print '---------------------'
            userHostOption = raw_input('Select option to edit: ')
            while not Validations.checkIsInteger(userHostOption):
                userHostOption = raw_input("Select option to edit: ")
            JsonFile.updateJson(int(userHostOption))
        except IndexError, IOError:
            print 'Configution not added.'

    def viewHost(self):
        try:
            conn_string = JsonFile.readJson()
            if conn_string['host'] == []:
                print 'No IP Address found, try Again'
                return
            print '\n--------Hosts--------'
            for index, element in enumerate(conn_string['host']):
                print '(', index + 1, ')', element['ip_address']
            print '---------------------'
        except IOError as e:
            print 'Configution not added.'

def some_job(path):
    print 'Hello ', path
    threading.Timer(2.0, some_job, args=('world',)).start()


# t = threading.Timer(2.0, some_job, args=('world',))
# t.start()

def main():
    exitValue = True
    while exitValue:
        print '---------------------'
        print '(1) Add Host'
        print '(2) Remove Host'
        print '(3) Run'
        print '(4) Edit Host Conf.'
        print '(5) View Hosts'
        print '(6) Exit'
        print '---------------------'
        a = Switcher()
        options = raw_input('Enter the option: ')
        if int(options) > 5:
            exitStr = raw_input('Do you want to exit(y/n)?')
            if exitStr == 'y':
                exitValue= False
        else:
            a.numbers_to_options(options)

if __name__ == '__main__':
    main()