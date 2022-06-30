from MultiListBox_class import MultiColumnListbox
from db_handler import get_all_alumnos
from db_constantes import *

def init_multilist_alumnos(frame_container):
    header_alumnos = [
        'Nombre completo',
        'Carnet Identidad',
        'Municipio',
        'Telefono',
        'Otros datos',
    ]
    
    lista_alumnos = get_all_alumnos()
    if not lista_alumnos:
        lista_alumnos = [('','','','','')]
    
    multi = MultiColumnListbox(frame_container, header_alumnos,lista_alumnos)
    return multi


""" 
def init_multilist_matriculas(frame_container):
    header_matriculas = [
        'Nombre completo',
        'Carnet Identidad',
        'Horario',
        'Telefono',
        'Otros datos',
    ]
    
    fetch_matriculas = get_matriculas_by_curso_year(10,2022)
    print(fetch_matriculas)
    matriculas_lista = []
    
    if fetch_matriculas:
        pass
    
    multi = MultiColumnListbox(frame_container, header_matriculas,lista_matriculas)
    return multi

 """
       