import time
import Validations
from MailConfiguration import Mail
from HostSSH import SSHClient
from terminaltables import AsciiTable
from DHandler import DbHandler
import getpass
from Obj import DataObj
from Constant import HostConstant

class HostOptions(SSHClient, DbHandler, Mail):
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
            password = getpass.getpass("Enter password: ")
            while not Validations.checkIsEmpty(password):
                password = getpass.getpass('Please enter the password: ')

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
            obj = DataObj(None, ipAddress, userName, password, port, dir_path, file_name, email,'')
            self.saveData(obj)
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
            hdetails = self.selectQueryMethod()
            if hdetails == []:
                print 'No IP Address found, try Againn'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            table_data.append(['0','Run All'])
            listIndex = []
            for index, data in enumerate(hdetails):
                index = index +1
                table_data.append([str(data.getDid()), str(data.getHost())])
                listIndex.append(str(index))
            table = AsciiTable(table_data)
            print table.table
            userAction = raw_input('Enter the option to connect host: ')
            if Validations.checkIsInteger(userAction):
                if int(userAction) == 0:
                    self.hostWatcherAll(hdetails)
                else:
                    while not any(str(d.getDid()) == str(userAction) for d in hdetails):
                        userAction = raw_input("Enter the valid option to connect host: ")
                    self.hostWatcher(userAction)
            else:
                numbers = userAction.split(',')
                new_list = []
                hdAll = []
                for element in numbers:
                    if element in listIndex:
                        hdAll.append(hdetails[int(element) -1])
                        new_list.append(element)
                    else:
                        print 'The selected options are not available ='+element
                print hdAll
                if hdAll:
                    self.hostWatcherAll(hdAll)

            # while not Validations.checkIsInteger(userAction):
            #     userAction = raw_input("Enter the option to connect host: ")


        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Host not found'
            return

    def hostWatcher(self, index):
        try:
            while True:
                hdetails = self.selectMethod(index)
                self.connect_host(hdetails)
                time.sleep(10)
        except KeyboardInterrupt:
            self.stopProgress()
            print 'Host watching stopped'
            return

    def hostWatcherAll(self, list):
        # spinner = Validations.initConst()
        try:
            # spinner.start()
            self.startProgress()
            while True:
                self.calculateParallel(list, len(list))
                time.sleep(10)
        except KeyboardInterrupt:
            self.stopProgress()
            print 'Host watching stopped'
            return

    def editHostConfiguration(self):
        try:
            hdetails = self.selectQueryMethod()
            if hdetails == []:
                print 'No IP Address found, try Againn'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            for data in hdetails:
                table_data.append([str(data.getDid()), str(data.getHost())])
            table = AsciiTable(table_data)
            print table.table
            userHostOption = raw_input('Select option to edit: ')
            while not Validations.checkIsInteger(userHostOption):
                userHostOption = raw_input("Select option to edit: ")

            while not any(str(d.getDid()) == str(userHostOption) for d in hdetails):
                userHostOption = raw_input("Select valid option to edit: ")

            self.updateHostData(userHostOption)

        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Configution not added.'

    def viewHost(self):
        try:
            hdetails = self.selectQueryMethod()
            if hdetails == []:
                print 'No IP Address found, try Againn'
                return
            table_data = []
            table_data.append(['Options', 'Hosts', 'Receiver'])
            for data in hdetails:
                table_data.append([str(data.getDid()), str(data.getHost()), str(data.getEmail())])
            table = AsciiTable(table_data)
            print table.table
        except (IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Configution not added.'

    def updateMail(self):
        try:
            table_data = []
            table_data.append(['Mail', 'values'])
            config = self.readMailData()
            if config is None:
                return
            table_data.append(['SMTP', config.getSmtp()])
            table_data.append(['SMTP Port', config.getSmtpPort()])
            table_data.append(['Email', config.getEmail()])
            table_data.append(['Password',' **********'])
            table_data.append(['Receiver', config.getReceiver()])
            table_data.append(['Subject', config.getSub()])
            table = AsciiTable(table_data)
            print table.table

            print 'Do you want to edit mail configuration?'
            print '(1) Modify'
            print '(2) Exit'
            uMailInput = raw_input('Enter the option: ')
            while not Validations.checkIsInteger(uMailInput):
                uMailInput = raw_input("Please enter the option: ")

            if int(uMailInput) == 1:
                self.configMail(self,config.getEmail())
            else:
                return
        except KeyboardInterrupt:
            return

    def removeHostServer(self, obj, index):
        try:
            obj.deleteData(index)
            print 'Succesfully removed host.\n'
        except (IndexError, IOError):
            print 'Host not found'

    def updateHostData(self, option):
        try:
            obj = self.selectMethod(option)
            # conn_string = JsonFile.readJson()
            # hostValues = conn_string[hostStr][index]
            table_data = []
            table_data.append(['Mail', 'Values'])
            table_data.append(['Username', obj.getUname()])
            table_data.append(['Password', ' *******'])
            table_data.append(['Host', obj.getHost()])
            table_data.append(['Port', obj.getPort()])
            table_data.append(['Directory Path', obj.getDpath()])
            table_data.append(['File Name', obj.getFname()])
            table_data.append(['E-mail', obj.getEmail()])
            table = AsciiTable(table_data)
            print table.table
        except IndexError:
            print 'Host not exist'
        print '---------------------'
        print '(1) Username'
        print '(2) Password'
        print '(3) Host'
        print '(4) Port'
        print '(5) Directory Path'
        print '(6) File Name'
        print '(7) E-mail'
        print '(8) All'
        print '(9) Exit'
        print '---------------------'
        try:
            userSelectedHost = raw_input('Select option to update: ')
            while not Validations.checkIsInteger(userSelectedHost):
                userSelectedHost = raw_input("Select option to update: ")
            if int(userSelectedHost) == 1:
                self.updateHostConfigs(option, 'Username', HostConstant.uname)
            if int(userSelectedHost) == 2:
                self.updateHostConfigs(option, 'Password', HostConstant.pwd)
            if int(userSelectedHost) == 3:
                self.updateHostConfigs(option, 'Host', HostConstant.host)
            if int(userSelectedHost) == 4:
                self.updateHostConfigs(option, 'Port', HostConstant.port)
            if int(userSelectedHost) == 5:
                self.updateHostConfigs(option, 'Directory Path', HostConstant.dirpath)
            if int(userSelectedHost) == 6:
                self.updateHostConfigs(option, 'File name', HostConstant.fname)
            if int(userSelectedHost) == 7:
                self.updateHostConfigs(option, 'E-mail', HostConstant.email)
            if int(userSelectedHost) == 8:
                self.updateAllConfigs(option)
            else:
                raise IndexError

        except IndexError as e:
            print e

    def updateHostConfigs(self, index, obj, column):
        # conn_string = readJson()
        # tmp = conn_string["host"][index]
        if column == HostConstant.pwd:
            userValue = getpass.getpass("Enter the " + obj + " value: ")
        else:
            userValue = raw_input("Enter the " + obj + " value: ")

        if column == HostConstant.host:
            while not Validations.checkIsEmpty(userValue):
                userValue = raw_input("Enter the valid host: ")

            while not Validations.isServerUp(userValue):
                ipHost = raw_input('The entered host is server down. Do you want to continue? (y/n)')
                if ipHost == 'y':
                    break
                else:
                    userValue = raw_input("Enter the valid host: ")
        elif column == HostConstant.email:
            if userValue:
                while not Validations.checkEmail(userValue):
                    userValue = raw_input('Enter the valid email address.: ')
                    if not userValue:
                        break
            else:
                userValue = ''
        self.updateData(column, userValue, index)

    def updateAllConfigs(self, index):
        userNameValue = raw_input('Enter the username: ')
        while not Validations.checkIsEmpty(userNameValue):
            userNameValue = raw_input('Please enter the username: ')

        passwordValue = raw_input('Enter the password: ')
        while not Validations.checkIsEmpty(passwordValue):
            passwordValue = raw_input('Please enter the password: ')

        ipAddress = raw_input('Enter the Host: ')
        # while not Validations.checkIp(ip_addressValue):
        #     ip_addressValue = raw_input("Enter the valid host: ")
        while not Validations.checkIsEmpty(ipAddress):
            ipAddress = raw_input("Enter the valid ip address: ")

        while not Validations.isServerUp(ipAddress):
            ipHost = raw_input('The entered host is server down. Do you want to continue? (y/n)')
            if ipHost == 'y':
                return
            else:
                ipAddress = raw_input("Enter the valid ip address: ")

        while self.checkHost(ipAddress, userNameValue, passwordValue) == 'Error':
            checkHostOption = raw_input('The host   do you want continue?(y/n)')
            if checkHostOption == 'n':
                return
            else:
                break

        portValue = raw_input('Enter the port: ')
        if not portValue:
            portValue = '22'

        dir_path = raw_input("Enter the directory path. (ex.:/home/user/): ")
        while not Validations.checkIsEmpty(dir_path):
            dir_path = raw_input('Please enter the directory path: ')
        file_name = raw_input("(Optional)Enter the file name. (ex:*.txt): ")
        if not file_name:
            file_name = ''
        email = raw_input("Enter the email: ")
        if email:
            while not Validations.checkEmail(email):
                email = raw_input('Enter the valid email address.: ')
                if not email:
                    break
        else:
            email = ''
        self.updateAllData(ipAddress, userNameValue, passwordValue, portValue, dir_path, file_name, email, index)
        print 'Updated successfully.'