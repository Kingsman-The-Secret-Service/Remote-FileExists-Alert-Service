from halo import Halo
import base64

class HostConstant:
    haloSpinner = None

    def initSpinner(self):
        if self.haloSpinner is None:
            self.haloSpinner = Halo(text='Please wait', spinner='dots1')
            #https://github.com/sindresorhus/cli-spinners/blob/dac4fc6571059bb9e9bc204711e9dfe8f72e5c6f/spinners.json
        return self.haloSpinner

    def startProgress(self):
        self.initSpinner().start()

    def stopProgress(self):
        self.initSpinner().stop()

    def encryptpwd(self, pwd):
        return base64.b64encode(pwd)

    def decryptpwd(self, pwd):
        return base64.b64decode(pwd)

    ADD = '(1) Add Host'
    REMOVE = '(2) Remove Host'
    RUN = '(3) Run'
    EDIT = '(4) Edit Host Conf.'
    VIEW = '(5) View Hosts'
    MAIL = '(6) Mail Configuration'
    EXIT = '(7) Exit'

    dbName = 'host.db'
    did = 'id'
    tName = 'hostserver'
    host = 'host'
    uname = 'username'
    pwd = 'password'
    port = 'port'
    dirpath = 'dir_path'
    fname ='file_name'
    email ='email'
    fwatch = 'f_watcher'

    mTName = 'config'
    smtp = 'smtp'
    smtp_port = 'smtp_port'
    receiver = 'receiver'
    sub = 'subject'

    ENTER_OPTION = 'Enter the option: '