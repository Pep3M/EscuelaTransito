from os import path
from sqlite3 import connect
from db_constantes import *


# Decorador, para las conexiones a la DB
def conexion_db(func):
    def wrapper(*args, **kwargs):
        db = connect('db.sqlite3')
        f = func(db=db)
        db.commit()
        db.close()
        return f
    return wrapper


@conexion_db
def create_tables(db):
    
    # TABLA ALUMNOS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s VARCHAR(30),
        %s VARCHAR(30),
        %s VARCHAR(15),
        %s VARCHAR(150))
    ''' % (T_ALUMNOS, FULL_NAME, CI, MUNICIPIO, TELEFONO, DATOS)
    db.cursor().execute(sql)
    
    # TABLA CURSOS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s INTEGER,
        %s VARCHAR(100))
    ''' % (T_CURSOS, NOMBRE_CURSO, MATRICULA_INIT, DATOS)
    db.cursor().execute(sql)
    
    # TABLA HORARIOS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s VARCHAR(100))
    ''' % (T_HORARIOS, HORARIO, DATOS)
    db.cursor().execute(sql)
    
    # TABLA CATEGORIAS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s VARCHAR(5),
        %s VARCHAR(100))
    ''' % (T_CATEGORIA_LIC, NOMBRE_CAT, CODIGO_CAT, DATOS)
    db.cursor().execute(sql)
    
    # TABLA MUNICIPIOS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(30),
        %s VARCHAR(100))
    ''' % (T_MUNICIPIOS, MUNICIPIO, DATOS)
    db.cursor().execute(sql)

    # TABLA MATRICULAS
    sql = '''
    CREATE TABLE IF NOT EXISTS %s (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        %s VARCHAR(20),
        %s INTEGER UNIQUE,
        %s INTEGER,
        %s INTEGER,
        %s INTEGER,
        %s INTEGER,
        %s VARCHAR(200))
    ''' % (T_MATRICULAS, FECHA, MATRICULA, ID_CURSO, ID_ALUMNO, ID_CATEGORIA_LIC, ID_HORARIO, DATOS)
    db.cursor().execute(sql)

@conexion_db
def datos_iniciales(db):
    
    # llenando municipios
    municipios = [
        'Playa', 'Plaza de la Revolución', 'Centro Habana', 'La Habana Vieja', 'Regla', 'La Habana del Este', 'Guanabacoa', 'San Miguel del Padrón', 'Diez de Octubre', 'Cerro', 'Marianao', 'La Lisa','Boyeros', 'Arroyo Naranjo', 'Cotorro'
    ]
    for municipio in municipios:
        sql = '''
        INSERT OR IGNORE INTO %s (%s)
        VALUES (?)
        ''' % (T_MUNICIPIOS, MUNICIPIO)
        param = [municipio]
        db.cursor().execute(sql, param)
        
    # llenando categorias
    categorias = [
       ['A', 'Motocicletas', 'motocicletas y otros vehículos de motor similares'],
       ['A-1', 'Ciclomotor', 'los ciclomotores'],
       ['B', 'Automovil', 'vehículos de motor no comprendidos en la categoría “A”, con peso máximo autorizado inferior a 3500 kilogramos y con un número de asientos que, sin contar el del conductor, no exceda de ocho y a arrastrar un remolque ligero.'],
       ['C', 'Camion (mas de 7500Kg)', 'vehículos de motor dedicados al transporte de carga, con un peso máximo autorizado superior a 3500 kilogramos y a arrastrar un remolque ligero'],
       ['C-1', 'Camion (hasta 7500Kg)', 'los vehículos de motor dedicados al transporte de carga, con un peso máximo autorizado que exceda de 3500 kilogramos y hasta 7500 Kilogramos y arrastrar un remolque ligero.'],
       ['D', 'Omnibus (mas de 17 asientos)', 'vehículos de motor destinados al transporte de personas, con más de ocho asientos, sin contar el del conductor.'],
       ['D-1', 'Microbus (hasta 17 asientos)', 'los vehículos de motor destinados al transporte de personas, con más de ocho asientos y no exceda de dieciséis, sin contar el del conductor.'],
       ['E', 'Articulado', 'conjunto de vehículos cuyo vehículo de tracción esté comprendido en cualquiera de las categorías y subcategorías “B”, “C”, “C-1”, “D” y “D-1”, para los cuales está habilitado el conductor, pero que por su naturaleza no quede incluido en ninguna de ellas. Se incluyen, además, en esta categoría a los ómnibus articulados..'],
       ['F', 'Agroindustrial y de la construccion', 'vehículos agrícolas de motor, especializados de la construcción, industriales, de carga o descarga, o cualesquiera otros que reuniendo los requisitos exigidos para circular por las vías, no clasifican en ninguna de las anteriores categorías de licencia de conducción.'],
       ['FE', 'Tractor con remolques', 'vehículos contenidos en el numeral anterior, cuando circulen con uno o más remolques'],
    ]
    for categoria in categorias:
        sql = '''
        INSERT OR IGNORE INTO %s (%s,%s,%s)
        VALUES (?,?,?)
        ''' % (T_CATEGORIA_LIC, CODIGO_CAT, NOMBRE_CAT, DATOS)
        param = [categoria[0], categoria[1], categoria[2]]
        db.cursor().execute(sql, param)

# datos iniciales cuando no existe la DB
if not path.exists(DB_NAME):
    create_tables()
    datos_iniciales()
    
    
# Consultas (SELECTS)

@conexion_db
def get_all_alumnos(db):
    cursor = db.cursor()
    sql = 'SELECT %s, %s, %s, %s, %s FROM %s' % (FULL_NAME, CI, MUNICIPIO, TELEFONO, DATOS, T_ALUMNOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    return elementos

@conexion_db
def get_municipios(db):
    cursor = db.cursor()
    sql = 'SELECT %s FROM %s;' % (MUNICIPIO, T_MUNICIPIOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    municipios = [elemento[0] for elemento in elementos]
    return municipios