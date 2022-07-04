from tkinter import E, RIGHT, X, Button, Frame, Label, PhotoImage, StringVar, Tk, Toplevel, font
from tkinter.messagebox import askquestion, showwarning
from tkinter.ttk import Combobox
from db_handler import eliminar_curso, get_all_cat_code,get_fecha_inicio_fin_by_idcurso, get_horarios, get_idcurso_by_curso_year, get_municipios, get_view_matriculas_by_idcurso
from funciones import actualizar_treeview, create_excel_by_curso, formato_fecha_natural, init_multilist_matriculas, valores_by_cbcursos
from tkform_new_matr import Form_curso, Form_edit_curso, Form_new_matric

COLOR_DARK_BG = '#1b1e2b'
COLOR_SOFT_BG = '#313446'
COLOR_FB = '#a3a9c9'
COLOR_FB_SOFT = '#444444'
COLOR_RED_DEL = '#943444'

# Funciones #


def agregar_matricula():
    x = root.winfo_x()
    y = root.winfo_y()

    top = Toplevel()
    w = 340
    h = 270
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
    
def crear_curso():
    x = root.winfo_x()
    y = root.winfo_y()

    top = Toplevel()
    w = 300
    h = 220
    top.geometry("%dx%d+%d+%d" % (w, h, x + 350, y + 150))

    top.title('Agregando curso')
    top.attributes('-topmost', 'true')
    
    form = Form_curso(top, treeview, cb_curso, lb_fecha)
    top.mainloop()
    
    
def editar_curso():
    x = root.winfo_x()
    y = root.winfo_y()

    top = Toplevel()
    w = 300
    h = 220
    top.geometry("%dx%d+%d+%d" % (w, h, x + 350, y + 150))

    top.title('Agregando curso')
    top.attributes('-topmost', 'true')
    
    form = Form_edit_curso(top, treeview, cb_curso, lb_fecha)
    top.mainloop()
    
def del_curso():
    sc = cb_curso.get().split('-')
    
    confirmation = askquestion('Eliminar curso',f'Desea eliminar el curso {cb_curso.get()}?\n\nCUIDADO! Al eliminar este curso, se eliminarán todas las matriculas que haya hecho en el. Esta accion no puede deshacerse')
    
    if confirmation == 'yes':
        id_curso = get_idcurso_by_curso_year(sc[0],sc[1])
        eliminar_curso(id_curso)
        valores_by_cbcursos(cb_curso)
        treeview.curso = cb_curso.get()
        actualizar_treeview(treeview)
    
    
def valores_fechas():
    sc = cb_curso.get().split('-')
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])
    fechas = get_fecha_inicio_fin_by_idcurso(id_curso)
    lb_fecha.config(text=formato_fecha_natural(fechas))

    
def elegir_curso(event):
    sc = cb_curso.get().split('-')
    id_curso = get_idcurso_by_curso_year(sc[0],sc[1])
    matriculas_lista = get_view_matriculas_by_idcurso(id_curso)
    fechas = get_fecha_inicio_fin_by_idcurso(id_curso)
    
    if not matriculas_lista:
        matricula_empty = ['' for _ in range(7)]
        matriculas_lista = []
        matriculas_lista.append(matricula_empty)
        
    lb_fecha.config(text=formato_fecha_natural(fechas))
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

lb_fecha = Label(frame_superior, text='',background=COLOR_DARK_BG, foreground=COLOR_FB, font=font_middle)
lb_fecha.grid(row=0,column=4)
valores_fechas()

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

Label(buttons_frame,text='Excel', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack(fill=X)
bt_crear_modelos = Button(buttons_frame,
                     text='Crear modelos',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     command=crear_modelos
                     )
bt_crear_modelos.pack(padx=3, pady=5, fill=X)
Label(buttons_frame,text='   ', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack(pady=1) # ---- separador ----

Label(buttons_frame,text='Cursos', background=COLOR_DARK_BG, foreground=COLOR_FB_SOFT).pack(fill=X)
bt_new_curso = Button(buttons_frame,
                     text='Nuevo curso',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     command=crear_curso
                     )
bt_new_curso.pack(padx=3, pady=5, fill=X)
frame_curso_edit_del = Frame(buttons_frame, bg=COLOR_DARK_BG)
frame_curso_edit_del.pack(fill=X)
bt_edit_curso = Button(frame_curso_edit_del,
                     text='Editar',
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle,
                     width=10,
                     command=editar_curso
                     )
bt_edit_curso.grid(row=0,column=0, padx=3, pady=5)
img_trash = PhotoImage(file='assets/imgs/trash.png')
bt_del_curso = Button(frame_curso_edit_del,
                     background=COLOR_SOFT_BG,
                     foreground=COLOR_FB,
                     font=font_middle, 
                     image=img_trash,
                     bg=COLOR_RED_DEL,
                     width=25,
                     height=25,
                     command=del_curso
                     )
bt_del_curso.grid(row=0, column=1, padx=3, pady=5)

# - Frame del treeview (principal)
tree_frame = Frame(body_frame)
tree_frame.pack(expand=True, fill='both', side='right')

treeview = init_multilist_matriculas(tree_frame, cb_curso.get())


root.mainloop()
