from tkinter import E, X, Button, Frame, Label, PhotoImage, Tk, Toplevel, font
from tkinter.ttk import Combobox
from db_handler import get_all_cat_code, get_cursos, get_horarios, get_idcurso_by_curso_year, get_municipios, get_view_matriculas_by_idcurso
from funciones import create_excel_by_curso, init_multilist_matriculas
from tkform_new_matr import Form_new_matric

COLOR_DARK_BG = '#1b1e2b'
COLOR_SOFT_BG = '#313446'
COLOR_FB = '#a3a9c9'
COLOR_FB_SOFT = '#444444'

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

def crear_modelos():
    create_excel_by_curso(cb_curso.get())

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
root.iconbitmap('assets/imgs/logo.ico')
root.minsize(width=1200, height=350)
root.geometry('1200x650+50+10')
font_big = font.Font(family='Helvetica', size= '14')
font_middle = font.Font(family='Helvetica', size= '12')


# - Frame body
body_frame = Frame(root)
body_frame.pack(expand=True, fill='both')



# - Frame superior
frame_superior = Frame(body_frame, background=COLOR_DARK_BG, height=50)
frame_superior.pack(fill='x', anchor=E)

img = PhotoImage(file='assets/imgs/logo.png')
lb_logo = Label(frame_superior, image=img, background=COLOR_DARK_BG)
lb_logo.grid(row=0, column=0, padx=15, pady=5)
Label(frame_superior,background=COLOR_DARK_BG, text='').grid(row=0, column=1, padx=10)
Label(frame_superior, text='Curso', background=COLOR_DARK_BG, foreground=COLOR_FB, font=font_big).grid(row=0, column=2)

cb_curso = Combobox(frame_superior, width=8, state='readonly', font=font_big)
cb_curso.grid(row=0,column=3, sticky='e', padx=10, pady=10)
valores_by_cbcursos(cb_curso)
cb_curso.bind("<<ComboboxSelected>>", elegir_curso)



# - Frame de botones (lateral)
buttons_frame = Frame(body_frame, width=150, padx=5,
                      pady=5, background=COLOR_DARK_BG)
buttons_frame.pack(fill='y', side='left')
Label(buttons_frame,text='Matriculas', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack()
bt_new_matr = Button(buttons_frame,
                     text='Nueva matricula',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     command=agregar_matricula)
bt_new_matr.pack(padx=3, pady=5, fill=X)
Label(buttons_frame,text='   ', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack(pady=1) # ---- separador ----

Label(buttons_frame,text='Excel', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack()
bt_crear_modelos = Button(buttons_frame,
                     text='Crear modelos',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     command=crear_modelos
                     )
bt_crear_modelos.pack(padx=3, pady=5)
Label(buttons_frame,text='   ', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack(pady=1) # ---- separador ----

Label(buttons_frame,text='Cursos', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack()
bt_new_curso = Button(buttons_frame,
                     text='Nuevo curso',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     command=agregar_matricula
                     )
bt_new_curso.pack(padx=3, pady=5, fill=X)

# - Frame del treeview (principal)
tree_frame = Frame(body_frame)
tree_frame.pack(expand=True, fill='both', side='right')

treeview = init_multilist_matriculas(tree_frame, cb_curso.get())


root.mainloop()
