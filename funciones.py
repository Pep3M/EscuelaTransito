from os import mkdir, path
from tkinter import filedialog
from tkinter.ttk import Combobox
from MultiListBox_class import MultiColumnListbox
from curso_modelo import AulaModelo, CursoModelo
from db_handler import get_all_alumnos, get_alumnos_for_excel, get_curso_by_id, get_cursos, get_fecha_inicio_fin_by_idcurso, get_horario_by_id, get_horarios, get_id_horarios, get_idcurso_by_curso_year, get_last_curso_id, get_matr_init_by_id, get_modelo_init_by_idcurso, get_unidad_my_municipio, get_view_matriculas_by_idcurso, set_matriculas_by_id_horario_idcurso
from cmd_abrir_carpeta_explorer import abrirCarpeta
from db_constantes import *

MESES = [
    'meses',
    'enero',
    'febrero',
    'marzo',
    'abril',
    'mayo',
    'junio',
    'julio',
    'agosto',
    'septiembre',
    'octubre',
    'noviembre',
    'diciembre'
]

def init_multilist_alumnos(frame_container):
    header_alumnos = [
        'Nombre completo',
        'Carnet Identidad',
        'Municipio',
        'Telefono',
        'Horario',
        'Categoria',
        'Otros datos',
    ]
    
    lista_alumnos = get_all_alumnos()
    if not lista_alumnos:
        lista_alumnos = [('','','','','')]
    
    multi = MultiColumnListbox(frame_container, header_alumnos,lista_alumnos)
    return multi



def init_multilist_matriculas(frame_container, curso:str, horario=None):
    header_matriculas = [
        'Nombre completo',
        'Carnet Identidad',
        'Municipio',
        'Telefono',
        'Horario',
        'Categoria',
        'Otros datos',
    ]
    
    sc = curso.split('-')
    
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])

    horario_final = horario if not horario == 'CURSO COMPLETO' else None
    
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso, horario_final)
        
    if not matriculas_lista:
        matricula_empty = ['' for _ in header_matriculas]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
    
    multi = MultiColumnListbox(frame_container, header_matriculas,matriculas_lista)
    return multi


def actualizar_treeview(treeview:MultiColumnListbox):
    sc = treeview.curso.split('-')
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])

    horario = treeview.horario
    horario_final = horario if not horario == 'CURSO COMPLETO' else None
        
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso, horario_final)
    
    if not matriculas_lista:
        matricula_empty = ['' for _ in range(7)]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
        
    treeview.change(matriculas_lista)
    


def valores_by_cbcursos(cb:Combobox, curso_mostrar=None):
    valores = []
    cursos = get_cursos()
    position_curso = 0
    if cursos:
        for i,item in enumerate(get_cursos()):
            curso = item[0]
            year = str(item[1])
            curso_conform = f'{curso}-{year}' 
            valores.append(curso_conform)
            
            if curso_conform == curso_mostrar:
                position_curso = i
            
        cb['values'] = valores
        
        if not curso_mostrar:
            cb.current(0)
            return
        
        cb.current(position_curso)
        
def valores_by_cbhorario(cb:Combobox, horario_mostrar=None):
    valores = []
    horarios = get_horarios()
    position_horario = 0
    if horarios:
        valores.append('CURSO COMPLETO')
        for i,horario in enumerate(horarios):
            
            valores.append(horario)
            
            if horario == horario_mostrar:
                position_horario = i
            
        cb['values'] = valores
        
        if not horario_mostrar:
            cb.current(0)
            return
        
        cb.current(position_horario)

   
def formato_fecha_natural(fechas:list | tuple):
    fe_inicio = str(fechas[0]).split('/')
    fe_fin = str(fechas[1]).split('/')
    
    d_inicio = int(fe_inicio[0])
    m_inicio = MESES[int(fe_inicio[1])]
    
    d_fin = int(fe_fin[0])
    m_fin = MESES[int(fe_fin[1])]
        
    if m_inicio == m_fin:
        return f'{d_inicio} al {d_fin} de {m_fin}'
    else:
        return f'{d_inicio} de {m_inicio} al {d_fin} de {m_fin}'


