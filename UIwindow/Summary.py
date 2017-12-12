from WindowUI import *

class summary(UiSample):
    summaryData = {}

    def __init__(self):
        super(summary, self).__init__()

    def summary(self):
        self.docker('summary')
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()

        hbox = QHBoxLayout(self.mainWindow)
        self.textbox = QLabel(self.mainWindow)
        self.textbox.setText('Hello')
        hbox.addWidget(self.treeView)
        self.mainWindow.setLayout(hbox)

        # index = self.treeView.selectedIndexes()[0]
        # hostname = self.treeView.model().itemFromIndex(index).text()
        #
        # summaryTab = Helper.getData(self.widgetData[self.currentData()['hostname']], 'summary')
        # ssh = Helper.getData(self.widgetData[self.currentData()['hostname']], 'ssh')
        # summaryTab.setLayout(QVBoxLayout())
        #
        # self.ip()
        # self.hostname(ssh)
        #
        # html = self.render('summary.html', self.summaryData)
        # view = QWebEngineView()
        # view.setHtml(html, QUrl("file://"))
        # summaryTab.layout().addWidget(view)

    def ip(self):
        self.summaryData['ip'] = self.dataHost['hostname']

    def hostname(self, ssh):
        output = SSHClient.execute(ssh, 'hostname')
        self.summaryData['hostname'] = output.decode('utf-8')
