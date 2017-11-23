from ConfigParser import SafeConfigParser
import os.path
import Validations


def initParser():
    return SafeConfigParser()


def initSetup():
    if not os.path.isfile('config.ini'):
        config = initParser()
        config.read('config.ini')
        config.add_section('main')
        config.set('main', 'smtp', 'smtp.gmail.com')
        config.set('main', 'smtp_port', '587')
        config.set('main', 'e-mail', 'dummy.letsmeditate@gmail.com')
        config.set('main', 'password', 'lets@2858')
        config.set('main', 'receiver', 'akkravikumar@gmail.com')
        config.set('main', 'subject', 'File Created')

        with open('config.ini', 'w') as f:
            config.write(f)


def configMail():
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
        password = raw_input("Enter password: ")
        while not Validations.checkIsEmpty(password):
            password = raw_input('Please enter the password: ')
        receiver = raw_input("Enter receiver email: ")
        while not Validations.checkIsEmpty(receiver):
            receiver = raw_input('Please enter the receiver email: ')
        subject = raw_input("Enter the mail subject: ")
        while not Validations.checkIsEmpty(subject):
            subject = raw_input('Please enter the mail subject: ')
        update_config(smtp, smtp_port, email, password, receiver, subject)
    except KeyboardInterrupt:
        return

def update_config(smtp, smtp_port, e_mail, mail_password, receiver, subject):
    config = initParser()
    config.read('config.ini')

    config.set('main', 'smtp', smtp)
    config.set('main', 'smtp_port', str(smtp_port))
    config.set('main', 'e-mail', e_mail)
    config.set('main', 'password', mail_password)
    config.set('main', 'receiver', receiver)
    config.set('main', 'subject', subject)
    with open('config.ini', 'w+') as f:
        config.write(f)

def read_config():
    config = initParser()
    config.read('config.ini')
    return config
