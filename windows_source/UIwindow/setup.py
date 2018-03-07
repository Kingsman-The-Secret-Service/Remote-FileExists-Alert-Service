from cx_Freeze import setup, Executable
import sys, os

productName = "ReLinAll"
# if 'bdist_msi' in sys.argv:
#     sys.argv += ['--initial-target-dir', 'C:\InstallDir\\' + productName]
#     sys.argv += ['--install-script', 'install.py']

build_exe_options = {"packages": ['time', 'sys', 'sqlite3', 'paramiko','terminaltables','smtplib','email.mime.text','email.mime.multipart','multiprocessing','_cffi_backend','logging.config'], "includes":["idna.idnadata"], "excludes": ["tkinter"]}

exe = Executable(
      script="AppUI.py",
      base="Win32GUI",
      targetName="ReLinAll.exe"
     )
setup(
      name="ReLinAll.exe",
      version="1.0",
      author="ravi",
      options={"build_exe": build_exe_options},
      description="Copyright 2018",
      executables=[exe])
      # scripts=[
      #          'install.py'
      #          ]
      # ) 