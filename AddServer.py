import json
import os.path
import threading
import paramiko
import smtplib
import JsonFile

class ServerEnvironment:
    def __init__(self):
        self.ipAddress = []
        self.username = []
        self.password=[]
        self.port = []

    def addServer(self, ipAddress, userName, password, port):
        self.ipAddress.append(ipAddress)
        self.username.append(userName)
        self.password.append(password)
        self.port.append(port)

    def createJsonFile(self):
        for ip,user,pwd,portValue in zip(self.ipAddress, self.username, self.password, self.port):
            datas = {
                "ip_address":ip,
                "username":user,
                "password":pwd,
                "port":portValue
            }
            a = {}
            a['host'] =  []
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

    def removeHostServer(self, ipAddress):
        with open('test.json', 'r') as data_file:
            data = json.load(data_file)

        for index,element in enumerate(data['host']):
            if str(element['ip_address']) == ipAddress:
                del data['host'][index]

        with open('test.json', 'w') as data_file:
            json.dump(data, data_file)

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

class HostConfiguration:
    def swith_configuration(self, argument):
        if int(argument) == 1:
            host_methods = 'updateUser'
        elif int(argument) == 2:
            host_methods = 'updatePassword'
        elif int(argument) == 3:
            host_methods = 'updateHost'
        elif int(argument) == 4:
            host_methods = 'updatePort'
        elif int(argument) == 4:
            host_methods = 'updateAll'
        else:
            print 'No options found'
            return
        method = getattr(self, host_methods, lambda: "Invalid Options")
        return method()

    def updateUser(self):
        jsonList = JsonFile.readJson()

        print ''
    def updatePassword(self):
        print ''
    def updateHost(self):
        print ''
    def updatePort(self):
        print ''
    def updateAll(self):
        print ''


class Switcher(ServerEnvironment, SSHClient, HostConfiguration):
    def numbers_to_options(self, argument):
        if int(argument) == 1:
            method_name = 'addHost'
        elif int(argument) == 2:
            method_name = 'removeHost'
        elif int(argument) == 3:
            method_name = 'runHost'
        elif int(argument) == 4:
            method_name = 'editHostConfiguration'
        else:
            print 'No options found'
            return

        method = getattr(self, method_name, lambda: "Invalid Options")
        return method()

    def addHost(self): #Add Host
        ipAddress = raw_input("Enter ipAddress=")
        while not checkValidIp(ipAddress):
            print 'Enter the valid ip address'
            ipAddress = raw_input("Enter ipAddress=")
        userName = raw_input("Enter userName=")
        password = raw_input("Enter password=")
        port = raw_input("Enter port=")
        self.addServer(ipAddress, userName, password, port)
        self.createJsonFile()

    def removeHost(self): #Remove host
        jsonFile = open('test.json', 'r')
        conn_string = json.load(jsonFile)
        listsHost= []
        for index,element in enumerate(conn_string['host']):
            print index, '.', element['ip_address']
            listsHost.append(str(element['ip_address']))
        host = raw_input("Enter the host to remove from list=")
        while not checkValidIp(host):
            print 'Enter the valid ip address'
            host = raw_input("Enter ipAddress=")
        if host in listsHost:
            self.removeHostServer(host)
        else:
            print 'IP address not found, try again.'

    def runHost(self):
        jsonFile = open('test.json', 'r')
        conn_string = json.load(jsonFile)
        for index,element in enumerate(conn_string['host']):
            print '(',index, ').', element['ip_address']
        if not conn_string or conn_string ==[]:
            print 'No connections available.'
        userAction = raw_input('Enter the option to connect to host=')
        try:
            hostDetails = conn_string['host'][int(userAction)]
            self.connect_host(hostDetails['ip_address'],hostDetails['username'],hostDetails['password'],hostDetails['port'])
        except IndexError:
            print 'Host not found'

    def editHostConfiguration(self):
        jsonFile = open('test.json', 'r')
        conn_string = json.load(jsonFile)
        if conn_string == []:
            print 'No hosts available.'
            return

        for index, element in enumerate(conn_string['host']):
            print '(', index + 1, ').', element['ip_address']

        userHostOption = raw_input('Select host to edit')
        JsonFile.updateJson(int(userHostOption))

def checkValidIp(ip):
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) < 256 for part in parts)
    except ValueError:
        return False
    except (AttributeError, TypeError):
        return False

def some_job(path):
    print 'Hello ', path
    threading.Timer(2.0, some_job, args=('world',)).start()


# t = threading.Timer(2.0, some_job, args=('world',))
# t.start()

if __name__ == '__main__':
    print 'Enter the following which one you need to configure:'
    print '(1) Add Host'
    print '(2) Remove Host'
    print '(3) Run'
    print '(4) Edit Host Conf.'
    a = Switcher()
    options = raw_input('Enter number=')
    a.numbers_to_options(options)

