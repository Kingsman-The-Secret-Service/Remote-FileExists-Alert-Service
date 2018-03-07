import getpass

import Validations
from UIwindow.DHandler import DbHandler


class Mail:
    db = None
    def __init__(self):
        if self.db is None:
            self.db = DbHandler()

    def initSetup(self):
        if self.db.readSmtpData() is None:
            smtpData = {'smtp': 'smtp.gmail.com',
                        'smtpPort': '587'}
            self.db.saveSmtpData(smtpData)

        if self.db.readMailCountData() == 0:
            mailData = {'smtpMail':'xxxxx@gmail.com',
                        'mailPwd':'xxxxxxx',
                        'receiver':'yyyyyy@gmail.com',
                        'subject':'File Created'
                        }
            self.db.saveMailData(mailData)

    def configSmtp(self, dbObj):
        smtp = raw_input("Enter the SMTP: ")
        while not Validations.checkIsEmpty(smtp):
            smtp = raw_input("Enter the valid SMTP: ")
        smtp_port = raw_input("Enter SMTP Port: ")
        while not Validations.checkIsEmpty(smtp_port):
            smtp_port = raw_input("Please enter the SMTP Port: ")

        mailData = {'smtp': smtp,
                    'smtpPort': smtp_port}
        dbObj.updateSmtpData(mailData)
        dbObj.updateMail()

    def configMail(self, dbObj, mId):
        try:
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

            mailData = {'smtpMail': email,
                        'mailPwd': password,
                        'receiver': receiver,
                        'subject': subject
                        }
            dbObj.updateMailData(mId, mailData)
        except KeyboardInterrupt:
            return
