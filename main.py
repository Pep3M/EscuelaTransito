from tkinter import E, Button, Frame, Label, Tk, Toplevel
from tkinter.ttk import Combobox
from db_handler import get_all_cat_code, get_cursos, get_horarios, get_idcurso_by_curso_year, get_municipios, get_view_matriculas_by_idcurso
from funciones import init_multilist_matriculas
from tkform_new_matr import Form_new_matric

# Funciones #


def agregar_matricula():
    x = root.winfo_x()
    y = root.winfo_y()

    top = Toplevel()
    w = 340
    h = 325
    top.geometry("%dx%d+%d+%d" % (w, h, x + 350, y + 150))

    top.title('Agregando matricula')
    top.attributes('-topmost', 'true')

    municipios = get_municipios()
    horarios = get_horarios()
    cat_code = get_all_cat_code()

    form = Form_new_matric(top, municipios, horarios, cat_code, treeview)

    top.mainloop()


def valores_by_cbcursos(cb:Combobox):
    valores = []
    for item in get_cursos():
        curso = item[0]
        year = str(item[1])
        valores.append(f'{curso}-{year}')
    cb['values'] = valores
    cb.current(0)
    
    
def elegir_curso(event):
    sc = cb_curso.get().split('-')
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso)
    
    if not matriculas_lista:
        matricula_empty = ['' for _ in range(7)]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
        
    treeview.curso=cb_curso.get()
    treeview.change(matriculas_lista)


# VISUAL #

root = Tk()
root.title('Transito matriculas')
root.minsize(width=1200, height=350)



# - Frame body
body_frame = Frame(root)
body_frame.pack(expand=True, fill='both')



# - Frame superior
frame_superior = Frame(body_frame, background='#1b1e2b', height=50)
frame_superior.pack(fill='x', anchor=E)

Label(frame_superior,background='#1b1e2b', text='').grid(row=0, column=0, padx=550)
Label(frame_superior, text='Curso', background='#1b1e2b', foreground='#a3a9c9', font=('Helvetica 14')).grid(row=0, column=1)

cb_curso = Combobox(frame_superior, background='blue', width=8, state='readonly', font=('Helvetica 14'))
cb_curso.grid(row=0,column=2, sticky='e', padx=10, pady=10)
valores_by_cbcursos(cb_curso)
cb_curso.bind("<<ComboboxSelected>>", elegir_curso)



# - Frame de botones (lateral)
buttons_frame = Frame(body_frame, width=150, padx=5,
                      pady=5, background='#1b1e2b')
buttons_frame.pack(fill='y', side='left')

bt_new_matr = Button(buttons_frame,
                     text='Nueva matricula',
                     background='#313446',
                     foreground='#a3a9c9',
                     command=agregar_matricula)
bt_new_matr.pack()



# - Frame del treeview (principal)
tree_frame = Frame(body_frame)
tree_frame.pack(expand=True, fill='both', side='right')

treeview = init_multilist_matriculas(tree_frame, cb_curso.get())


root.mainloop()
