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
# from jinja2 import *
from Constant import *
from progress.progress import *

class Job(QRunnable):
    event = True
    def __init__(self, data, sftp, runall):
        super(Job, self).__init__()
        self.ssh = SSHClient()
        self.data = data
        self.sftp = sftp
        self.runall = runall

    def run(self):
        try:
            if self.runall is None:
                while self.event:
                    print 'loading'
                    # self.ssh.checkFileEntries(self.data, self.sftp)
                    self.ssh.connect_host(self.data)
                    time.sleep(10)
            else:
                while self.event:
                    print 'loading'
                    # self.ssh.checkFileEntries(self.data, self.sftp)
                    self.ssh.calculateParallel(self.data, len(self.data))
                    time.sleep(10)
        except Exception as e:
            print e

    def stopRun(self):
        if self.event:
            self.event = False
        print 'stopped'

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
        self.windowSubWidget()
        self.statusBar()

        QMetaObject.connectSlotsByName(self.mainWindow)
        self.mainWindow.show()

    def menuBar(self):
        self.menubar = QMenuBar(self.mainWindow)
        self.menubar.setObjectName("menubar")
        self.relinAllMenu()
        self.serverMenu()
        self.mailSetupMenubar()
        self.mainWindow.setMenuBar(self.menubar)

    def relinAllMenu(self):
        menuRelin = QMenu(self.menubar)
        menuRelin.setTitle("RelinAll")
        menuRelin.addAction("About")
        menuRelin.addSeparator()
        menuRelin.addAction("Exit", self.exitApp)
        self.menubar.addAction(menuRelin.menuAction())

    def serverMenu(self):
        menuServer = QMenu(self.menubar)
        menuServer.setTitle("Server")
        menuServer.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
        menuServer.addSeparator()
        count = self.dbHandler.readHostCountData()
        if count > 1:
            menuServer.addAction("Run All")
        self.menubar.addAction(menuServer.menuAction())

    def mailSetupMenubar(self):
        menuSsh = QMenu(self.menubar)
        menuSsh.setTitle("Mail")
        menuSsh.addSeparator()
        menuSsh.addAction("Setup", self.mailSetup)
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

    def windowSubWidget(self):
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
        self.rightWidget.setStyleSheet("background-color: white")
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.qbtnWidget = QWidget()
        qbtnLayout = QVBoxLayout()
        self.qHostTable = QTableWidget()
        self.qHostTable.setStyleSheet("QTableView { border: none;}")

        hdetails = self.dbHandler.selectHostDetail()
        self.qHostTable.setRowCount(len(hdetails))
        self.qHostTable.setColumnCount(3)
        self.qHostTable.verticalHeader().hide()
        self.qHostTable.setHorizontalHeaderLabels(['Server', 'Username', 'Status'])
        for index, element in enumerate(hdetails):
            btn_edit = QPushButton()
            btn_edit.setText(element['hostname'])
            btn_edit.clicked.connect(self.hostBtn)
            self.qHostTable.setCellWidget(index, 0, btn_edit)
            self.qHostTable.setItem(index, 1, QTableWidgetItem(element['username']))
            self.qHostTable.setItem(index, 2, QTableWidgetItem(element['iswatch']))

        self.qHostTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.qHostTable.resizeColumnsToContents()
        self.qHostTable.cellClicked.connect(self.cellClick)
        qbutton = QPushButton('click')
        qbutton.clicked.connect(lambda:self.whichbtn('test'))
        qbtnLayout.addWidget(qbutton)
        qbtnLayout.addWidget(self.qHostTable)
        self.qbtnWidget.setLayout(qbtnLayout)
        self.qbtnWidget.setVisible(True)
        # layout.addWidget(self.qbtnWidget)

        ###
        title = QLabel('----- Summary -----')
        self.qboxWidget = QWidget()
        boxlayout = QVBoxLayout()
        boxlayout.addWidget(title)
        self.qboxWidget.setLayout(boxlayout)
        qtableWidget = QWidget()
        qtableLayout = QHBoxLayout()
        self.tableHostWidget = QTableWidget()
        self.tableHostWidget.setStyleSheet("QTableView { border: none;}")
        qtableLayout.addWidget(self.tableHostWidget)
        qtableWidget.setLayout(qtableLayout)
        layout.setContentsMargins(10,10,0,0)
        layout.addWidget(self.qboxWidget, 0, Qt.AlignTop)
        layout.addWidget(self.tableHostWidget, 1, Qt.AlignTop)
        self.qsummarywidget = QWidget()
        qsummarybox = QVBoxLayout()
        self.tableSummaryWidget = QTableWidget()
        self.tableSummaryWidget.setStyleSheet("QTableView { border: none;}")
        qsummarybox.addWidget(self.tableSummaryWidget)
        currentPath = os.path.dirname(__file__)
        gifPath = currentPath + "/searching.gif"
        self.progressLabel = QTextMovieLabel('Watching...', gifPath)
        qsummarybox.addWidget(self.progressLabel)
        self.progressLabel.setVisible(False)
        self.qsummarywidget.setLayout(qsummarybox)
        layout.addWidget(self.qsummarywidget, 2, Qt.AlignTop)
        self.qboxWidget.setVisible(False)
        self.tableHostWidget.setVisible(False)
        self.qsummarywidget.setVisible(False)
        #####
        layout.addWidget(self.qbtnWidget)
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

    def cellClick(self, row, col):
        print "Click on " + str(row) + " " + str(col)

    def hostBtn(self):
        hdetails = self.dbHandler.selectHostDetail()
        clickme = qApp.focusWidget()
        index = self.qHostTable.indexAt(clickme.pos())
        if index.isValid():
            print (index.row(), index.column())
            hosts = hdetails[index.row()]
            self.qbtnWidget.setVisible(False)
            self.qHostTable.setVisible(False)
            self.qboxWidget.setVisible(True)
            self.tableHostWidget.setVisible(True)
            self.qsummarywidget.setVisible(True)
            self.doubleClicked(hosts['hostname'])

    def whichbtn(self,test):
        print 'clicked'
        self.qbtnWidget.setVisible(False)
        self.qboxWidget.setVisible(True)
        self.tableHostWidget.setVisible(True)
        self.qsummarywidget.setVisible(True)

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()
        print len(indexes)
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        hserver = self.getHostServer()
        if level == 0:
            if hserver['iswatch'] == 'No':
                menu.addAction("Run", self.runServer)
            else:
                menu.addAction("Stop", self.stopServer)
            menu.addSeparator()
            menu.addAction("View", self.summary)
            menu.addAction("Edit Server")
            menu.addAction("Remove", self.removeServer)
            menu.addAction("Edit Server", self.editServer)
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def selectAllHosts(self):
        self.treeView.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.treeView.selectAll()

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

        if hostServer['iswatch'] == 'Yes':
            self.progressLabel.setVisible(True)
        else:
            self.progressLabel.setVisible(False)
        hostServer['password'] = self.constant.decryptpwd(hostServer['password'])
        self.sshClient, error = self.ssh.checkHost(hostServer)

        if error is None:
            self.hostname(self.sshClient)
            self.uptime(self.sshClient)
            self.kernelname(self.sshClient)
            self.kernelrelease(self.sshClient)
            self.osname(self.sshClient)
            self.processor(self.sshClient)
            self.sshClient.close()
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
        self.job = Job(hostServer, None, None)
        QThreadPool.globalInstance().start(self.job)
        self.dbHandler.updateFileData('', 'Yes', hostServer['hostname'])
        self.doubleClicked(hostServer['hostname'])

    def runAllServer(self):
        hdetails = self.dbHandler.selectHostDetail()
        self.job = Job(hdetails, None, True)
        QThreadPool.globalInstance().start(self.job)

    def stopServer(self):
        hostServer = self.getHostServer()
        self.dbHandler.updateFileData('','No', hostServer['hostname'])
        self.doubleClicked(hostServer['hostname'])
        self.job.stopRun()
        # self.sshHost.close()
        # self.sftp.close()

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