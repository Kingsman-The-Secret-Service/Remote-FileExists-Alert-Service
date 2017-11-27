import json
import os.path
import threading
import paramiko
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import JsonFile
import Validations
import MailConfiguration
from multiprocessing.dummy import Pool as ThreadPool
import glob, os
import re
import time

class ServerEnvironment:
    def __init__(self):
        self.ipAddress = ''
        self.username = ''
        self.password=''
        self.port = ''
        self.dir_path = ''
        self.filename = ''

    def addServer(self, ipAddress, username, password, port, dir_path, filename):
        self.ipAddress = ipAddress
        self.username = username
        self.password = password
        self.port = port
        self.dir_path = dir_path
        self.filename = filename

    def createJsonFile(self):
        datas = {
            "ip_address": self.ipAddress,
            "username": self.username,
            "password": self.password,
            "port": self.port,
            "dir_path":self.dir_path,
            "file_name":self.filename
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
    def removeHostServer(self, index):
        try:
            data = JsonFile.readJson()
            del data['host'][index]
            JsonFile.writeJson(data)
            print 'Succesfully removed host.\n'
        except IndexError, IOError:
            print 'Host not found'

class SSHClient():
    def calculateParallel(self, data, threads=2):
        pool = ThreadPool(threads)
        results = pool.map(self.connect_host, data)
        pool.close()
        pool.join()
        return results

    def mailAlert(self):
        config = MailConfiguration.read_config()
        smtp = config.get('main', 'smtp')
        smtp_port = config.get('main', 'smtp_port')
        mail = config.get('main', 'e-mail')
        password = config.get('main', 'password')
        receiver = config.get('main', 'receiver')
        subject = config.get('main', 'subject')

        server = smtplib.SMTP(smtp, int(smtp_port))
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(mail, password)
        msg = MIMEMultipart()
        msg['From'] = mail
        msg['To'] = receiver
        msg['Subject'] = subject
        body = "File Created"
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        server.sendmail(mail, "akkravikumar@gmail.com", text)

    def connect_host(self, data):
        try:
            server, username, password = (data['ip_address'], data['username'], data['password'])
            ssh = paramiko.SSHClient()
            paramiko.util.log_to_file("ssh.log")
            print 'connecting host...'
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn = ssh.connect(server, username=username, password=password)
            if conn is None:
                print 'Connection successful.'
            else:
                print 'connection failed'
            sftp = ssh.open_sftp()
            try:
                folderPath = str(data['dir_path'])
                list = sftp.listdir(folderPath)
                if not list == []:
                    fileExt = str(data['file_name'])
                    if not fileExt:
                        self.mailAlert()
                    else:
                        patern = re.compile(r"[^\\]%s$"%fileExt, re.I)
                        filtered_files = [f for f in list if patern.search(f)]
                        if filtered_files ==[] :
                            if any(fileExt in s for s in list):
                                # print 'yes'
                                self.mailAlert()
                            else:
                                print 'No'
                        else:
                            self.mailAlert()
                            print filtered_files
                else:
                    print 'No files in this directory.'
                # for element in list:
                #     print '=', element
            except IOError as e:
                print e
                return
            finally:
                sftp.close()
                ssh.close()
        except paramiko.AuthenticationException:
            output = "Authentication Failed"
            print output
        # except KeyboardInterrupt:
        #     return

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
        elif int(argument) == 6:
            method_name = 'updateMail'
        else:
            print 'No options found'
            return

        method = getattr(self, method_name, lambda: "Invalid Options")
        return method()

    def addHost(self): #Add Host
        try:
            ipAddress = raw_input("Enter the host: ")
            while not Validations.checkIsEmpty(ipAddress):
                ipAddress = raw_input("Enter the valid ip address: ")

            while not Validations.isServerUp(ipAddress):
                ipHost = raw_input('The entered host is server down. Do you want to continue? (y/n)')
                if ipHost =='y':
                    return
                else:
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
            dir_path = raw_input("Enter the directory path. (ex.:/home/user/): ")
            while not Validations.checkIsEmpty(dir_path):
                dir_path = raw_input('Please enter the directory path: ')
            file_name = raw_input("(Optional) Enter the file name or extension. (ex:*.txt): ")

            self.addServer(ipAddress, userName, password, port, dir_path, file_name)
            self.createJsonFile()
        except (IOError, KeyboardInterrupt):
            return

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
        except (IOError, IndexError, KeyboardInterrupt):
            print 'Hosts not found'

    def runHost(self):
        try:
            conn_string = JsonFile.readJson()
            if not conn_string or conn_string['host'] ==[]:
                print 'No IP Address found, try Again'
                return
            print '---------------------'
            print '( 0 ) Run all'
            for index,element in enumerate(conn_string['host']):
                print '(',index+1, ').', element['ip_address']
            print '---------------------'
            userAction = raw_input('Enter the option to host: ')
            while not Validations.checkIsInteger(userAction):
                userAction = raw_input("Enter the option to host: ")

            if int(userAction) == 0:
                list = []
                for element in conn_string['host']:
                    list.append(element)

                self.hostWatcherAll(list)
            else:
                self.hostWatcher(userAction)

        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Host not found'
            return

    def hostWatcher(self, index):
        try:
            while True:
                conn_string = JsonFile.readJson()
                hostDetails = conn_string['host'][int(index) - 1]
                self.connect_host(hostDetails)
                time.sleep(5)
        except KeyboardInterrupt:
            return

    def hostWatcherAll(self, list):
        try:
            while True:
                self.calculateParallel(list, len(list))
                # for n in squaredNumbers:
                #     print(n)
                time.sleep(5)
        except KeyboardInterrupt:
            return

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
        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
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
        except (IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Configution not added.'

    def updateMail(self):
        try:
            print '-----Mail Setup------'
            config = MailConfiguration.read_config()
            print 'SMTP: ',config.get('main', 'smtp')
            print 'SMTP Port: ', config.get('main', 'smtp_port')
            print 'Email: ', config.get('main', 'e-mail')
            print 'Password: **********'
            print 'Receiver: ', config.get('main', 'receiver')
            print 'Subject: ', config.get('main', 'subject')
            print '---------------------'

            print 'Do you want to edit mail configuration?'
            print '(1) Modify'
            print '(2) Exit'
            uMailInput = raw_input('Enter the option: ')
            while not Validations.checkIsInteger(uMailInput):
                uMailInput = raw_input("Please enter the option: ")

            if int(uMailInput) == 1:
                MailConfiguration.configMail()
            else:
                return
        except KeyboardInterrupt:
            return


def some_job(path):
    print 'Hello ', path
    threading.Timer(2.0, some_job, args=('world',)).start()


t = threading.Timer(2.0, some_job, args=('world',))
# t.start()

def main():
    try:
        exitValue = True
        while exitValue:
            MailConfiguration.initSetup()
            print '---------------------'
            print '(1) Add Host'
            print '(2) Remove Host'
            print '(3) Run'
            print '(4) Edit Host Conf.'
            print '(5) View Hosts'
            print '(6) Mail Configuration'
            print '(7) Exit'
            print '---------------------'
            a = Switcher()
            options = raw_input('Enter the option: ')
            while not Validations.checkIsInteger(options):
                options = raw_input("Please enter the option: ")
            if int(options) > 6:
                exitStr = raw_input('Do you want to exit(y/n)?')
                if exitStr == 'y':
                    exitValue= False
            else:
                a.numbers_to_options(options)
    except KeyboardInterrupt:
        print ''

if __name__ == '__main__':
    main()


