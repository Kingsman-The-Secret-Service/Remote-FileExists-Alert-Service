import time
import Validations
from MailConfiguration import Mail
from HostSSH import SSHClient
from terminaltables import AsciiTable
from DHandler import DbHandler
import getpass
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

            newServerData = {
                'env':'cli',
                'hostname': ipAddress,
                'username': userName,
                'password': password,
            }

            self.startProgress()
            ssh, error = self.checkHost(newServerData)
            if error:
                checkHostOption = raw_input('Failed to connect the server, Do you want continue?(y/n)')
                if checkHostOption == 'n':
                    return
            ssh.close()
            self.stopProgress()


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
            pwd = self.encryptpwd(password)
            hostData = {
                'hostname': ipAddress,
                'username': userName,
                'password': pwd,
                'port': port,
                'dir':dir_path,
                'file_name':file_name,
                'mail':email,
                'fwatcher':''
            }
            self.saveData(hostData)
            # self.createJsonFile()
        except (IOError, KeyboardInterrupt):
            return

    def removeHost(self):  # Remove host
        try:
            listsHost = []
            hdetails = self.selectHostDetail()
            if hdetails == []:
                print 'No IP Address found, try Again'
                return

            table_data = []
            table_data.append(['Options', 'Hosts'])
            for data in hdetails:
                table_data.append([str(data['did']), str(data['hostname'])])
                listsHost.append(str(data['hostname']))
            table = AsciiTable(table_data)
            print table.table
            host = raw_input('Enter the option to remove: ')
            while not Validations.checkIsInteger(host):
                host = raw_input("Enter the option to remove: ")

            while not any(str(d['did']) == str(host) for d in hdetails):
                host = raw_input("The host not found, Enter the valid option to remove: ")

            choice = raw_input('Are you sure, you want to remove?(y/n)')
            while not Validations.checkIsEmpty(choice):
                choice = raw_input('Do you want to remove?(y/n)')
            if choice == 'y':
                self.removeHostServer(host)

        except (IOError, IndexError, KeyboardInterrupt):
            print 'Hosts not found'

    def runHost(self):
        try:
            hdetails = self.selectHostDetail()
            if hdetails == []:
                print 'No IP Address found, try Again'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            table_data.append(['0','Run All'])
            listIndex = []
            listId = []
            for index, data in enumerate(hdetails):
                index = index +1
                table_data.append([str(data['did']), str(data['hostname'])])
                listIndex.append(str(index))
                listId.append(str(data['did']))
            table = AsciiTable(table_data)
            print table.table
            userAction = raw_input('Enter the option to connect host: ')
            if Validations.checkIsInteger(userAction):
                if int(userAction) == 0:
                    self.hostWatcherAll(hdetails)
                else:
                    while not any(str(d['did']) == str(userAction) for d in hdetails):
                        userAction = raw_input("Enter the valid option to connect host: ")
                    self.hostWatcher(userAction)
            else:
                try:
                    numbers = userAction.split(',')
                    hdAll = []
                    for element in numbers:
                        # indices = [i for i, x in enumerate(hdetails) if str(x['did']) == element]
                        for ix, x in enumerate(hdetails):
                            if str(x['did']) == element:
                                hdAll.append(hdetails[ix])
                    if hdAll:
                        self.hostWatcherAll(hdAll)
                    else:
                        print 'The entered options are not available'
                except TypeError:
                    print 'Enter the valid hosts.'
                    return
        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Host not found'
            return

    def hostWatcher(self, index):
        try:
            hdetails = self.selectMethod(index)
            self.updateFileData('', hdetails['hostname'])
            self.startProgress()
            while True:
                self.connect_host(hdetails)
                time.sleep(10)
        except KeyboardInterrupt:
            self.stopProgress()
            hdetails = self.selectMethod(index)
            self.updateFileData('', hdetails['hostname'])
            print 'Host watching stopped'
            return

    def hostWatcherAll(self, list):
        try:
            self.startProgress()
            while True:
                self.calculateParallel(list, len(list))
                time.sleep(10)
        except KeyboardInterrupt:
            self.stopProgress()
            for h in list:
                self.updateFileData('', h['hostname'])
            print 'Host watching stopped'
            return

    def editHostConfiguration(self):
        try:
            hdetails = self.selectHostDetail()
            if hdetails == []:
                print 'No IP Address found, try Again'
                return
            table_data = []
            table_data.append(['Options', 'Hosts'])
            for data in hdetails:
                table_data.append([str(data['did']), str(data['hostname'])])
            table = AsciiTable(table_data)
            print table.table
            userHostOption = raw_input('Select option to edit: ')
            while not Validations.checkIsInteger(userHostOption):
                userHostOption = raw_input("Select option to edit: ")

            while not any(str(d['did']) == str(userHostOption) for d in hdetails):
                userHostOption = raw_input("Select valid option to edit: ")

            self.updateHostData(userHostOption)

        except (IndexError, IOError, KeyboardInterrupt, AttributeError, TypeError):
            print 'Configution not added.'

    def viewHost(self):
        try:
            hdetails = self.selectHostDetail()
            if hdetails == []:
                print 'No IP Address found, try Again'
                return
            table_data = []
            table_data.append(['Options', 'Hosts', 'Receiver'])
            for data in hdetails:
                table_data.append([str(data['did']), str(data['hostname']), str(data['mail'])])
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
            table_data.append(['SMTP', config['smtp']])
            table_data.append(['SMTP Port', config['smtpPort']])
            table_data.append(['Email', config['smtpMail']])
            table_data.append(['Password',' **********'])
            table_data.append(['Receiver', config['receiver']])
            table_data.append(['Subject', config['subject']])
            table = AsciiTable(table_data)
            print table.table

            print 'Do you want to edit mail configuration?'
            print '(1) Modify'
            print '(2) Exit'
            uMailInput = raw_input('Enter the option: ')
            while not Validations.checkIsInteger(uMailInput):
                uMailInput = raw_input("Please enter the option: ")

            if int(uMailInput) == 1:
                self.configMail(self,config['smtpMail'])
            else:
                return
        except KeyboardInterrupt:
            return

    def removeHostServer(self, index):
        try:
            self.deleteData(index)
            print 'Succesfully removed host.\n'
        except (IndexError, IOError):
            print 'Host not found'

    def updateHostData(self, option):
        try:
            obj = self.selectMethod(option)
            table_data = []
            table_data.append(['Mail', 'Values'])
            table_data.append(['Username', obj['username']])
            table_data.append(['Password', ' *******'])
            table_data.append(['Host', obj['hostname']])
            table_data.append(['Port', obj['port']])
            table_data.append(['Directory Path', obj['dir']])
            table_data.append(['File Name', obj['file_name']])
            table_data.append(['E-mail', obj['mail']])
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
        if column == HostConstant.pwd:
            userValue = getpass.getpass("Enter the " + obj + " value: ")
            userValue = self.encryptpwd(userValue)
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

        passwordValue = getpass.getpass('Enter the password: ')
        while not Validations.checkIsEmpty(passwordValue):
            passwordValue = getpass.getpass('Please enter the password: ')

        ipAddress = raw_input('Enter the Host: ')
        while not Validations.checkIsEmpty(ipAddress):
            ipAddress = raw_input("Enter the valid ip address: ")

        while not Validations.isServerUp(ipAddress):
            ipHost = raw_input('The entered host is server down. Do you want to continue? (y/n)')
            if ipHost == 'y':
                return
            else:
                ipAddress = raw_input("Enter the valid ip address: ")

        hostData = {
            'env': 'cli',
            'hostname': ipAddress,
            'username': userNameValue,
            'password': passwordValue,
        }

        self.startProgress()
        ssh, error = self.checkHost(hostData)
        if error:
            checkHostOption = raw_input('Failed to connect the server, Do you want continue?(y/n)')
            if checkHostOption == 'n':
                return
        ssh.close()
        self.stopProgress()

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
        pwd = self.encryptpwd(passwordValue)
        updateServerData = {
            'hostname': ipAddress,
            'username': userNameValue,
            'password': pwd,
            'port': portValue,
            'dir': dir_path,
            'file_name':file_name,
            'mail': email
        }
        self.updateAllData(updateServerData, index)
        print 'Updated successfully.'