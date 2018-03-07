from Server import *
from PyQt5.QtGui import *
from Summary import *

class SSHApp(summary, server):
    def __init__(self):
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon(QPixmap('sample.png')))
        app.setStyle('Fusion')
        super(SSHApp,self).__init__()
        sys.exit(app.exec_())

if __name__ == '__main__':
    SSHApp()