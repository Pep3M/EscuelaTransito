from tkinter import Button, Frame, Tk, Toplevel
from db_handler import get_municipios
from funciones import init_multilist_alumnos
from tkform_new_matr import Form_new_matric

# Funciones #


def agregar_matricula():
    top = Toplevel()
    top.title('Agregando matricula')
    top.attributes('-topmost', 'true')

    municipios = get_municipios()

    form = Form_new_matric(top, municipios)
    top.mainloop()
    
    print(form.guardar)


# VISUAL #

root = Tk()
root.title('Transito matriculas')
root.minsize(width=600, height=350)

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

init_multilist_alumnos(tree_frame)

root.mainloop()