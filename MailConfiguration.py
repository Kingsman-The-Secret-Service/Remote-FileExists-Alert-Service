import getpass
import Validations
from DHandler import DbHandler

class Mail:
    db = None
    def __init__(self):
        if self.db is None:
            self.db = DbHandler()

    def initSetup(self):
        if self.db.readMailCountData() == 0:
            mailData = {'smtp':'smtp.gmail.com',
                        'port':'587',
                        'sender':'xxxxx@gmail.com',
                        'password':'xxxxxxx',
                        'receiver':'yyyyyy@gmail.com',
                        'sub':'File Created'
                        }
            self.db.saveMailData(mailData)

    def configMail(self, dbObj, mId):
        try:
            smtp = raw_input("Enter the SMTP: ")
            while not Validations.checkIsEmpty(smtp):
                smtp = raw_input("Enter the valid ip address: ")
            smtp_port = raw_input("Enter SMTP Port: ")
            while not Validations.checkIsEmpty(smtp_port):
                smtp_port = raw_input("Please enter the SMTP Port: ")
            email = raw_input("Enter email: ")
            while not Validations.checkIsEmpty(email):
                email = raw_input('Please enter the email: ')
            password = getpass.getpass("Enter password: ")
            while not Validations.checkIsEmpty(password):
                password = getpass.getpass('Please enter the password: ')
            receiver = raw_input("Enter receiver email: ")
            while not Validations.checkIsEmpty(receiver):
                receiver = raw_input('Please enter the receiver email: ')
            subject = raw_input("Enter the mail subject: ")
            while not Validations.checkIsEmpty(subject):
                subject = raw_input('Please enter the mail subject: ')

            mailData = {'smtp': smtp,
                        'port': smtp_port,
                        'sender': email,
                        'password': password,
                        'receiver': receiver,
                        'sub': subject
                        }
            dbObj.updateMailData(mId, mailData)
        except KeyboardInterrupt:
            return
