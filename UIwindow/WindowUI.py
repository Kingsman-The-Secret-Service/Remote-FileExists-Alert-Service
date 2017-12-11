import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import  *
from DHandler import *
import json
from HostSSH import SSHClient

class UiSample(object):
    width = 900
    height = 700

    def __init__(self):
        super(UiSample, self).__init__()
        self.initUI()

    def initUI(self):
        self.mainWindow = QMainWindow()
        self.mainWindow.resize(self.width, self.height)
        self.mainWindow.setTabPosition(Qt.RightDockWidgetArea, QTabWidget.North)

        self.menuBar()
        self.treeViewWidget()
        self.statusBar()

        QMetaObject.connectSlotsByName(self.mainWindow)
        self.mainWindow.show()


        # hbox = QHBoxLayout(self)
        #
        # topleft = QFrame(self)
        # topleft.setFrameShape(QFrame.StyledPanel)
        # topleft.resize(200,300)
        # topleft.setStyleSheet("background-color: rgb(200, 255, 255)")
        #
        # layout = QVBoxLayout(topleft)
        # for _ in range(10):
        #     l = QLabel('test')
        #     layout.addWidget(l)
        #
        # layout.setAlignment(Qt.AlignTop)
        # topleft.setLayout(layout)
        #
        # topright = QFrame(self)
        # topright.setFrameShape(QFrame.StyledPanel)
        # topright.resize(500,200)
        #
        # splitter1 = QSplitter(Qt.Horizontal)
        # splitter1.addWidget(topleft)
        # splitter1.addWidget(topright)
        # hbox.addWidget(splitter1)
        #
        # self.setLayout(hbox)
        # self.setGeometry(300, 100, 700, 500)
        # # self.setWindowIcon(QIcon('sample.png'))
        # self.setWindowTitle('QSplitter')

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
        dockWidget = QDockWidget()
        dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
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
        dockWidget.setWidget(self.treeView)
        self.mainWindow.addDockWidget(Qt.LeftDockWidgetArea, dockWidget)

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

    def statusBar(self):
        self.statusbar = QStatusBar(self.mainWindow)
        self.mainWindow.setStatusBar(self.statusbar)