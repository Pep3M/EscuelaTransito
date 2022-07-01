from tkinter import Button, Frame, Tk, Toplevel
from db_handler import get_all_cat_code, get_horarios, get_municipios
from funciones import init_multilist_matriculas
from tkform_new_matr import Form_new_matric

# Funciones #


def agregar_matricula():
    top = Toplevel()
    top.title('Agregando matricula')
    top.attributes('-topmost', 'true')

    municipios = get_municipios()
    horarios = get_horarios()
    cat_code = get_all_cat_code()

    form = Form_new_matric(top, municipios, horarios, cat_code, treeview)
    def closing():
        print('top cerrado')
    
    top.mainloop()


# VISUAL #

root = Tk()
root.title('Transito matriculas')
root.minsize(width=1000, height=350)

body_frame = Frame(root)
body_frame.pack(expand=True, fill='both')

buttons_frame = Frame(body_frame, width=150, background='green')
buttons_frame.pack(fill='y', side='left')

bt_new_matr = Button(buttons_frame,
                     text='Nueva matricula',
                     command=agregar_matricula)
bt_new_matr.pack()

tree_frame = Frame(body_frame, background='blue')
tree_frame.pack(expand=True, fill='both', side='right')

treeview = init_multilist_matriculas(tree_frame)


root.mainloop()