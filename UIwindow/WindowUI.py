import sys, os, inspect
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from PyQt5 import QtCore
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from DHandler import *
from HostSSH import SSHClient
from jinja2 import *
from Constant import *

class Job(QRunnable):
    event = True
    def __init__(self, data, sftp):
        super(Job, self).__init__()
        self.ssh = SSHClient()
        self.data = data
        self.sftp = sftp

    def run(self):
        while self.event:
            time.sleep(3)
            print 'hello'
            self.ssh.checkFileEntries(self.data, self.sftp)
    def stopRun(self):
        self.event = False
        self.sftp.close()

class UiSample(object):
    width = 900
    height = 700
    detail = {}
    spinner = None
    nilServer = None

    def __init__(self):
        super(UiSample, self).__init__()
        self.dbHandler = DbHandler()
        self.ssh = SSHClient()
        self.constant = HostConstant()
        self.initUI()

    def initUI(self):
        self.mainWindow = QMainWindow()
        self.mainWindow.resize(self.width, self.height)
        # self.mainWindow.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)

        self.menuBar()
        self.treeViewWidget()
        self.statusBar()

        QMetaObject.connectSlotsByName(self.mainWindow)
        self.mainWindow.show()

    def menuBar(self):
        self.menubar = QMenuBar(self.mainWindow)
        self.menubar.setObjectName("menubar")
        self.serverMenu()
        self.mailSetupMenubar()
        self.sshMenubar()
        self.mainWindow.setMenuBar(self.menubar)

    def serverMenu(self):
        menuServer = QMenu(self.menubar)
        menuServer.setTitle("Server")
        menuServer.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
        menuServer.addSeparator()
        menuServer.addAction("Exit", self.exitApp)
        self.menubar.addAction(menuServer.menuAction())

    def mailSetupMenubar(self):
        menuSsh = QMenu(self.menubar)
        menuSsh.setTitle("Mail")
        menuSsh.addSeparator()
        menuSsh.addAction("Setup", self.mailSetup)
        self.menubar.addAction(menuSsh.menuAction())

    def sshMenubar(self):
        menuSsh = QMenu(self.menubar)
        menuSsh.setTitle("SSH")
        menuSsh.addSeparator()
        menuSsh.addAction("About", self.aboutMenu)
        menuSsh.addSeparator()
        menuSsh.addAction("Help", self.helpMenu)
        self.menubar.addAction(menuSsh.menuAction())

    def mailSetup(self):
        mailData = self.dbHandler.readMailData()
        if mailData is None:
            self.addMailConfig()
        else:
            self.addMailConfig(mailData)

    def exitApp(self):
        sys.exit()

    def aboutMenu(self):
        print 'about'

    def helpMenu(self):
        print 'help'

    def treeViewWidget(self):
        qwidget = QWidget()
        hbox = QHBoxLayout()
        self.leftFrame = QFrame()
        self.treeView = QTreeView()
        self.treeView.setStyleSheet("""
        .QTreeView {
            color: blue;
        }
        .QTreeView::item:selected {
            color: black;
        }
        QTreeView::branch {
            background-color: white;
        }""")
        self.treeView.setMaximumSize(QSize(200, 16777215))
        self.treeView.setGeometry(QRect(10, 10, 200, self.height))
        self.treeView.setObjectName("treeView")
        self.treeView.setSortingEnabled(True)
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setExpandsOnDoubleClick(True)
        self.treeView.setAnimated(True)
        self.treeView.setWordWrap(True)
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.doubleClicked.connect(self.summary)
        self.treeView.setAlternatingRowColors(True)
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.treeView)
        qwidget.setLayout(leftLayout)

        self.rightWidget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel('----- Summary -----')
        qboxWidget = QWidget()
        boxlayout = QVBoxLayout()
        boxlayout.addWidget(title)
        qboxWidget.setLayout(boxlayout)

        qtableWidget = QWidget()
        qtableLayout = QHBoxLayout()
        self.tableHostWidget = QTableWidget()
        qtableLayout.addWidget(self.tableHostWidget)
        qtableWidget.setLayout(qtableLayout)
        layout.setContentsMargins(10,10,0,0)

        layout.addWidget(qboxWidget, 0, Qt.AlignTop)
        layout.addWidget(self.tableHostWidget, 1, Qt.AlignTop)
        layout.addWidget(player, 2, Qt.AlignTop)

        self.tableSummaryWidget = QTableWidget()
        layout.addWidget(self.tableSummaryWidget, 2, Qt.AlignTop)
        self.rightWidget.setLayout(layout)

        self.rightWidget.setVisible(False)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(qwidget)
        splitter.addWidget(self.rightWidget)
        splitter.setSizes([50, 250])
        hbox.addWidget(splitter)
        centerWidget = QWidget()
        centerWidget.setLayout(hbox)
        self.mainWindow.setCentralWidget(centerWidget)

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        hserver = self.getHostServer()
        if level == 0:
            menu.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
            menu.addSeparator()
            menu.addAction("Remove Group", self.removeServer)
            if hserver['iswatch'] == 'No':
                menu.addAction("Run", self.runServer)
            else:
                menu.addAction("Stop", self.stopServer)
            menu.addSeparator()
            menu.addAction("Edit Server", self.editServer)
        elif level == 1:
            menu.addAction("Summary")
            menu.addAction("Ftp")
            menu.addSeparator()
            menu.addAction("Edit Server")
            menu.addAction("Remove Server")
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def doubleClicked(self, name):
        self.rightWidget.setVisible(True)
        hostServer = self.dbHandler.getHostDetail(name)
        self.tableHostWidget.setRowCount(6)
        self.tableHostWidget.setColumnCount(2)

        self.tableHostWidget.setHorizontalHeaderLabels(['Data', 'Detail'])
        self.tableHostWidget.horizontalHeader().hide()
        self.tableHostWidget.verticalHeader().hide()

        self.tableHostWidget.setItem(0, 0, QTableWidgetItem("Host server"))
        self.tableHostWidget.setItem(0, 1, QTableWidgetItem(hostServer['hostname']))
        self.tableHostWidget.setItem(1, 0, QTableWidgetItem("Username"))
        self.tableHostWidget.setItem(1, 1, QTableWidgetItem(hostServer['username']))
        self.tableHostWidget.setItem(2, 0, QTableWidgetItem("Port"))
        self.tableHostWidget.setItem(2, 1, QTableWidgetItem(str(hostServer['port'])))
        self.tableHostWidget.setItem(3, 0, QTableWidgetItem("Directory Path"))
        self.tableHostWidget.setItem(3, 1, QTableWidgetItem(hostServer['dir']))
        self.tableHostWidget.setItem(4, 0, QTableWidgetItem("File Name"))
        self.tableHostWidget.setItem(4, 1, QTableWidgetItem(hostServer['file_name']))
        self.tableHostWidget.setItem(4, 0, QTableWidgetItem("Email"))
        self.tableHostWidget.setItem(4, 1, QTableWidgetItem(hostServer['mail']))
        self.tableHostWidget.setItem(5, 0, QTableWidgetItem("Is Watching"))
        self.tableHostWidget.setItem(5, 1, QTableWidgetItem(hostServer['iswatch']))

        self.tableHostWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableHostWidget.resizeColumnsToContents()
        self.tableHostWidget.setMaximumHeight(185)
        self.tableHostWidget.setMaximumWidth(350)

        hostServer['password'] = self.constant.decryptpwd(hostServer['password'])
        self.sshClient, error = self.ssh.checkHost(hostServer)

        if error is None:
            self.hostname(self.sshClient)
            self.uptime(self.sshClient)
            self.kernelname(self.sshClient)
            self.kernelrelease(self.sshClient)
            self.osname(self.sshClient)
            self.processor(self.sshClient)

            self.tableSummaryWidget.setRowCount(5)
            self.tableSummaryWidget.setColumnCount(2)
            self.tableSummaryWidget.setHorizontalHeaderLabels(['Data', 'Detail'])
            self.tableSummaryWidget.horizontalHeader().hide()
            self.tableSummaryWidget.verticalHeader().hide()
            self.tableSummaryWidget.setItem(0, 0, QTableWidgetItem("Host Name"))
            self.tableSummaryWidget.setItem(0, 1, QTableWidgetItem(self.detail['hostname']))
            self.tableSummaryWidget.setItem(1, 0, QTableWidgetItem("Uptime"))
            self.tableSummaryWidget.setItem(1, 1, QTableWidgetItem(self.detail['uptime']))

            self.tableSummaryWidget.setItem(2, 0, QTableWidgetItem("Kernal Name"))
            self.tableSummaryWidget.setItem(2, 1, QTableWidgetItem(self.detail['kernelname']))
            self.tableSummaryWidget.setItem(3, 0, QTableWidgetItem("Kernal Release"))
            self.tableSummaryWidget.setItem(3, 1, QTableWidgetItem(self.detail['kernelrelease']))
            self.tableSummaryWidget.setItem(4, 0, QTableWidgetItem("OS Name"))
            self.tableSummaryWidget.setItem(4, 1, QTableWidgetItem(self.detail['osname']))
            self.tableSummaryWidget.setItem(4, 0, QTableWidgetItem("Processor"))
            self.tableSummaryWidget.setItem(4, 1, QTableWidgetItem(self.detail['processor']))
            self.tableSummaryWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableSummaryWidget.resizeColumnsToContents()
            self.tableSummaryWidget.setMaximumHeight(170)
            self.tableSummaryWidget.setMaximumWidth(400)

    def runServer(self):
        hostServer = self.getHostServer()
        self.dbHandler.updateFileData('','Yes', hostServer['hostname'])
        self.doubleClicked(hostServer['hostname'])
        sftp = self.ssh.check_host_server(self.sshClient)
        self.job = Job(hostServer, sftp)
        QThreadPool.globalInstance().start(self.job)

    def stopServer(self):
        hostServer = self.getHostServer()
        self.job.stopRun()
        self.sshClient.close()
        self.dbHandler.updateFileData('','No', hostServer['hostname'])
        print 'test'
        self.doubleClicked(hostServer['hostname'])

    def getHostServer(self):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()
        return  self.dbHandler.getHostDetail(hostname)

    def statusBar(self):
        self.statusbar = QStatusBar(self.mainWindow)
        self.mainWindow.setStatusBar(self.statusbar)

    # def render(self, fileName, data):
    #     currentDirectoryPath = os.path.dirname(os.path.realpath(__file__))
    #     templatePath = currentDirectoryPath + '/templates/'
    #     staticPath = 'file://' + currentDirectoryPath + '/static/'
    #
    #     env = Environment(
    #         loader=FileSystemLoader(templatePath)
    #     )
    #
    #     template = env.get_template(fileName)
    #     html = template.render(data, staticPath=staticPath)
    #     return html