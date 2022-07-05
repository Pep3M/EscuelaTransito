from datetime import datetime
from os import mkdir, path
from db_constantes import DB_NAME

from db_handler import get_last_matricula_date



#Rutas
RUTA_ASSETS = 'assets'
RUTA_COPIA_SEG = path.join(RUTA_ASSETS,'secure_copies')



def copia_seguridad_diaria():
    
    if not path.exists(RUTA_COPIA_SEG):
        mkdir(RUTA_COPIA_SEG)

    #last_date_update = get_last_matricula_date()
    date_today = str(datetime.now().date())

    #if last_date_update:
    ruta_copia_hoy = path.join(RUTA_COPIA_SEG, date_today)
    
    if not path.exists(ruta_copia_hoy):
        mkdir(ruta_copia_hoy)
        
    file_fuente = path.join(DB_NAME)
    file_destino = path.join(ruta_copia_hoy, 'db.sqlite3')
    
    with open(file_fuente,'rb') as file:
        data = file.read()
        with open(file_destino,'wb') as file_dest:
            
            file_dest.write(data)
                    
    