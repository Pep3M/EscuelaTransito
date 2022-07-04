import os


instr = 'pyinstaller.exe --windowed --onefile --icon=assets/imgs/logo.ico --name=Matriculas --hidden-import babel.numbers main.py'

#os.system(instr)
os.popen(instr)