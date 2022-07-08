from os import path
from sqlite3 import Connection, connect
from db_constantes import *
from datetime import datetime


# Decorador, para las conexiones a la DB
def conexion_db(func):

    def wrapper(*args, **kwargs):
        db = connect(DB_NAME)
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
        %s VARCHAR(15),
        %s VARCHAR(15),
        %s VARCHAR(100))
    ''' % (T_CURSOS, NOMBRE_CURSO, MATRICULA_INIT, YEAR, FECHA_INICIAL,
           FECHA_FINAL, DATOS)
    db.cursor().execute(sql)

    # TABLA HORARIOS
    sql = '''CREATE TABLE IF NOT EXISTS %s (
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
        {MATRICULA} INTEGER,
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
    {T_MATRICULAS}.{ID_CURSO},
    {T_MATRICULAS}.id
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
        'Playa', 'Plaza de la Revolución', 'Centro Habana', 'La Habana Vieja',
        'Regla', 'La Habana del Este', 'Guanabacoa', 'San Miguel del Padrón',
        'Diez de Octubre', 'Cerro', 'Marianao', 'La Lisa', 'Boyeros',
        'Arroyo Naranjo', 'Cotorro'
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
        [
            'A', 'Motocicletas',
            'motocicletas y otros vehículos de motor similares'
        ],
        ['A-1', 'Ciclomotor', 'los ciclomotores'],
        [
            'B', 'Automovil',
            'vehículos de motor no comprendidos en la categoría “A”, con peso máximo autorizado inferior a 3500 kilogramos y con un número de asientos que, sin contar el del conductor, no exceda de ocho y a arrastrar un remolque ligero.'
        ],
        [
            'C', 'Camion (mas de 7500Kg)',
            'vehículos de motor dedicados al transporte de carga, con un peso máximo autorizado superior a 3500 kilogramos y a arrastrar un remolque ligero'
        ],
        [
            'C-1', 'Camion (hasta 7500Kg)',
            'los vehículos de motor dedicados al transporte de carga, con un peso máximo autorizado que exceda de 3500 kilogramos y hasta 7500 Kilogramos y arrastrar un remolque ligero.'
        ],
        [
            'D', 'Omnibus (mas de 17 asientos)',
            'vehículos de motor destinados al transporte de personas, con más de ocho asientos, sin contar el del conductor.'
        ],
        [
            'D-1', 'Microbus (hasta 17 asientos)',
            'los vehículos de motor destinados al transporte de personas, con más de ocho asientos y no exceda de dieciséis, sin contar el del conductor.'
        ],
        [
            'E', 'Articulado',
            'conjunto de vehículos cuyo vehículo de tracción esté comprendido en cualquiera de las categorías y subcategorías “B”, “C”, “C-1”, “D” y “D-1”, para los cuales está habilitado el conductor, pero que por su naturaleza no quede incluido en ninguna de ellas. Se incluyen, además, en esta categoría a los ómnibus articulados..'
        ],
        [
            'F', 'Agroindustrial y de la construccion',
            'vehículos agrícolas de motor, especializados de la construcción, industriales, de carga o descarga, o cualesquiera otros que reuniendo los requisitos exigidos para circular por las vías, no clasifican en ninguna de las anteriores categorías de licencia de conducción.'
        ],
        [
            'FE', 'Tractor con remolques',
            'vehículos contenidos en el numeral anterior, cuando circulen con uno o más remolques'
        ],
    ]
    for categoria in categorias:
        sql = '''
        INSERT OR IGNORE INTO %s (%s,%s,%s)
        VALUES (?,?,?)
        ''' % (T_CATEGORIA_LIC, CODIGO_CAT, NOMBRE_CAT, DATOS)
        param = [categoria[0], categoria[1], categoria[2]]
        db.cursor().execute(sql, param)

    # primer curso
    sql = '''
    INSERT OR IGNORE INTO %s (%s,%s,%s,%s,%s,%s)
    VALUES (?,?,?,?,?,?)
    ''' % (T_CURSOS, NOMBRE_CURSO, MATRICULA_INIT, YEAR, FECHA_INICIAL,
           FECHA_FINAL,MODELO_INIT)
    param = ['10', 615, 2022, '08/07/2022', '20/07/2022',26]
    db.cursor().execute(sql, param)

    # horario inicial
    horarios = [
        ['9:00 AM - 11:00 AM', 'Horario de la mañana'],
        ['2:00 PM - 4:00 PM', 'WhatsApp'],
        ['5:00 PM - 7:00 PM', 'Horario de la tarde'],
    ]
    for horario in horarios:
        sql = '''
        INSERT OR IGNORE INTO %s (%s,%s)
        VALUES (?,?)
        ''' % (T_HORARIOS, HORARIO, DATOS)
        param = [horario[0], horario[1]]
        db.cursor().execute(sql, param)


