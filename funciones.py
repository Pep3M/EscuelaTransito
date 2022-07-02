from os import mkdir, path
from tkinter import filedialog
from MultiListBox_class import MultiColumnListbox
from curso_modelo import CursoModelo
from db_handler import get_all_alumnos, get_alumnos_for_excel, get_horario_by_id, get_id_horarios, get_idcurso_by_curso_year, get_matr_init_by_id, get_view_matriculas_by_idcurso, set_matriculas_by_id_horario_idcurso
from cmd_abrir_carpeta_explorer import abrirCarpeta
from db_constantes import *

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



def init_multilist_matriculas(frame_container, curso:str):
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
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso)
    
    if not matriculas_lista:
        matricula_empty = ['' for _ in header_matriculas]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
    
    multi = MultiColumnListbox(frame_container, header_matriculas,matriculas_lista)
    return multi


def actualizar_treeview(treeview:MultiColumnListbox):
    sc = treeview.curso.split('-')
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso)
    
    if not matriculas_lista:
        matricula_empty = ['' for _ in range(7)]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
        
    treeview.change(matriculas_lista)
    
    
def create_excel_by_curso(curso:str):
    sc = curso.split('-')
    idcurso = get_idcurso_by_curso_year(sc[0], sc[1])
    matr_init = get_matr_init_by_id(idcurso)
    
    # primero vamos a guardar en db las matriculas por horarios
    num_matricula = matr_init
    lista_iniciales = []
    
    for id_hor in get_id_horarios():
        lista_iniciales.append([num_matricula, id_hor])
        matr_final = set_matriculas_by_id_horario_idcurso(id_hor, idcurso, num_matricula)
        num_matricula = matr_final
    
    # vamos pal excel. creamos una lista de objetos tipo cursos.xlsx
    cursos_xlsx = []

    for inicial in lista_iniciales:
        matricula_inicial = inicial[0]
        horario = get_horario_by_id(inicial[1])[0]
        alumnos = get_alumnos_for_excel(idcurso,horario)
        
        cursoxls = CursoModelo(matricula_inicial)
        cursoxls.fecha_horario('1/06/2022','10/06/2022', horario)
        cursoxls.agregar_lote_matriculas(alumnos)
        
        cursos_xlsx.append(cursoxls)
    
    
    ruta = filedialog.askdirectory(title='Elige donde desea crear la carpeta con los documentos guardados')
    
    if ruta:
        ruta_export = path.join(ruta,curso)
        if not path.exists(ruta_export): mkdir(ruta_export)
        
        for i, cur in enumerate(cursos_xlsx):
            cur.exportar(f'{ruta_export}/curso {i+1}.xlsx')
                
        abrirCarpeta(ruta_export)
    
    