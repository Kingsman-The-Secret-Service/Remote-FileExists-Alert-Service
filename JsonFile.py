import json
import Validations

def readJson():
    try:
        with open("test.json", "r") as jsonFile:
            return json.load(jsonFile)
    except IOError:
        print 'Host not found'
        return

def writeJson(data):
    try:
        with open("test.json", "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)
    except IOError:
        print 'Host not found'
        return

def updateJson(option):
    index = int(option) -1
    hostStr = 'host'
    try:
        conn_string = readJson()
        hostValues = conn_string[hostStr][index]
        print 'Username : ', hostValues['username']
        print 'Password: *******'
        print 'Host : ', hostValues['ip_address']
        print 'Port : ', hostValues['port']
        print 'Directory Path :', hostValues['dir_path']
        print 'File Name :', hostValues['file_name']

    except IndexError:
        print 'Host not exist'
    print '---------------------'
    print '(1) Username'
    print '(2) Password'
    print '(3) Host'
    print '(4) Port'
    print '(5) Directory Path'
    print '(6) File Name'
    print '(7) All'
    print '(8) Exit'
    print '---------------------'
    try:
        userSelectedHost = raw_input('Select option to update: ')
        while not Validations.checkIsInteger(userSelectedHost):
            userSelectedHost = raw_input("Select option to update: ")
        if int(userSelectedHost) == 1:
            updateHostConfigs(index,'Username','username')
        if int(userSelectedHost) == 2:
            updateHostConfigs(index,'Password','password')
        if int(userSelectedHost) == 3:
            updateHostConfigs(index,'Host','ip_address')
        if int(userSelectedHost) == 4:
            updateHostConfigs(index,'Port','port')
        if int(userSelectedHost) == 5:
            updateHostConfigs(index, 'Directory Path', 'dir_path')
        if int(userSelectedHost) == 6:
            updateHostConfigs(index, 'File name', 'file_name')
        if int(userSelectedHost) == 7:
            updateAllConfigs(inpopdex)
        else:
            raise IndexError

    except IndexError as e:
        print e

def updateAllConfigs(index):
    hostStr = 'host'
    conn_string = readJson()
    tmp = conn_string["host"][index]
    userNameValue = raw_input('Enter the username: ')
    while not Validations.checkIsEmpty(userNameValue):
        userNameValue = raw_input('Please enter the username: ')
    passwordValue = raw_input('Enter the password: ')
    while not Validations.checkIsEmpty(passwordValue):
        passwordValue = raw_input('Please enter the password: ')
    ip_addressValue = raw_input('Enter the Host: ')
    while not Validations.checkValidIp(ip_addressValue):
        ip_addressValue = raw_input("Enter the valid host: ")
    portValue = raw_input('Enter the port: ')
    if not portValue:
        portValue = '22'
    dir_path = raw_input("Enter the directory path. (ex.:/home/user/): ")
    while not Validations.checkIsEmpty(dir_path):
        dir_path = raw_input('Please enter the directory path: ')
    file_name = raw_input("(Optional)Enter the file name. (ex:*.txt): ")
    if not file_name:
        file_name = ''
    conn_string[hostStr][index]['username'] = userNameValue
    conn_string[hostStr][index]['password'] = passwordValue
    conn_string[hostStr][index]['ip_address'] = ip_addressValue
    conn_string[hostStr][index]['port'] = portValue
    conn_string[hostStr][index]['dir_path'] = dir_path
    conn_string[hostStr][index]['file_name'] = file_name
    writeJson(conn_string)

def updateHostConfigs(index,obj, values):
    conn_string = readJson()
    tmp = conn_string["host"][index]
    userValue = raw_input("Enter the " + obj + " value: ")
    conn_string['host'][index][values] = userValue
    writeJson(conn_string)