from WindowUI import *

class server(UiSample):

    def __init__(self):
        super(server, self).__init__()
        self.dbHandler = DbHandler()
        self.constant = HostConstant()
        self.ssh = SSHClient()
        self.generateTree()

    def generateTree(self):
        self.serverData = QStandardItemModel()
        self.serverData.setHorizontalHeaderLabels(["Server List"])
        self.treeView.setModel(self.serverData)
        self.dhandler = DbHandler()
        data = self.dbHandler.getServerGrouped()

        for group in data:
            serverGroup = QStandardItem(group)
            serverGroup.setData(json.dumps({'hostname': group, 'count': data[group]['count']}))
            self.serverData.appendRow(serverGroup)


    def addServer(self):
        if self.mainWindow.sender().objectName() == 'MainMenuAddServer':
            mailData = self.dbHandler.readMailData()
            if mailData:
                self.serverDialog()
            else:
                QMessageBox.information(self.mainWindow, 'Warning', "Please setup the mail configuration before adding server.",
                                        QMessageBox.Ok)

    def editServer(self):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()
        hostServer = self.dbHandler.getHostDetail(hostname)
        self.serverDialog(hostServer)

    def serverDialog(self, hostServer = {}):
        self.qdialog = QDialog()
        self.qdialog.setWindowTitle("Add Server Details")
        self.qdialog.setWindowModality(Qt.ApplicationModal)
        self.qdialog.setFixedSize(300, 280)

        formwidget = QWidget(self.qdialog)
        formLayout = QFormLayout(formwidget)

        hostLabel = QLabel(formwidget)
        hostLabel.setText("Hostname/IP")
        hostLabel.setToolTip('Hostname/IP')
        formLayout.setWidget(0, QFormLayout.LabelRole, hostLabel)
        userLabel = QLabel(formwidget)
        userLabel.setText("Username ")
        userLabel.setToolTip('Username')
        formLayout.setWidget(1, QFormLayout.LabelRole, userLabel)
        pwdLabel = QLabel(formwidget)
        pwdLabel.setText("Password: ")
        pwdLabel.setToolTip('Password')
        formLayout.setWidget(2, QFormLayout.LabelRole, pwdLabel)
        portLabel = QLabel(formwidget)
        portLabel.setText("Port: ")
        portLabel.setToolTip('Port')
        formLayout.setWidget(3, QFormLayout.LabelRole, portLabel)
        dirLabel = QLabel(formwidget)
        dirLabel.setText("Dir Path ")
        dirLabel.setToolTip('Directory Path')
        formLayout.setWidget(4, QFormLayout.LabelRole, dirLabel)
        fileLabel = QLabel(formwidget)
        fileLabel.setText("File Name\n ex:(*.txt)")
        fileLabel.setToolTip('File Name')
        formLayout.setWidget(5, QFormLayout.LabelRole, fileLabel)
        mailLabel = QLabel(formwidget)
        mailLabel.setText("Email")
        mailLabel.setToolTip('Email')
        formLayout.setWidget(6, QFormLayout.LabelRole, mailLabel)

        self.hostnameField = QLineEdit(formwidget)
        formLayout.setWidget(0, QFormLayout.FieldRole, self.hostnameField)

        self.usernameField = QLineEdit(formwidget)
        formLayout.setWidget(1, QFormLayout.FieldRole, self.usernameField)

        self.passwordField = QLineEdit(formwidget)
        self.passwordField.setEchoMode(QLineEdit.Password)
        formLayout.setWidget(2, QFormLayout.FieldRole, self.passwordField)

        self.portField = QLineEdit(formwidget)
        self.portField.setText('22')
        formLayout.setWidget(3, QFormLayout.FieldRole, self.portField)

        self.dirField = QLineEdit(formwidget)
        formLayout.setWidget(4, QFormLayout.FieldRole, self.dirField)

        self.fileField = QLineEdit(formwidget)
        formLayout.setWidget(5, QFormLayout.FieldRole, self.fileField)
        self.mailField = QLineEdit(formwidget)
        formLayout.setWidget(6, QFormLayout.FieldRole, self.mailField)

        if ('hostname' in hostServer):
            self.hostnameField.setText(hostServer['hostname'])
        if ('username' in hostServer):
            self.usernameField.setText(hostServer['username'])
        if ('password' in hostServer):
            self.passwordField.setText(self.constant.decryptpwd(hostServer['password']))
        if ('port' in hostServer):
            self.portField.setText(str(hostServer['port']))
        if ('dir' in hostServer):
            self.dirField.setText(hostServer['dir'])
        if ('file_name' in hostServer):
            self.fileField.setText(hostServer['file_name'])
        if ('mail' in hostServer):
            self.mailField.setText(hostServer['mail'])

        hostnameExp = QRegExp(self.domainOrIpRegex())
        hostnameValidator = QRegExpValidator(hostnameExp, self.hostnameField)
        self.hostnameField.setValidator(hostnameValidator)
        self.hostnameField.textChanged.connect(self.validateServerFormOnChange)
        self.hostnameField.textChanged.emit(self.hostnameField.text())

        usernameExp = QRegExp(".{1,30}")
        usernameValidator = QRegExpValidator(usernameExp, self.usernameField)
        self.usernameField.setValidator(usernameValidator)
        self.usernameField.textChanged.connect(self.validateServerFormOnChange)
        self.usernameField.textChanged.emit(self.usernameField.text())

        passwordExp = QRegExp(".{1,30}")
        passwordValidator = QRegExpValidator(passwordExp, self.passwordField)
        self.passwordField.setValidator(passwordValidator)
        self.passwordField.textChanged.connect(self.validateServerFormOnChange)
        self.passwordField.textChanged.emit(self.passwordField.text())

        portExp = QRegExp(self.portRegex())
        portValidator = QRegExpValidator(portExp, self.portField)
        self.portField.setValidator(portValidator)
        self.portField.textChanged.connect(self.validateServerFormOnChange)
        self.portField.textChanged.emit(self.portField.text())

        dirFieldExp = QRegExp(".{1,30}")
        direcotoryValidator = QRegExpValidator(dirFieldExp, self.dirField)
        self.dirField.setValidator(direcotoryValidator)
        self.dirField.textChanged.connect(self.validateServerFormOnChange)
        self.dirField.textChanged.emit(self.dirField.text())

        fileFieldExp = QRegExp("^$|.{1,30}")
        fileValidator = QRegExpValidator(fileFieldExp, self.fileField)
        self.fileField.setValidator(fileValidator)
        self.fileField.textChanged.connect(self.validateServerFormOnChange)
        self.fileField.textChanged.emit(self.fileField.text())

        mailFieldExp = QRegExp(self.mailRegex())
        mailusernameValidator = QRegExpValidator(mailFieldExp, self.mailField)
        self.mailField.setValidator(mailusernameValidator)
        self.mailField.textChanged.connect(self.validateServerFormOnChange)
        self.mailField.textChanged.emit(self.mailField.text())

        addButton = QPushButton(formwidget)
        addButton.setText('Save Server')
        formLayout.setWidget(7, QFormLayout.FieldRole, addButton)

        addButton.clicked.connect(lambda: self.saveServer(hostServer))
        self.qdialog.exec_()

    def saveServer(self, hostValue):
        newServerData = {
            'hostname': self.hostnameField.text(),
            'username': self.usernameField.text(),
            'password': self.passwordField.text(),
            'port': self.portField.text(),
            'dir' : self.dirField.text(),
            'mail':self.mailField.text(),
        }

        if not self.validateServerFormOnSubmit(newServerData):
            reply = None
            ssh, error = self.ssh.checkHost(newServerData)
            ssh.close()
            pwd = self.constant.encryptpwd(newServerData['password'])
            newServerData['password'] = pwd
            newServerData['fwatcher'] = ''
            newServerData['is_watching'] = 'No'
            newServerData['file_name'] = self.fileField.text()
            # newServerData['email'] = self.mailField.text()

            if error:
                reply = QMessageBox.question(self.mainWindow, 'Message',
                                             "Failed to connect the server <b>" + newServerData[
                                                 'hostname'] + "</b>, Still wanna save the server details?",
                                             QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes or not error:
                if hostValue:
                    newServerData['did'] = hostValue['did']
                    self.dbHandler.editData(newServerData)
                else:
                    self.dbHandler.saveData(newServerData)
                self.generateTree()
                self.qdialog.close()
                QMessageBox.information(self.mainWindow, 'Warning', "Server details has been saved successfully",
                                        QMessageBox.Ok)

    def removeServer(self):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()

        reply = QMessageBox.question(self.mainWindow, 'Message',
                                     "Deleting the group <b>" + hostname + "</b> delete all server from it, are you sure wanna do it?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.dhandler.deleteHostData(hostname)
            self.generateTree()

    def addMailConfig(self, mailServer = {}):
        self.qdialog = QDialog()
        self.qdialog.setWindowTitle("Add Server Details")
        self.qdialog.setWindowModality(Qt.ApplicationModal)
        self.qdialog.setFixedSize(300, 280)
        formwidget = QWidget(self.qdialog)
        formLayout = QFormLayout(formwidget)

        smtpLabel = QLabel(formwidget)
        smtpLabel.setText("SMTP")
        smtpLabel.setToolTip('SMTP')
        formLayout.setWidget(0, QFormLayout.LabelRole, smtpLabel)

        portLabel = QLabel(formwidget)
        portLabel.setText("SMTP Port")
        portLabel.setToolTip('SMTP Port')
        formLayout.setWidget(1, QFormLayout.LabelRole, portLabel)

        senderLabel = QLabel(formwidget)
        senderLabel.setText("Email")
        senderLabel.setToolTip('Email')
        formLayout.setWidget(2, QFormLayout.LabelRole, senderLabel)

        pwdLabel = QLabel(formwidget)
        pwdLabel.setText("Password")
        pwdLabel.setToolTip('Password')
        formLayout.setWidget(3, QFormLayout.LabelRole, pwdLabel)
        recLabel = QLabel(formwidget)
        recLabel.setText("Receiver")
        recLabel.setToolTip('Receiver')
        formLayout.setWidget(4, QFormLayout.LabelRole, recLabel)
        subLabel = QLabel(formwidget)
        subLabel.setText("Subject")
        subLabel.setToolTip('Subject')
        formLayout.setWidget(5, QFormLayout.LabelRole, subLabel)

        self.smtpField = QLineEdit(formwidget)
        formLayout.setWidget(0, QFormLayout.FieldRole, self.smtpField)
        self.smtpPortField = QLineEdit(formwidget)
        formLayout.setWidget(1, QFormLayout.FieldRole, self.smtpPortField)
        self.smtpMailField = QLineEdit(formwidget)
        formLayout.setWidget(2, QFormLayout.FieldRole, self.smtpMailField)
        self.mailPwdField = QLineEdit(formwidget)
        self.mailPwdField.setEchoMode(QLineEdit.Password)
        formLayout.setWidget(3, QFormLayout.FieldRole, self.mailPwdField)
        self.receiverField = QLineEdit(formwidget)
        formLayout.setWidget(4, QFormLayout.FieldRole, self.receiverField)
        self.subjectField = QLineEdit(formwidget)
        formLayout.setWidget(5, QFormLayout.FieldRole, self.subjectField)

        if ('smtp' in mailServer):
            self.smtpField.setText(mailServer['smtp'])
        if ('smtpPort' in mailServer):
            self.smtpPortField.setText(str(mailServer['smtpPort']))
        if ('smtpMail' in mailServer):
            self.smtpMailField.setText(mailServer['smtpMail'])
        if ('mailPwd' in mailServer):
            self.mailPwdField.setText(mailServer['mailPwd'])
        if ('receiver' in mailServer):
            self.receiverField.setText(mailServer['receiver'])
        if ('subject' in mailServer):
            self.subjectField.setText(mailServer['subject'])

        smtpExp = QRegExp(".{1,30}")
        hostnameValidator = QRegExpValidator(smtpExp, self.smtpField)
        self.smtpField.setValidator(hostnameValidator)
        self.smtpField.textChanged.connect(self.validateServerFormOnChange)
        self.smtpField.textChanged.emit(self.smtpField.text())

        portExp = QRegExp(".{1,30}")
        portValidator = QRegExpValidator(portExp, self.smtpPortField)
        self.smtpPortField.setValidator(portValidator)
        self.smtpPortField.textChanged.connect(self.validateServerFormOnChange)
        self.smtpPortField.textChanged.emit(self.smtpPortField.text())

        mailFieldExp = QRegExp(self.mailMandatoryRegex())
        mailValidator = QRegExpValidator(mailFieldExp, self.smtpMailField)
        self.smtpMailField.setValidator(mailValidator)
        self.smtpMailField.textChanged.connect(self.validateServerFormOnChange)
        self.smtpMailField.textChanged.emit(self.smtpMailField.text())

        passwordExp = QRegExp(".{1,30}")
        passwordValidator = QRegExpValidator(passwordExp, self.mailPwdField)
        self.mailPwdField.setValidator(passwordValidator)
        self.mailPwdField.textChanged.connect(self.validateServerFormOnChange)
        self.mailPwdField.textChanged.emit(self.mailPwdField.text())

        mailReceiverValidator = QRegExpValidator(mailFieldExp, self.receiverField)
        self.receiverField.setValidator(mailReceiverValidator)
        self.receiverField.textChanged.connect(self.validateServerFormOnChange)
        self.receiverField.textChanged.emit(self.receiverField.text())

        subValidator = QRegExpValidator(smtpExp, self.subjectField)
        self.subjectField.setValidator(subValidator)
        self.subjectField.textChanged.connect(self.validateServerFormOnChange)
        self.subjectField.textChanged.emit(self.subjectField.text())

        addButton = QPushButton(formwidget)
        addButton.setText('Save')
        formLayout.setWidget(7, QFormLayout.FieldRole, addButton)

        addButton.clicked.connect(lambda: self.saveMail(mailServer))
        self.qdialog.exec_()


    def saveMail(self, mailValue):
        newServerData = {
            'smtp': self.smtpField.text(),
            'smtpPort': self.smtpPortField.text(),
            'smtpMail': self.smtpMailField.text(),
            'mailPwd': self.mailPwdField.text(),
            'receiver': self.receiverField.text(),
            'subject':self.subjectField.text()
        }
        if not self.validateServerFormOnSubmit(newServerData):
            server, error = self.ssh.mailCheck(newServerData)
            if error:
                QMessageBox.question(self.mainWindow, 'Message',
                                             "Failed to authenticate <b>" + newServerData[
                                                 'smtpMail'] + "</b>, Please enter the valid data.",
                                             QMessageBox.Ok)
            else:
                if mailValue:
                    self.dbHandler.updateMailData(mailValue['smtpMail'], newServerData)
                else:
                    self.dbHandler.saveMailData(newServerData)
                self.qdialog.close()
                QMessageBox.information(self.mainWindow, 'Warning', "Mail details has been saved successfully",
                                        QMessageBox.Ok)

    def domainOrIpRegex(self):
        ip = "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
        domain = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
        return ip

    def mailRegex(self):
        m = "^$|^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
        return m

    def mailMandatoryRegex(self):
        m = "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
        return m

    def portRegex(self):
        return "([0-9]{0,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"

    def validateServerFormOnChange(self, *args, **kwargs):

        sender = self.mainWindow.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b' # green
        elif state == QValidator.Intermediate:
            color = '#ffffff' # yellow
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)


    def validateServerFormOnSubmit(self, fields):
        states = []

        for field in fields:
            fieldObj = getattr(self, field + "Field")
            if isinstance(fieldObj, QLineEdit):
                if field == 'mail':
                    if fieldObj.text() == '':
                        continue
                state = fieldObj.validator().validate(fieldObj.text(), 0)[0]
                if state == QValidator.Acceptable:
                    color = '#c4df9b'  # green
                elif state == QValidator.Intermediate:
                    states.append(field)
                    color = '#f6989d'  # yellow
                else:
                    color = '#f6989d'  # red
                    states.append(field)
                fieldObj.setStyleSheet('QLineEdit { background-color: %s }' % color)

        return states
