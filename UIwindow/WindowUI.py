import sys, os, inspect
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
import json
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from DHandler import *
from HostSSH import SSHClient
from jinja2 import *
from Constant import *

class UiSample(object):
    width = 900
    height = 700
    widgetData = {}
    prevDockWidget = None

    def __init__(self):
        super(UiSample, self).__init__()
        self.dbHandler = DbHandler()
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
        self.sshMenubar()
        self.mainWindow.setMenuBar(self.menubar)

    def serverMenu(self):
        menuServer = QMenu(self.menubar)
        menuServer.setTitle("Server")
        menuServer.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
        menuServer.addSeparator()
        menuServer.addAction("Exit", self.exitApp)
        self.menubar.addAction(menuServer.menuAction())

    def sshMenubar(self):
        menuSsh = QMenu(self.menubar)
        menuSsh.setTitle("SSH")
        menuSsh.addSeparator()
        menuSsh.addAction("About", self.aboutMenu)
        menuSsh.addSeparator()
        menuSsh.addAction("Help", self.helpMenu)
        self.menubar.addAction(menuSsh.menuAction())

    def exitApp(self):
        sys.exit()

    def aboutMenu(self):
        print 'about'

    def helpMenu(self):
        print 'help'

    def treeViewWidget(self):
        # hbox = QHBoxLayout(self.mainWindow)
        # dockWidget = QDockWidget()
        # dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        qwidget = QWidget()
        hbox = QHBoxLayout()
        self.leftFrame = QFrame()
        self.treeView = QTreeView()
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
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.treeView)
        qwidget.setLayout(leftLayout)

        self.rightWidget = QWidget()
        formLayout = QFormLayout(self.rightWidget)
        titleLabel = QLabel("== Server Details ==")
        formLayout.setWidget(0, QFormLayout.LabelRole, titleLabel)
        nameLabel = QLabel("Host Server:")
        formLayout.setWidget(1, QFormLayout.LabelRole, nameLabel)
        self.hostEdit = QLabel()
        formLayout.setWidget(1, QFormLayout.FieldRole, self.hostEdit)
        userLabel = QLabel("Username:")
        formLayout.setWidget(2, QFormLayout.LabelRole, userLabel)
        self.unameEdit = QLabel()
        formLayout.setWidget(2, QFormLayout.FieldRole, self.unameEdit)
        pwdLabel = QLabel("Password:")
        formLayout.setWidget(3, QFormLayout.LabelRole, pwdLabel)
        self.pwdEdit = QLabel()
        self.pwdEdit.setText("*******")
        formLayout.setWidget(3, QFormLayout.FieldRole, self.pwdEdit)

        portLabel = QLabel("Port:")
        formLayout.setWidget(4, QFormLayout.LabelRole, portLabel)
        self.portEdit = QLabel()
        formLayout.setWidget(4, QFormLayout.FieldRole, self.portEdit)

        dirLabel = QLabel("Directory Path:")
        formLayout.setWidget(5, QFormLayout.LabelRole, dirLabel)
        self.dirEdit = QLabel()
        formLayout.setWidget(5, QFormLayout.FieldRole, self.dirEdit)

        fileLabel = QLabel("File  Path:")
        formLayout.setWidget(6, QFormLayout.LabelRole, fileLabel)
        self.fileEdit = QLabel()
        formLayout.setWidget(6, QFormLayout.FieldRole, self.fileEdit)

        mailLabel = QLabel("Email:")
        formLayout.setWidget(7, QFormLayout.LabelRole, mailLabel)
        self.mailEdit = QLabel()
        formLayout.setWidget(7, QFormLayout.FieldRole, self.mailEdit)

        self.rightWidget.setLayout(formLayout)
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
        if level == 0:
            menu.addAction("Add Server", self.addServer).setObjectName('MainMenuAddServer')
            menu.addSeparator()
            menu.addAction("Remove Group", self.removeServer)
            menu.addAction("Run")
            # menu.addAction("Summary")
            # menu.addAction("Ftp")
            menu.addSeparator()
            menu.addAction("Edit Server")
        elif level == 1:
            menu.addAction("Summary")
            menu.addAction("Ftp")
            menu.addSeparator()
            menu.addAction("Edit Server")
            menu.addAction("Remove Server")
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def doubleClicked(self, name):
        print name
        self.rightWidget.setVisible(True)
        self.hostEdit.setText(name)
        dataHost = self.dbHandler.getSeverByGroup(name)
        self.unameEdit.setText(dataHost[0][2])
        self.portEdit.setText(str(dataHost[0][4]))
        self.dirEdit.setText(dataHost[0][5])
        self.fileEdit.setText(dataHost[0][6])
        self.mailEdit.setText(dataHost[0][7])

        '''def docker(self, tabName):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()
        self.statusbar.showMessage("Connecting to " + hostname)
        self.dataHost = DbHandler().getSeverByGroup(hostname)
        hostdata = {'hostname':self.dataHost[0][1],
                    'username':self.dataHost[0][2],
                    'password':HostConstant().decryptpwd(self.dataHost[0][3])
                    }
        ssh, error = SSHClient().checkHost(hostdata)

        if error:
            self.statusbar.showMessage("Failed to connect " + self.dataHost[0][1])
        else:
            if self.dataHost[0][1] not in self.widgetData:
                dockWidget = QDockWidget(self.dataHost[0][1])
                dockWidget.setAllowedAreas(Qt.RightDockWidgetArea)

                self.mainWindow.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

                if self.prevDockWidget:
                    self.mainWindow.tabifyDockWidget(self.prevDockWidget, dockWidget)
                else:
                    self.prevDockWidget = dockWidget

                tabWidget = QTabWidget()
                tabWidget.setObjectName("tabWidget")
                tabWidget.setTabsClosable(True)
                tabWidget.tabCloseRequested.connect(self.tabberClose)
                dockWidget.setWidget(tabWidget)

                self.widgetData[self.dataHost[0][1]] = {}
                self.widgetData[self.dataHost[0][1]]['dock'] = dockWidget
                self.widgetData[self.dataHost[0][1]]['tab'] = tabWidget
                self.widgetData[self.dataHost[0][1]]['ssh'] = ssh
                self.statusbar.showMessage("Connected to " + self.dataHost[0][1])
            else:
                dockWidget = self.widgetData[self.dataHost[0][1]]['dock']

            dockWidget.setVisible(True)
            dockWidget.setFocus()
            dockWidget.raise_()
            dockWidget.show()
            # self.mainWindow.addDockWidget(Qt.RohjDockWidgetArea, dockWidget)
            self.tabber(tabName)

    def tabber(self, name):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()

        currentData = {'hostname':self.dataHost[0][1],
                    'username':self.dataHost[0][2],
                    'password':HostConstant().decryptpwd(self.dataHost[0][3])
                    }
        tabWidget = self.widgetData[currentData['hostname']]['tab']

        if name not in self.widgetData[currentData['hostname']]:
            tab = QWidget()
            tabWidget.addTab(tab, name.title())
            self.widgetData[currentData['hostname']][name] = tab
        else:
            tab = self.widgetData[currentData['hostname']][name]
            tabWidget.addTab(tab, name.title())

        tabWidget.setCurrentWidget(tab)
        tab.show()

    def tabberClose(self, i):
        pos = QCursor.pos()
        widgets = qApp.widgetAt(pos)
        widgets.parentWidget().parentWidget().removeTab(i)'''

    # def currentData(self, hostname):
    #     return self.dbHandler.getSeverByGroup(hostname)

    def statusBar(self):
        self.statusbar = QStatusBar(self.mainWindow)
        self.mainWindow.setStatusBar(self.statusbar)

    def render(self, fileName, data):
        currentDirectoryPath = os.path.dirname(os.path.realpath(__file__))
        templatePath = currentDirectoryPath + '/templates/'
        staticPath = 'file://' + currentDirectoryPath + '/static/'

        env = Environment(
            loader=FileSystemLoader(templatePath)
        )

        template = env.get_template(fileName)
        html = template.render(data, staticPath=staticPath)
        return html