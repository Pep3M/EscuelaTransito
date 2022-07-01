from MultiListBox_class import MultiColumnListbox
from db_handler import get_all_alumnos, get_idcurso_by_curso_year, get_view_matriculas_by_idcurso
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



def init_multilist_matriculas(frame_container):
    header_matriculas = [
        'Nombre completo',
        'Carnet Identidad',
        'Municipio',
        'Telefono',
        'Horario',
        'Categoria',
        'Otros datos',
    ]
    
    id_curso = get_idcurso_by_curso_year(10,2022)
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso)
    
    
    multi = MultiColumnListbox(frame_container, header_matriculas,matriculas_lista)
    return multi


       