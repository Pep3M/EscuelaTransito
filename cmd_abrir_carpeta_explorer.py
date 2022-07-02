import os

def url_windows(url_Python):
    return str(url_Python).replace('/','\\')

def abrirCarpeta(ruta):
    #print(url_windows(ruta))
    os.system('start %windir%\explorer.exe "{}"'.format(url_windows(ruta)))