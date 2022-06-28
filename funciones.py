from MultiListBox_class import MultiColumnListbox
from db_handler import get_all_alumnos

def init_multilist_alumnos(frame_container):
    header_alumnos = [
        'Nombre completo',
        'Carnet Identidad',
        'Municipio',
        'Telefono',
        'Otros datos',
    ]
    
    ### revisar por que me esta dando NONE get all alumnos
    lista_alumnos = get_all_alumnos()
    print(lista_alumnos)
    if not lista_alumnos:
        lista_alumnos = [('','','','','')]
    
    multi = MultiColumnListbox(frame_container, header_alumnos,lista_alumnos)
    return multi