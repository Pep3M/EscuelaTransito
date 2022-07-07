# CONSTANTES
DB_NAME = 'assets/db.sqlite3'

T_ALUMNOS = 't_alumnos'
T_CURSOS = 't_cursos'
T_HORARIOS = 't_horarios'
T_CATEGORIA_LIC = 't_categoria_lic'
T_MUNICIPIOS = 't_municipios'
T_MATRICULAS = 't_matriculas'

# T_ALUMNOS
FULL_NAME = 'full_name'
CI = 'ci'
MUNICIPIO = 'MUNICIPIO'
TELEFONO = 'telefono'
DATOS = 'datos'

# T_HORARIOS
HORARIO = 'horario'

# T_CURSOS
NOMBRE_CURSO = 'nombre_curso'
MATRICULA_INIT = 'matricula_init'
YEAR = 'year'
FECHA_INICIAL = 'fecha_inicial'
FECHA_FINAL = 'fecha_final'
MODELO_INIT = 'modelo_init'

# T_HORARIOS
HORARIO = 'horario'

# T_CATEGORIA_LIC
NOMBRE_CAT = 'nombre_cat'
CODIGO_CAT = 'codigo_cat'

# T_MATRICULAS
FECHA = 'fecha'
MATRICULA = 'matricula'
ID_CURSO = 'id_curso'
ID_ALUMNO = 'id_alumno'
ID_CATEGORIA_LIC = 'id_categoria_lic'
ID_HORARIO = 'id_horario'

KEY_MATRICULAS = [
    'id',
    FECHA,
    MATRICULA,
    ID_CURSO,
    ID_ALUMNO,
    ID_CATEGORIA_LIC,
    ID_HORARIO,
    DATOS
]


# ---- VIEWS -------

# V_MATRICULAS
V_MATRICULAS = 'v_matriculas'
KEYS_V_MATRICULAS = [
    FULL_NAME,
    CI,
    MUNICIPIO,
    TELEFONO,
    HORARIO,
    CODIGO_CAT,
    DATOS
]