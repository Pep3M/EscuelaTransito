from os import path
from sqlite3 import Connection, connect
from db_constantes import *
from datetime import datetime


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
        %s INTEGER,
        %s VARCHAR(100))
    ''' % (T_CURSOS, NOMBRE_CURSO, MATRICULA_INIT, YEAR, DATOS)
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
    sql = f'''
    CREATE TABLE IF NOT EXISTS {T_MATRICULAS} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        {FECHA} VARCHAR(20),
        {MATRICULA} INTEGER UNIQUE,
        {ID_CURSO} INTEGER,
        {ID_ALUMNO} INTEGER,
        {ID_CATEGORIA_LIC} INTEGER,
        {ID_HORARIO} INTEGER,
        {DATOS} VARCHAR(200),
        FOREIGN KEY ({ID_CURSO}) REFERENCES {T_CURSOS}('id'),
        FOREIGN KEY ({ID_ALUMNO}) REFERENCES {T_ALUMNOS}('id'),
        FOREIGN KEY ({ID_CATEGORIA_LIC}) REFERENCES {T_CATEGORIA_LIC}('id'), 
        FOREIGN KEY ({ID_HORARIO}) REFERENCES {T_HORARIOS}('id'))
    '''
    db.cursor().execute(sql)
    
    # VIEW MATRICULAS
    sql = f'''
    CREATE VIEW IF NOT EXISTS {V_MATRICULAS}
    AS SELECT 
    {T_ALUMNOS}.{FULL_NAME},
    {T_ALUMNOS}.{CI},
    {T_ALUMNOS}.{MUNICIPIO},
    {T_ALUMNOS}.{TELEFONO},
    {T_HORARIOS}.{HORARIO},
    {T_CATEGORIA_LIC}.{CODIGO_CAT},
    {T_MATRICULAS}.{DATOS},
    {T_MATRICULAS}.{ID_CURSO}
    FROM {T_MATRICULAS}
    INNER JOIN {T_ALUMNOS} on {ID_ALUMNO}={T_ALUMNOS}.id
    INNER JOIN {T_HORARIOS} on {ID_HORARIO}={T_HORARIOS}.id
    INNER JOIN {T_CATEGORIA_LIC} on {ID_CATEGORIA_LIC}={T_CATEGORIA_LIC}.id;
    '''
    db.cursor().execute(sql)


@conexion_db
def datos_iniciales(db):

    # llenando municipios
    municipios = [
        'Playa', 'Plaza de la Revolución', 'Centro Habana', 'La Habana Vieja', 'Regla', 'La Habana del Este', 'Guanabacoa', 'San Miguel del Padrón', 'Diez de Octubre', 'Cerro', 'Marianao', 'La Lisa', 'Boyeros', 'Arroyo Naranjo', 'Cotorro'
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
        ['D', 'Omnibus (mas de 17 asientos)',
         'vehículos de motor destinados al transporte de personas, con más de ocho asientos, sin contar el del conductor.'],
        ['D-1', 'Microbus (hasta 17 asientos)',
         'los vehículos de motor destinados al transporte de personas, con más de ocho asientos y no exceda de dieciséis, sin contar el del conductor.'],
        ['E', 'Articulado', 'conjunto de vehículos cuyo vehículo de tracción esté comprendido en cualquiera de las categorías y subcategorías “B”, “C”, “C-1”, “D” y “D-1”, para los cuales está habilitado el conductor, pero que por su naturaleza no quede incluido en ninguna de ellas. Se incluyen, además, en esta categoría a los ómnibus articulados..'],
        ['F', 'Agroindustrial y de la construccion', 'vehículos agrícolas de motor, especializados de la construcción, industriales, de carga o descarga, o cualesquiera otros que reuniendo los requisitos exigidos para circular por las vías, no clasifican en ninguna de las anteriores categorías de licencia de conducción.'],
        ['FE', 'Tractor con remolques',
         'vehículos contenidos en el numeral anterior, cuando circulen con uno o más remolques'],
    ]
    for categoria in categorias:
        sql = '''
        INSERT OR IGNORE INTO %s (%s,%s,%s)
        VALUES (?,?,?)
        ''' % (T_CATEGORIA_LIC, CODIGO_CAT, NOMBRE_CAT, DATOS)
        param = [categoria[0], categoria[1], categoria[2]]
        db.cursor().execute(sql, param)

    sql = '''
    INSERT OR IGNORE INTO %s (%s,%s,%s)
    VALUES (?,?,?)
    ''' % (T_CURSOS, NOMBRE_CURSO, MATRICULA_INIT, YEAR)
    param = ['10', 615, 2022]
    db.cursor().execute(sql, param)


# datos iniciales cuando no existe la DB
if not path.exists(DB_NAME):
    create_tables()
    datos_iniciales()
#create_tables()

# Consultas (SELECTS)

@conexion_db
def get_all_alumnos(db: Connection):
    cursor = db.cursor()
    sql = 'SELECT %s, %s, %s, %s, %s FROM %s' % (
        FULL_NAME, CI, MUNICIPIO, TELEFONO, DATOS, T_ALUMNOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    return elementos


def select_alumno_by_ci(ci):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = 'SELECT %s, %s, %s, %s, %s FROM %s WHERE %s=?' % (
        FULL_NAME, CI, MUNICIPIO, TELEFONO, DATOS, T_ALUMNOS, CI)
    param = [ci]

    cursor.execute(sql, param)
    elementos = cursor.fetchall()

    db.close()
    return elementos


def get_id_alumno_by_ci(ci):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql2 = '''
    SELECT id FROM %s WHERE %s=? LIMIT 1
    ''' % (T_ALUMNOS, CI)
    param2 = [ci]

    cursor.execute(sql2, param2)
    id_alumno = int(cursor.fetchone()[0])

    db.close()
    return id_alumno


@conexion_db
def get_municipios(db):
    cursor = db.cursor()
    sql = 'SELECT %s FROM %s;' % (MUNICIPIO, T_MUNICIPIOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    municipios = [elemento[0] for elemento in elementos]
    return municipios


@conexion_db
def get_horarios(db: Connection):
    cursor = db.cursor()
    sql = 'SELECT %s FROM %s;' % (HORARIO, T_HORARIOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    municipios = [elemento[0] for elemento in elementos]
    return municipios


@conexion_db
def get_last_curso_id(db: Connection):
    cursor = db.cursor()
    sql = '''
    SELECT %s FROM %s ORDER BY %s,%s DESC LIMIT 1;
    ''' % ('id', T_CURSOS, NOMBRE_CURSO, YEAR)

    cursor.execute(sql)

    return cursor.fetchone()[0]



def get_idcurso_by_curso_year(curso, year):
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = '''
    SELECT id FROM %s WHERE %s=? AND %s=?
    ''' % (T_CURSOS, NOMBRE_CURSO, YEAR)
    param = [curso,year]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()
    
    if fetch: id = fetch[0]
    else: id = 0
    
    return id



@conexion_db
def get_all_cat_code(db: Connection):
    cursor = db.cursor()
    sql = '''
    SELECT %s FROM %s
    ''' % (CODIGO_CAT, T_CATEGORIA_LIC)
    cursor.execute(sql)

    return [categoria[0] for categoria in cursor.fetchall()]


def get_id_cat(categoria_code):
    db = connect(DB_NAME)
    cursor = db.cursor()
    sql = '''
    SELECT id FROM %s WHERE %s=?
    ''' % (T_CATEGORIA_LIC, CODIGO_CAT)
    param = [categoria_code]
    cursor.execute(sql, param)
    id = cursor.fetchone()[0]
    db.close()
    return id

def get_id_horario(horario):
    db = connect(DB_NAME)
    cursor = db.cursor()
    sql = '''
    SELECT id FROM %s WHERE %s=?
    ''' % (T_HORARIOS, HORARIO)
    param = [horario]
    cursor.execute(sql, param)
    id = cursor.fetchone()[0]
    db.close()
    return id


def get_curso_by_id(id):
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = '''
    SELECT %s FROM %s WHERE id=?
    ''' % (NOMBRE_CURSO, T_CURSOS)
    param = [id]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()
    
    if fetch: nombre = fetch[0]
    else: nombre = ''
    
    return nombre
    
def get_alumno_by_id(id):
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = '''
    SELECT %s,%s,%s FROM %s WHERE id=?
    ''' % (FULL_NAME, CI, TELEFONO, T_ALUMNOS)
    param = [id]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()
    
    return fetch

def get_categoria_by_id(id):
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = '''
    SELECT %s,%s FROM %s WHERE id=?
    ''' % (CODIGO_CAT, NOMBRE_CAT, T_CATEGORIA_LIC)
    param = [id]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()
    
    return fetch

def get_horario_by_id(id):
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = '''
    SELECT %s,%s FROM %s WHERE id=?
    ''' % (HORARIO, DATOS, T_HORARIOS)
    param = [id]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()
    
    return fetch


def get_view_matriculas_by_idcurso(id_curso):
        
    db = connect(DB_NAME)
    cursor = db.cursor()
    
    sql = f'''
    SELECT {FULL_NAME},{CI},{MUNICIPIO},{TELEFONO},{HORARIO},{CODIGO_CAT},{DATOS} 
    FROM {V_MATRICULAS} WHERE {ID_CURSO}=?;
    '''
    param = [id_curso]
    
    cursor.execute(sql, param)
    fetch = cursor.fetchall()
    db.close()
    
    if fetch: 
        return fetch
    else:
        return False




# INSERTS

def agregar_alumno(datos_alumno):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = '''
    INSERT OR IGNORE INTO %s (%s,%s,%s,%s,%s)
    VALUES (?,?,?,?,?)
    ''' % (T_ALUMNOS, FULL_NAME, CI, MUNICIPIO, TELEFONO, DATOS)

    cursor.execute(sql, datos_alumno)

    db.commit()
    db.close()

    id_alumno = get_id_alumno_by_ci(datos_alumno[1])
    return id_alumno


def agregar_matricula(datos_matricula: list):

    nombre = datos_matricula[0]
    ci = datos_matricula[1]
    municipio = datos_matricula[2]
    telefono = datos_matricula[3]
    horario = datos_matricula[4]
    datos = datos_matricula[5]
    categoria = datos_matricula[6]

    if not len(select_alumno_by_ci(ci)) > 0:
        # agregar datos, sin el horario
        datos_alumnos = [nombre, ci, municipio, telefono, datos]
        agregar_alumno(datos_alumnos)

    id_alumno = get_id_alumno_by_ci(ci)

    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = '''
    INSERT OR IGNORE INTO %s (%s,%s,%s,%s,%s,%s)
    VALUES (?,?,?,?,?,?)
    ''' % (T_MATRICULAS, FECHA, ID_CURSO, ID_ALUMNO, ID_CATEGORIA_LIC, ID_HORARIO, DATOS)
    
    param = [str(datetime.now())[0:10], get_last_curso_id(), id_alumno, get_id_cat(
        categoria), get_id_horario(horario), datos]
    
    cursor.execute(sql, param)
    db.commit()
    db.close()


#print(agregar_alumno(['Juan Pedro', '811232145765', 'Cerro', '53423245', '']))
# print(select_alumno_by_ci(ci='811232145765'))
# print(get_horarios())
