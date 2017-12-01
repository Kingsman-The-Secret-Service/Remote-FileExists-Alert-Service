import sys
import paramiko
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import time
import Validations
from multiprocessing.dummy import Pool as ThreadPool
from Constant import HostConstant
from DHandler import DbHandler

class SSHClient(HostConstant, DbHandler):
    def calculateParallel(self, data, threads=2):
        pool = ThreadPool(threads)
        results = pool.map(self.connect_host, data)
        pool.close()
        pool.join()
        return results

    def mailAlert(self, data):
        config = self.readMailData()
        smtp = config.getSmtp()
        smtp_port = config.getSmtpPort()
        mail = config.getEmail()
        password = config.getPwd()
        subject = config.getSub()

        receiver = data.getEmail()
        if not receiver:
            receiver = config.getReceiver()
        try:
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
            server.sendmail(mail, receiver, text)
        except smtplib.SMTPAuthenticationError as e:
            print e
            return

    def checkHost(self, server, user, pwd):
        spinner = Validations.initConst()
        spinner.start()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(server, username=user, password=pwd)
            spinner.stop()
            return 'working'
        except paramiko.BadHostKeyException, e:
            spinner.stop()
            print e
            return 'Error'
        except paramiko.AuthenticationException, e:
            print e
            spinner.stop()
            return 'Error'
        except paramiko.SSHException, e:
            spinner.stop()
            print e
            print 'Error'
        except socket.error as e:
            spinner.stop()
            print 'socket =', e
            return 'Error'
        finally:
            ssh.close()

    def connect_host(self, data):
        try:
            server, username, password = (data.getHost(), data.getUname(), data.getPwd())
            # port = data.getPort()
            ssh = paramiko.SSHClient()
            paramiko.util.log_to_file("ssh.log")
            sys.stdout.write('connecting host...')
            time.sleep(2)
            sys.stdout.flush()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn = ssh.connect(server, username=username, password=password)
            if conn:
                print 'connection failed'
            self.startProgress()
            sftp = ssh.open_sftp()
            try:
                folderPath = str(data.getDpath())
                list = sftp.listdir(folderPath)
                if not list == []:
                    fileExt = str(data.getFname())
                    if not fileExt:
                        self.mailAlert(data)
                    else:
                        patern = re.compile(r"[^\\]%s$" % fileExt, re.I)
                        filtered_files = [f for f in list if patern.search(f)]
                        if filtered_files == []:
                            if any(fileExt in s for s in list):
                                # print 'yes'
                                self.mailAlert(data)
                            else:
                                print 'No'
                        else:
                            self.mailAlert(data)
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

    def startProgress(self):
        self.initSpinner().start()

    def stopProgress(self):
        self.initSpinner().stop()