from setuptools import setup

setup(
    name='remote-watchman',    
    version='0.2',
    scripts=['HostMain.py','Constant.py','DHandler.py','HostConfig.py', 'HostSSH.py', 'MailConfiguration.py', 'Validations.py', 'Obj.py'],
    entry_points = {
    	"console_scripts": ['remote-watchman = HostMain:main']
    },
    install_requires=[
        'halo',
        'terminaltables'
    ],
)
