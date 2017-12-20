from WindowUI import *

class summary(UiSample):

    def __init__(self):
        super(summary, self).__init__()

    def summary(self, ):
        index = self.treeView.selectedIndexes()[0]
        hostname = self.treeView.model().itemFromIndex(index).text()
        self.doubleClicked(hostname)

        # data = self.dbHandler.getServerGrouped()
        # print str(data)
        #
        # for d in data:
        #     if d == hostname:
        #         self.treeView.model().itemFromIndex(index).setBackground(QColor("white"))
        #         self.treeView.clearSelection()
        #         b = QBrush(Qt.yellow)
        #         self.treeView.model().itemFromIndex(index).setBackground(b)

    def hostname(self, ssh):
        output = self.ssh.execute(ssh, 'hostname')
        self.detail['hostname'] = output.decode('utf-8')

    def uptime(self, ssh):
        output = self.ssh.execute(ssh, 'uptime -p')
        self.detail['uptime'] = output.decode('utf-8')

    def kernelname(self, ssh):
        output = self.ssh.execute(ssh, 'uname -s')
        self.detail['kernelname'] = output.decode('utf-8')

    def kernelrelease(self, ssh):
        output = self.ssh.execute(ssh, 'uname -r')
        self.detail['kernelrelease'] = output.decode('utf-8')

    def osname(self, ssh):
        output = self.ssh.execute(ssh, 'uname -o')
        self.detail['osname'] = output.decode('utf-8')

    def processor(self, ssh):
        output = self.ssh.execute(ssh, 'uname -p')
        self.detail['processor'] = output.decode('utf-8')
