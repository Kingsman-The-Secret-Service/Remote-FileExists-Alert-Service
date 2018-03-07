# from halo import Halo
import base64
import logging
import logging.config

class HostConstant:
    # haloSpinner = None
    def __init__(self):
        self.initLog()

    # def initSpinner(self):
    #     if self.haloSpinner is None:
    #         self.haloSpinner = Halo(text='Please wait', spinner='dots1')
    #         #https://github.com/sindresorhus/cli-spinners/blob/dac4fc6571059bb9e9bc204711e9dfe8f72e5c6f/spinners.json
    #     return self.haloSpinner

    def initLog(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler('relinall.log')
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def logComment(self, comments):
        self.logger.info(comments)

    # def startProgress(self):
    #     self.initSpinner().start()

    # def stopProgress(self):
    #     self.initSpinner().stop()

    def encryptpwd(self, pwd):
        return base64.b64encode(pwd.encode()).decode('utf-8')

    def decryptpwd(self, pwd):
        return base64.b64decode(pwd.encode()).decode('utf-8')

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
    iswatch = 'is_watching'
    conn_status = 'conn_status'

    mTName = 'mail_config'
    sTName = 'smtp_config'
    smtp = 'smtp'
    smtp_port = 'smtp_port'
    receiver = 'receiver'
    sub = 'subject'

    ENTER_OPTION = 'Enter the option: '