@conexion_db
def add_column_model_num_to_cursos(db:Connection):
    """
    Creamos este metodo provicional para crear el campo y valor inicial para que los modelos queden enumerados correctamente

    Args:
        db (Connection): Recibe db y metodos como decorador
    """
    c = db.cursor()

    sql = f'''
    ALTER TABLE {T_CURSOS} ADD COLUMN [{MODELO_INIT}] [INTEGER]
    '''
    sql2 = f'''
    UPDATE {T_CURSOS} SET {MODELO_INIT}=?;
    '''
    parm = [26]
    
    try:
        c.execute(sql)
        db.commit()
        c.execute(sql2, parm)
    except:
        pass
    
add_column_model_num_to_cursos()

@conexion_db
def agregar_fecha_al_horario(db: Connection):
    sql = f'''ALTER TABLE {T_CURSOS} 
    ADD COLUMN [{FECHA_INICIAL}] [VARCHAR(15)];'''
    sql2 = f'''ALTER TABLE {T_CURSOS} 
    ADD COLUMN [{FECHA_FINAL}] [VARCHAR(15)];'''

    cursor = db.cursor()
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
    except:
        print(
            'Ya la tabla horario tiene la fecha de inicio y final como campos')


# datos iniciales cuando no existe la DB
if not path.exists(DB_NAME):
    create_tables()
    datos_iniciales()
#create_tables()
#agregar_fecha_al_horario()




# Consultas (SELECTS)

def get_modelo_init_by_idcurso(id_curso):
    db = connect(DB_NAME)
    cursor = db.cursor()
    sql = 'SELECT %s FROM %s WHERE id=?' % (MODELO_INIT, T_CURSOS)
    parm = [id_curso]
    cursor.execute(sql, parm)
    elementos = cursor.fetchone()
    db.close()
    return elementos[0]


@conexion_db
def get_all_alumnos(db: Connection):
    cursor = db.cursor()
    sql = 'SELECT %s, %s, %s, %s, %s FROM %s' % (FULL_NAME, CI, MUNICIPIO,
                                                 TELEFONO, DATOS, T_ALUMNOS)
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


def get_alumnos_for_excel(id_curso, horario):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql2 = f'''
    SELECT {FULL_NAME},{CI},{TELEFONO},{MUNICIPIO} FROM {V_MATRICULAS} WHERE {HORARIO}=? AND {ID_CURSO}=?
    '''
    param2 = [horario, id_curso]

    cursor.execute(sql2, param2)
    alumnos = cursor.fetchall()

    db.close()
    return alumnos


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
    horarios = [elemento[0] for elemento in elementos]
    return horarios


@conexion_db
def get_id_horarios(db: Connection):
    cursor = db.cursor()
    sql = 'SELECT id FROM %s;' % (T_HORARIOS)
    cursor.execute(sql)
    elementos = cursor.fetchall()
    id_horarios = [elemento[0] for elemento in elementos]
    return id_horarios


def get_matr_init_by_id(id_curso) -> int:
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {MATRICULA_INIT} FROM {T_CURSOS} WHERE id=?;
    '''
    parm = [id_curso]

    cursor.execute(sql, parm)
    matr_ini = cursor.fetchone()[0]
    db.close()
    return int(matr_ini)


@conexion_db
def get_last_curso_id(db: Connection):
    cursor = db.cursor()
    sql = '''
    SELECT %s FROM %s ORDER BY %s DESC,%s DESC LIMIT 1;
    ''' % ('id', T_CURSOS, YEAR, NOMBRE_CURSO)

    cursor.execute(sql)

    return cursor.fetchone()[0]


def get_idcurso_by_curso_year(curso, year):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = '''
    SELECT id FROM %s WHERE %s=? AND %s=?
    ''' % (T_CURSOS, NOMBRE_CURSO, YEAR)
    param = [str(curso), int(year)]

    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()

    if fetch:
        id = fetch[0]
    else:
        id = 0

    return id


@conexion_db
def get_cursos(db: Connection):
    cursor = db.cursor()

    sql = f'''
    SELECT {NOMBRE_CURSO},{YEAR} FROM {T_CURSOS}
    ORDER BY {YEAR} DESC,{NOMBRE_CURSO} DESC
    '''
    cursor.execute(sql)
    fetch = cursor.fetchall()
    if fetch: return fetch
    else: return False


def get_campo_datos_idcursos(idcurso):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {DATOS} FROM {T_CURSOS}
    WHERE id=?;
    '''
    param = [idcurso]
    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    if fetch and not fetch[0] == None: return fetch[0]
    else: return False
    db.close()


