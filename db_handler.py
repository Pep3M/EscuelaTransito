from sqlite3 import connect

# CONSTANTES
DB_NAME = 'db.sqlite3'
T_ALUMNOS = 't_alumnos'
T_HORARIOS = 't_horarios'

# T_ALUMNOS
FULL_NAME = 'full_name'
TELEFONO = 'telefono'
DATOS = 'datos'


def conexion(func):
    def wrapper(*args, **kwargs):
        db = connect('db.sqlite3')
        func(db=db)
        db.commit()
        db.close()
    return wrapper


@conexion
def create_tables(db):
    
    # TABLA ALUMNOS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s VARCHAR(15),
        %s VARCHAR(150))
    ''' % (T_ALUMNOS, FULL_NAME, TELEFONO, DATOS)
    db.cursor().execute(sql)


create_tables()