import json
import time
import JsonFile
import Validations
import MailConfiguration
from HostEnv import ServerEnvironment
from HostSSH import SSHClient
from HostConfig import HostOptions
from Constant import HostConstant

def main():
    try:
        exitValue = True
        while exitValue:
            MailConfiguration.initSetup()
            print '---------------------'
            print HostConstant.ADD
            print HostConstant.REMOVE
            print HostConstant.RUN
            print HostConstant.EDIT
            print HostConstant.VIEW
            print HostConstant.MAIL
            print HostConstant.EXIT
            print '---------------------'
            a = HostOptions()
            options = raw_input(HostConstant.ENTER_OPTION)
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