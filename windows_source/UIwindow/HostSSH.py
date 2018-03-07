import re
import smtplib
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing.dummy import Pool as ThreadPool

import paramiko

from Constant import HostConstant
from DHandler import DbHandler


class SSHClient(HostConstant, DbHandler):
    def calculateParallel(self, data, threads):
        pool = ThreadPool(threads)
        results = pool.map(self.connect_host, data)
        pool.close()
        pool.join()
        return results

    def mailAlert(self, data):
        self.logComment(str('mail alert'))
        smtpConfig = self.readSmtpData()
        config = self.readMailData()
        smtp = smtpConfig['smtp']
        smtp_port = smtpConfig['smtpPort']
        mail = config['smtpMail']
        password = config['mailPwd']
        subject = config['subject']

        receiver = data['mail']
        if not receiver:
            receiver = config['receiver']
        try:
            self.logComment(str('mail sending'))
            recipients_list = receiver.split(',')
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
            server.sendmail(mail, recipients_list, text)
        except smtplib.SMTPAuthenticationError as e:
            self.logComment(str(e))
            print(e)
            return

    def mailCheck(self, config):
        self.logComment(str('mail check'))
        server, error = None, None
        smtp = config['smtp']
        smtp_port = config['smtpPort']
        mail = config['smtpMail']
        password = config['mailPwd']
        self.logComment(str(smtp))
        try:
            server = smtplib.SMTP(smtp, int(smtp_port))
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(mail, password)
            self.logComment(str(mail) + " " + str(password))
        except Exception as e:
            self.logComment('Error ' + str(e))
            print(e)
            error = True

        return server, error

    def checkHost(self, hostData):
        self.logComment(str('checkhost'))
        error = None
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostData['hostname'], username=hostData['username'], password=hostData['password'])
            self.logComment(str('checkhost success'))
        except Exception as e:
            print(e)
            error = True
        # finally:
        #     ssh.close()
        return ssh, error

    def connect_host(self, data):
        self.logComment(str('connect_host'))
        try:
            self.logComment('data = '+str(data))
            pwd = self.decryptpwd(data['password'])
            self.logComment('pwd ='+str(pwd))
            server, username, password = (data['hostname'], data['username'], pwd)
            self.logComment('testing server')
            port = data['port']
            self.logComment('port = '+str(port))
            ssh = paramiko.SSHClient()
            self.logComment('paraiko sshClient init')
            # sys.stdout.write('connecting host...')
            self.logComment('write sys.stdout')
            # time.sleep(2)
            self.logComment('time sleep')
            # sys.stdout.flush()
            self.logComment('data details = '+str(server + ' ' + username + ' ' + password))
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn = ssh.connect(server, port=port, username=username, password=password)
            self.logComment(str('connected ssh'))
            if conn:
                print('connection failed')
                self.logComment(str('connection failed'))
            sftp = ssh.open_sftp()
            self.logComment(str('sftp open'))
            try:
                folderPath = str(data['dir'])
                list = sftp.listdir(folderPath)
                if not list == []:
                    self.logComment(str('list'))
                    list.sort()
                    myString = ",".join(list)
                    myFs = self.getHostDetail(data['hostname'])
                    if myFs['fwatch'] == myString:
                        return
                    else:
                        if myFs['iswatch'] == 'Yes':
                            self.updateFiles(myString, data['hostname'])
                            self.logComment(str('update file'))

                    fileExt = str(data['file_name'])
                    if not fileExt:
                        self.logComment(str('file exist'))
                        self.mailAlert(data)
                    else:
                        self.logComment(str('file not list'))
                        patern = re.compile(r"[^\\]%s$" % fileExt, re.I)
                        filtered_files = [f for f in list if patern.search(f)]
                        if filtered_files == []:
                            if any(fileExt in s for s in list):
                                self.mailAlert(data)
                            else:
                                print('No')
                        else:
                            self.mailAlert(data)
                            print(filtered_files)
                else:
                    self.logComment(str('no files in this directory'))
                    sys.stdout.write('No files in this directory.')
                    time.sleep(2)
                    sys.stdout.flush()
                    # print 'No files in this directory.'
            except IOError as e:
                self.logComment('IO error' + str(e))
                sys.stdout.write(str(e))
                time.sleep(2)
                sys.stdout.flush()
                # print e
                return
            except Exception as e:
                self.logComment('exception ' + str(e))
            finally:
                sftp.close()
                ssh.close()
        except paramiko.AuthenticationException:
            self.logComment('Authentication error = ' )
            output = "Authentication Failed"
            print(output)
        except Exception as e:
            self.logComment('exceptin error = '+str(e))

    def check_host_server(self, ssh):
        sftp = ssh.open_sftp()
        return sftp

    def checkFileEntries(self, data, sftp):
        # sftp = ssh.open_sftp()
        try:
            folderPath = str(data['dir'])
            list = sftp.listdir(folderPath)
            if not list == []:
                list.sort()
                myString = ",".join(list)
                myFs = self.getHostDetail(data['hostname'])
                if myFs['fwatch'] == myString:
                    return
                else:
                    if myFs['iswatch'] == 'Yes':
                        self.updateFiles(myString, data['hostname'])

                fileExt = str(data['file_name'])
                if not fileExt:
                    self.mailAlert(data)
                else:
                    patern = re.compile(r"[^\\]%s$" % fileExt, re.I)
                    filtered_files = [f for f in list if patern.search(f)]
                    if filtered_files == []:
                        if any(fileExt in s for s in list):
                            self.mailAlert(data)
                        else:
                            print('No')
                    else:
                        self.mailAlert(data)
                        print(filtered_files)
            else:
                time.sleep(2)
                sys.stdout.flush()
        except Exception as e:
            print(e)

    def execute(self, ssh, cmd):
        stdin, stdout, stderr = ssh.exec_command(cmd)
        return stdout.read()

        cmd_op = stdout.read()
        result = '----------'
        result += cmd_op.decode('utf-8')
        print(result)