def alumnos_para_aula(lista_bruta:list[list]):
    lista_final = []
    for fila in lista_bruta:
        nomb = fila[0]
        ci = fila[1]
        tel = str(fila[2])
        mun = fila[3]

        if tel:
            tels = tel.split(' ')
            tel = ''
            for item in tels:
                if item[0:1] == '5' and len(item) == 8:
                    tel = item
                    break
            
            if tel == '': tel = tels[0]
        
        # agregamos a la nueva fila estos datos, falta la unidad, segun municipio
        unidad = get_unidad_my_municipio(mun)
        
        lista_final.append([nomb,ci,tel,unidad])
    return lista_final 
    
def create_excel_by_curso(curso:str):
    sc = curso.split('-')
    idcurso = get_idcurso_by_curso_year(sc[0], sc[1])
    matr_init = get_matr_init_by_id(idcurso)
    fechas = get_fecha_inicio_fin_by_idcurso(idcurso)
    
    
    # primero vamos a guardar en db las matriculas por horarios
    num_matricula = matr_init
    lista_iniciales = []
    
    for id_hor in get_id_horarios():
        lista_iniciales.append([num_matricula, id_hor])
        matr_final = set_matriculas_by_id_horario_idcurso(id_hor, idcurso, num_matricula)
        num_matricula = matr_final
    
    # vamos pal excel. creamos una lista de objetos tipo cursos.xlsx
    cursos_xlsx = []
    registros_xlsx = []
    aula_xlsx = []

    for inicial in lista_iniciales:
        matricula_inicial = inicial[0]
        horario = get_horario_by_id(inicial[1])[0]
        alumnos_con_dni = get_alumnos_for_excel(idcurso,horario)
        alumnos = [alumno[0] for alumno in alumnos_con_dni]
        alumnos_aula = alumnos_para_aula(alumnos_con_dni)
        
        try: modelo_num = get_modelo_init_by_idcurso(idcurso)
        except: modelo_num = 1
        
        #cursos 
        cursoxls = CursoModelo(matricula_inicial)
        cursoxls.fecha_horario(fechas[0],fechas[1], horario)
        cursoxls.agregar_lote_matriculas(alumnos_con_dni)
        cursos_xlsx.append(cursoxls)
        
        # registro asistencia
        registro_xls = CursoModelo(matricula_inicial)
        registro_xls.fecha_horario(fechas[0],fechas[1], horario)
        registro_xls.agregar_lote_matriculas(alumnos)
        registros_xlsx.append(registro_xls)
    
        # aula modelo
        aula_xls = AulaModelo(matricula_inicial)
        aula_xls.fecha_horario(fechas[0],fechas[1], horario)
        aula_xls.agregar_lote_matriculas(alumnos_aula)
        aula_xlsx.append(aula_xls)
    
    
    ruta = filedialog.askdirectory(title='Elige donde desea crear la carpeta con los documentos guardados')
    
    if ruta:
        # tomando fecha y formateando para la carpeta conenedora de modelos
        nombre_carpeta_final = f'{curso} Curso del {formato_fecha_natural(fechas)}'

        
        ruta_export = path.join(ruta,nombre_carpeta_final)
        if not path.exists(ruta_export): mkdir(ruta_export)
        
        ruta_aula_export = path.join(ruta_export,'Asistencia para aula')
        if not path.exists(ruta_aula_export): mkdir(ruta_aula_export)
        
        for i, cur in enumerate(cursos_xlsx):
            # cursos
            cur.exportar(f'{ruta_export}/Curso {i+modelo_num}.xlsx')
            # registro asistencia
            registros_xlsx[i].exportar(f'{ruta_export}/Registro de asistencia {i+modelo_num}.xlsx')
            # aula
            aula_xlsx[i].exportar(f'{ruta_aula_export}/{i+modelo_num}.xlsx')
                
        abrirCarpeta(ruta_export)
    

def get_new_curso_number():
    id_last_curso = get_last_curso_id()
    curso_full = get_curso_by_id(id_last_curso).split('-')
    curso_number = int(curso_full[0])
    
    return curso_number + 1