import json

def readJson():
    with open("test.json", "r") as jsonFile:
        return json.load(jsonFile)

def editJson(data):
    with open("test.json", "w") as jsonFile:
        json.dump(data, jsonFile)


def updateJson(option):
    index = int(option) -1
    hostStr = 'host'
    try:
        conn_string = readJson()
        hostValues = conn_string[hostStr][index]
        print 'Username = ', hostValues['username']
        print 'Host = ', hostValues['ip_address']
        print 'Port = ', hostValues['port']
    except IndexError:
        print 'Host not exist'

    print '(1) Username'
    print '(2) Password'
    print '(3) Host'
    print '(4) Port'
    print '(5) All'
    print '(6) Exit'
    try:
        userSelectedHost = raw_input('Which you need update? ')
        if int(userSelectedHost) == 1:
            updateHostConfigs(index,'Username','username')
        if int(userSelectedHost) == 2:
            updateHostConfigs(index,'Password','password')
        if int(userSelectedHost) == 3:
            updateHostConfigs(index,'Host','ip_address')
        if int(userSelectedHost) == 4:
            updateHostConfigs(index,'Port','port')
        # if int(userSelectedHost) == 5:
        #     updateHostConfigs(index,'One by One','password')
    except IndexError as e:
        print e


def updateHostConfigs(index,obj, values):
    conn_string = readJson()
    tmp = conn_string["host"][index]
    userValue = raw_input("Enter the " + obj + " values: ")
    conn_string['host'][index][values] = userValue
    editJson(conn_string)