from UIwindow.WindowUI import *

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

    def addServer(self):
        if self.mainWindow.sender().objectName() == 'MainMenuAddServer':
            self.serverDialog()

    def serverDialog(self):
        self.qdialog = QDialog()
        self.qdialog.setWindowTitle("Add Server Details")
        self.qdialog.setWindowModality(Qt.ApplicationModal)
        self.qdialog.setFixedSize(300, 220)

        formwidget = QWidget(self.qdialog)
        formLayout = QFormLayout(formwidget)

        groupLabel = QLabel(formwidget)
        groupLabel.setText('Group Name')
        formLayout.setWidget(0, QFormLayout.LabelRole, groupLabel)
        hostLabel = QLabel(formwidget)
        hostLabel.setText("Hostname/IP")
        formLayout.setWidget(1, QFormLayout.LabelRole, hostLabel)
        userLabel = QLabel(formwidget)
        userLabel.setText("Username: ")
        formLayout.setWidget(2, QFormLayout.LabelRole, userLabel)
        pwdLabel = QLabel(formwidget)
        pwdLabel.setText("Password: ")
        formLayout.setWidget(3, QFormLayout.LabelRole, pwdLabel)
        portLabel = QLabel(formwidget)
        portLabel.setText("Port: ")
        formLayout.setWidget(4, QFormLayout.LabelRole, portLabel)

        self.groupnameField = QLineEdit(formwidget)
        formLayout.setWidget(0, QFormLayout.FieldRole, self.groupnameField)
        self.hostnameField = QLineEdit(formwidget)
        formLayout.setWidget(1, QFormLayout.FieldRole, self.hostnameField)
        self.usernameField = QLineEdit(formwidget)
        formLayout.setWidget(2, QFormLayout.FieldRole, self.usernameField)
        self.passwordField = QLineEdit(formwidget)
        self.passwordField.setEchoMode(QLineEdit.Password)
        formLayout.setWidget(3, QFormLayout.FieldRole, self.passwordField)
        self.portField = QLineEdit(formwidget)
        self.portField.setText('22')
        formLayout.setWidget(4, QFormLayout.FieldRole, self.portField)

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

        addButton = QPushButton(formwidget)
        addButton.setText('Save Server')
        formLayout.setWidget(5, QFormLayout.FieldRole, addButton)

        addButton.clicked.connect(self.saveServer)

        self.qdialog.exec_()

    def saveServer(self):
        groupname = self.groupnameField.text()
        newServerData = {
            # 'groupname': groupname,
            'hostname': self.hostnameField.text(),
            'username': self.usernameField.text(),
            'password': self.passwordField.text(),
            'port': self.portField.text()
        }

        if not self.validateServerFormOnSubmit(newServerData):
            reply = None
            sshclient= self.ssh.checkHost(newServerData['hostname'], newServerData['username'],
                                     newServerData['password'])

            if sshclient == 'Error':
                reply = QMessageBox.question(self.mainWindow, 'Message',
                                             "Failed to connect the server <b>" + newServerData[
                                                 'hostname'] + "</b>, Still wanna save the server details?",
                                             QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                pwd =  self.constant.encryptpwd(newServerData['password'])
                obj = DataObj(None, newServerData['hostname'], newServerData['username'], pwd, newServerData['port'], '/home/ravi/sample', '', '', '')
                self.dbHandler.saveData(obj)

                # self.dbHandler.insertServer(newServerData)
                self.generateTree()

                # modelIndex = self.serverData.findItems(newServerData['groupname'])[0].index()
                # self.treeView.expand(modelIndex)

                self.qdialog.close()
                QMessageBox.information(self.mainWindow, 'Warning', "Server details has been saved successfully",
                                        QMessageBox.Ok)

    def domainOrIpRegex(self):
        ip = "(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
        domain = "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])"
        return ip

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