def actualizar_curso(id_curso, nombre, year, f_ini, f_fin, datos, matri_ini, model_ini):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    UPDATE {T_CURSOS} SET {NOMBRE_CURSO}=?, {YEAR}=?, {FECHA_INICIAL}=?, {FECHA_FINAL}=?, {DATOS}=?, {MATRICULA_INIT}=?, {MODELO_INIT}=? WHERE id=?
    '''
    param = [nombre, year, f_ini, f_fin, datos, matri_ini, model_ini, id_curso]
    cursor.execute(sql, param)

    db.commit()
    db.close()


def eliminar_curso(id_curso):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    DELETE FROM {T_MATRICULAS}
    WHERE {ID_CURSO}=?
    '''
    parm = [id_curso]

    cursor.execute(sql, parm)

    db.commit()

    sql = f'''
    DELETE FROM {T_CURSOS}
    WHERE id=?
    '''
    parm = [id_curso]

    cursor.execute(sql, parm)

    db.commit()

    db.close()


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


def get_curso_by_id(id, curso_formateado=False):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = '''
    SELECT %s,%s FROM %s WHERE id=?
    ''' % (NOMBRE_CURSO, YEAR, T_CURSOS)
    param = [id]

    cursor.execute(sql, param)
    fetch = cursor.fetchone()
    db.close()

    if fetch:
        nombre = fetch[0]
        year = fetch[1]
    else:
        nombre = ''

    if curso_formateado:
        return f'{nombre}-{year}'

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


def get_matricula_by_ci_curso(ci, id_curso):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {FULL_NAME},{HORARIO} FROM {V_MATRICULAS}
    WHERE {CI}=? AND {ID_CURSO}=?
    '''
    parm = [ci, id_curso]
    cursor.execute(sql, parm)

    fetch = cursor.fetchone()
    db.close()
    return fetch



def get_view_matriculas_by_idcurso(id_curso, horario=None):

    db = connect(DB_NAME)
    cursor = db.cursor()

    if not horario:
        sql = f'''
        SELECT {FULL_NAME},{CI},{MUNICIPIO},{TELEFONO},{HORARIO},{CODIGO_CAT},{DATOS} 
        FROM {V_MATRICULAS} WHERE {ID_CURSO}=?;
        '''
        param = [id_curso]
    else:
        sql = f'''
        SELECT {FULL_NAME},{CI},{MUNICIPIO},{TELEFONO},{HORARIO},{CODIGO_CAT},{DATOS} 
        FROM {V_MATRICULAS} WHERE {ID_CURSO}=? AND {HORARIO}=?;
        '''
        param = [id_curso, horario]
        
    cursor.execute(sql, param)
    fetch = cursor.fetchall()
    db.close()

    if fetch:
        return fetch
    else:
        return False



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


def actualizar_alumno(datos_alumno: list, old_ci):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    UPDATE {T_ALUMNOS} SET {FULL_NAME}=?, {CI}=?, {MUNICIPIO}=?, {TELEFONO}=?, {DATOS}=?
    WHERE {CI}=?
    '''
    parm = datos_alumno
    parm.append(old_ci)
    cursor.execute(sql, datos_alumno)

    db.commit()
    db.close()

    id_alumno = get_id_alumno_by_ci(datos_alumno[1])
    return id_alumno


def agregar_matricula(datos_matricula: list, curso, year):

    nombre = datos_matricula[0]
    ci = datos_matricula[1]
    municipio = datos_matricula[2]
    telefono = datos_matricula[3]
    horario = datos_matricula[4]
    datos = datos_matricula[5]
    categoria = datos_matricula[6]
    id_curso = get_idcurso_by_curso_year(curso, year)

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
    ''' % (T_MATRICULAS, FECHA, ID_CURSO, ID_ALUMNO, ID_CATEGORIA_LIC,
           ID_HORARIO, DATOS)

    param = [
        str(datetime.now())[0:10], id_curso, id_alumno,
        get_id_cat(categoria),
        get_id_horario(horario), datos
    ]

    cursor.execute(sql, param)
    db.commit()
    db.close()


def actualizar_matricula(datos_matricula: list, old_ci, id_curso):

    nombre = datos_matricula[0]
    ci = datos_matricula[1]
    municipio = datos_matricula[2]
    telefono = datos_matricula[3]
    horario = datos_matricula[4]
    datos = datos_matricula[5]
    categoria = datos_matricula[6]

    # actualizar datos de alumnos, sin el horario
    datos_alumnos = [nombre, ci, municipio, telefono, datos]
    id_alumno = actualizar_alumno(datos_alumnos, old_ci)

    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    UPDATE {T_MATRICULAS} SET {ID_CATEGORIA_LIC}=?, {ID_HORARIO}=?, {DATOS}=?
    WHERE {ID_ALUMNO}=? AND {ID_CURSO}=?;
    '''

    param = [
        get_id_cat(categoria),
        get_id_horario(horario), datos, id_alumno, id_curso
    ]

    cursor.execute(sql, param)
    db.commit()
    db.close()


