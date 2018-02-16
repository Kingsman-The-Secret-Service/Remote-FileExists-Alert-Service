from cx_Freeze import setup, Executable
import sys, os

productName = "ReLinAll"
# if 'bdist_msi' in sys.argv:
#     sys.argv += ['--initial-target-dir', 'C:\InstallDir\\' + productName]
#     sys.argv += ['--install-script', 'install.py']

build_exe_options = {"packages": ['time', 'sys', 'sqlite3', 'paramiko','halo','terminaltables','email.mime.text','email.mime.multipart','multiprocessing'], "excludes": ["tkinter"]}

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

      # pip install halo
      # pip install paramiko
      # pip install terminaltables