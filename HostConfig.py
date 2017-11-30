import json
import time
import JsonFile
import Validations
import MailConfiguration
from HostEnv import ServerEnvironment
from HostSSH import SSHClient
from terminaltables import AsciiTable
from DHandler import DbHandler
import getpass
from Obj import DataObj

class HostOptions(ServerEnvironment, SSHClient,DbHandler):

    # def __init__(self):
    #     self.dhandler = DbHandler()


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

    def addHost(self):  # Add Host
        try:
            ipAddress = raw_input("Enter the host: ")
            while not Validations.checkIsEmpty(ipAddress):
                ipAddress = raw_input("Enter the valid ip address: ")

            while not Validations.isServerUp(ipAddress):
                ipHost = raw_input('The entered host is server down. Do you want to continue? (y/n)')
                if ipHost == 'y':
                    break
                else:
                    ipAddress = raw_input("Enter the valid ip address: ")

            userName = raw_input("\nEnter userName: ")
            while not Validations.checkIsEmpty(userName):
                userName = raw_input("Please enter the username: ")
            password = raw_input("Enter password: ")
            while not Validations.checkIsEmpty(password):
                password = raw_input('Please enter the password: ')

            while self.checkHost(ipAddress, userName, password) == 'Error' or '':
                checkHostOption = raw_input('Error occured, Do you want continue?(y/n)')
                if checkHostOption == 'n':
                    return
                else:
                    break

            port = raw_input("Enter port: ")
            if not port:
                port = '22'
            dir_path = raw_input("Enter the directory path. (ex.:/home/user/): ")
            while not Validations.checkIsEmpty(dir_path):
                dir_path = raw_input('Please enter the directory path: ')
            file_name = raw_input("(Optional) Enter the file name or extension. (ex:*.txt): ")

            email = raw_input('Enter the email address for alerts.: ')
            if email:
                while not Validations.checkEmail(email):
                    email = raw_input('Enter the valid email address.: ')
                    if not email:
                        break
            else:
                email = ''
            # uname, pwd, port, dpath, fname, email
            # self.addServer(ipAddress, userName, password, port, dir_path, file_name, email)
            obj = DataObj(None, ipAddress, userName, password, port, dir_path, file_name, email)
            DbHandler().saveData(obj)
            # self.createJsonFile()
        except (IOError, KeyboardInterrupt):
            return

    def removeHost(self):  # Remove host
        try:
            # jsonFile = open('test.json', 'r')
            # conn_string = json.load(jsonFile)
            listsHost = []
            hdetails = self.selectQueryMethod()
            if hdetails == []:
                print 'No IP Address found, try Againn'
                return
            # if conn_string['host'] == []:
            #     print 'No IP Address found, try Again'
            #     return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            for data in hdetails:
                table_data.append([str(data.getDid()), str(data.getHost())])
                listsHost.append(str(data.getHost()))
            # for index, element in enumerate(conn_string['host']):
            #     # print '(', index + 1, ').', element['ip_address']
            #     table_data.append([str(index+1),  str(element['ip_address'])])
            #     listsHost.append(str(element['ip_address']))
            table = AsciiTable(table_data)
            print table.table
            host = raw_input('Enter the option to remove: ')
            while not Validations.checkIsInteger(host):
                host = raw_input("Enter the option to remove: ")

            while not any(str(d.getDid()) == str(host) for d in hdetails):
                host = raw_input("The host not found, Enter the valid option to remove: ")

            choice = raw_input('Are you sure, you want to remove?(y/n)')
            while not Validations.checkIsEmpty(choice):
                choice = raw_input('Do you want to remove?(y/n)')
            if choice == 'y':
                self.removeHostServer(self, host)

        except (IOError, IndexError, KeyboardInterrupt):
            print 'Hosts not found'

    def runHost(self):
        try:
            conn_string = JsonFile.readJson()
            if not conn_string or conn_string['host'] == []:
                print 'No IP Address found, try Again'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            table_data.append(['0','Run All'])
            for index, element in enumerate(conn_string['host']):
                table_data.append([str(index + 1), str(element['ip_address'])])
                # print '(', index + 1, ').', element['ip_address']
            table = AsciiTable(table_data)
            print table.table
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
            self.stopProgress()
            return

    def hostWatcherAll(self, list):
        spinner = Validations.initConst()
        try:
            spinner.start()
            while True:
                self.calculateParallel(list, len(list))
                # for n in squaredNumbers:
                #     print(n)
                time.sleep(60)
        except KeyboardInterrupt:
            spinner.stop()
            return

    def editHostConfiguration(self):
        try:
            conn_string = JsonFile.readJson()
            if conn_string['host'] == []:
                print 'No IP Address found, try Again'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            for index, element in enumerate(conn_string['host']):
                table_data.append([str(index + 1), str(element['ip_address'])])
            table = AsciiTable(table_data)
            print table.table
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
            table_data = []
            table_data.append(['Options', 'Hosts', 'Receiver'])
            for index, element in enumerate(conn_string['host']):
                table_data.append([str(index + 1), str(element['ip_address']), str(element['email'])])
                # print '(', index + 1, ')', element['ip_address']
            table = AsciiTable(table_data)
            print table.table
        except (IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Configution not added.'

    def updateMail(self):
        try:
            table_data = []
            table_data.append(['Mail', 'values'])
            config = MailConfiguration.read_config()
            table_data.append(['SMTP', config.get('main', 'smtp')])
            table_data.append(['SMTP Port', config.get('main', 'smtp_port')])
            table_data.append(['Email', config.get('main', 'e-mail')])
            table_data.append(['Password',' **********'])
            table_data.append(['Receiver', config.get('main', 'receiver')])
            table_data.append(['Subject', config.get('main', 'subject')])
            table = AsciiTable(table_data)
            print table.table
            # print 'SMTP: ', config.get('main', 'smtp')
            # print 'SMTP Port: ', config.get('main', 'smtp_port')
            # print 'Email: ', config.get('main', 'e-mail')
            # print 'Password: **********'
            # print 'Receiver: ', config.get('main', 'receiver')
            # print 'Subject: ', config.get('main', 'subject')

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