def eliminar_matr_by_ci_and_curso(ci, curso, year):

    id_curso = get_idcurso_by_curso_year(curso, year)

    id_alumno = get_id_alumno_by_ci(ci)

    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    DELETE FROM {T_MATRICULAS}
    WHERE {ID_ALUMNO}=? AND {ID_CURSO}=?
    '''
    param = [id_alumno, id_curso]

    cursor.execute(sql, param)

    db.commit()
    db.close()


def get_idalumnos_by_idhorario_idcurso(id_horario, id_curso):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {ID_ALUMNO} FROM {T_MATRICULAS}
    WHERE {ID_HORARIO}=? AND {ID_CURSO}=?;
    '''
    parm = [id_horario, id_curso]

    cursor.execute(sql, parm)
    fetch = cursor.fetchall()
    if fetch:
        ids = [item[0] for item in fetch]
        return ids


#print(get_idalumnos_by_idhorario_idcurso(1,1))


def set_matriculas_by_id_horario_idcurso(id_horario, id_curso,
                                         matricula_inicial: int):
    db = connect(DB_NAME)
    cursor = db.cursor()

    ids_alumnos = get_idalumnos_by_idhorario_idcurso(id_horario, id_curso)

    sql = f'''
    UPDATE {T_MATRICULAS} SET {MATRICULA}=?
    WHERE {ID_HORARIO}=? AND {ID_ALUMNO}=?;
    '''

    matricula = matricula_inicial
    if ids_alumnos:
        for id_alum in ids_alumnos:

            parm = [matricula, id_horario, id_alum]

            cursor.execute(sql, parm)
            db.commit()

            matricula += 1

    db.close()
    return matricula


def get_fecha_inicio_fin_by_idcurso(id_curso):
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {FECHA_INICIAL},{FECHA_FINAL} FROM {T_CURSOS}
    WHERE id=?
    '''
    parm = [id_curso]
    cursor.execute(sql, parm)

    fetch = cursor.fetchone()
    if fetch:
        return fetch
    return False


def agregar_curso(name_curso, year, f_ini, f_fin, datos, matri_ini, model_ini) -> int | bool:
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    INSERT OR IGNORE INTO {T_CURSOS}({NOMBRE_CURSO},{YEAR},{FECHA_INICIAL},{FECHA_FINAL},{DATOS},{MATRICULA_INIT},{MODELO_INIT})
    VALUES (?,?,?,?,?,?,?)
    '''
    param = [str(name_curso), int(year), f_ini, f_fin, datos, matri_ini, model_ini]
    cursor.execute(sql, param)
    db.commit()
    db.close()
    id_curso = get_idcurso_by_curso_year(name_curso, year)

    return id_curso

@conexion_db
def get_last_matricula_date(db:Connection):
    
    cursor = db.cursor()

    sql = f'''
    SELECT {FECHA} FROM {T_MATRICULAS} 
    ORDER BY {FECHA} DESC LIMIT 1
    '''
    cursor.execute(sql)

    fetch = cursor.fetchone()
    
    if fetch:
        return fetch[0]
    
    
def get_matric_model_init_by_idcurso(idcurso) -> list:
    
    db = connect(DB_NAME)
    cursor = db.cursor()

    sql = f'''
    SELECT {MATRICULA_INIT},{MODELO_INIT} FROM {T_CURSOS} 
    WHERE id=?
    '''
    par= [idcurso]
    
    cursor.execute(sql,par)

    fetch = cursor.fetchone()
    
    if fetch:
        return fetch
    
@conexion_db
def get_new_matric_model_init(db:Connection) -> list:

    idcurso = get_last_curso_id()
    
    cursor = db.cursor()

    sql = f'''
    SELECT {MATRICULA_INIT},{MODELO_INIT} FROM {T_CURSOS} 
    WHERE id=?
    '''
    par= [idcurso]
    
    cursor.execute(sql,par)

    fetch = cursor.fetchone()
    
    if fetch:
        matr_ini = fetch[0]
        model_ini = fetch[1]
        
        matriculas = get_view_matriculas_by_idcurso(idcurso)
        cant_matr = len(matriculas) if matriculas else 0
        cant_hor = 0

        if matriculas:
            horarios = get_horarios()
            
            for horario in horarios:
                for matricula in matriculas:
                    if horario in matricula[4]:
                        cant_hor += 1
                        break
        
        
        # matricula inicial mas la cantidad de matriculas hechas ese curso
        # numero en los modelos, mas la cantidad de horarios q hay, lo que da los numeros nuevos
        return [matr_ini+cant_matr, model_ini+cant_hor]
    
