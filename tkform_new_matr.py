
from msilib.schema import ComboBox
from tkinter import END, Button, Entry, Frame, Label, StringVar, Text, Tk
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox
from MultiListBox_class import MultiColumnListbox
from db_handler import agregar_matricula

from db_handler import get_municipios
from funciones import actualizar_treeview


class Form_new_matric:
    
    def __init__(self, frame_container, municipios, horarios, cat_code, treeview:MultiColumnListbox):
        self.frame_container = frame_container
        self.treeview = treeview
        self.guardar = []
        # labels
        self.lb_name = Label(self.frame_container, text='Nombre(s) y apellidos')
        self.lb_ci = Label(self.frame_container, text='Carnet de Identidad')
        self.lb_municipio = Label(self.frame_container, text='Municipio')
        self.lb_tel = Label(self.frame_container, text='Telefono')
        self.lb_horario = Label(self.frame_container, text='Horario')
        self.lb_categoria = Label(self.frame_container, text='Categoria')
        self.lb_datos = Label(self.frame_container, text='Otros datos')
        # labels grid
        self.lb_name.grid(row=1,column=0, sticky='w', pady=5, padx=10)
        self.lb_ci.grid(row=2,column=0, sticky='w', pady=5, padx=10)
        self.lb_municipio.grid(row=3,column=0, sticky='w', pady=5, padx=10)
        self.lb_tel.grid(row=4,column=0, sticky='w', pady=5, padx=10)
        self.lb_horario.grid(row=5,column=0, sticky='w', pady=5, padx=10)
        self.lb_categoria.grid(row=6,column=0, sticky='w', pady=5, padx=10)
        self.lb_datos.grid(row=7,column=0, sticky='wn', pady=5, padx=10)
        
        # entrys
        self.e_name = Entry(self.frame_container, width=30)
        self.e_ci = Entry(self.frame_container, width=30)
        self.e_municipio = self.combobox(municipios, width=27)
        self.e_tel = Entry(self.frame_container, width=10)
        self.e_horario = self.combobox(horarios, width=27)
        self.e_categoria = self.combobox(cat_code, width=27)
        self.e_datos = Text(self.frame_container, width=22, height=4,)
        # entrys grid
        self.e_name.grid(row=1,column=1, sticky='w', pady=5)
        self.e_ci.grid(row=2,column=1, sticky='w', pady=5)
        self.e_municipio.grid(row=3,column=1, sticky='w', pady=5)
        self.e_tel.grid(row=4,column=1, sticky='w', pady=5)
        self.e_horario.grid(row=5,column=1, sticky='w', pady=5)
        self.e_categoria.grid(row=6,column=1, sticky='w', pady=5)
        self.e_datos.grid(row=7,column=1, sticky='w', pady=5)
        
        self.e_name.focus_set()
    
        self.frame_bts = Frame(self.frame_container)
        self.frame_bts.grid(row=8, column=1, sticky='e')
        
        self.bt_aceptar = Button(self.frame_bts, text='Agregar', command=self.aceptar)
        self.bt_aceptar.grid(row=0, column=0, padx=10, pady=10)
        self.bt_cancelar = Button(self.frame_bts, text='Cancelar', command= self.cancelar)
        self.bt_cancelar.grid(row=0, column=1, padx=10, pady=10)
        
    
    def aceptar(self):
        self.guardar.clear()
        self.guardar.append(self.e_name.get())
        self.guardar.append(self.e_ci.get())
        self.guardar.append(self.e_municipio.get())
        self.guardar.append(self.e_tel.get())
        self.guardar.append(self.e_horario.get())
        self.guardar.append(self.e_datos.get('1.0',END))
        self.guardar.append(self.e_categoria.get())
        
        if not self.check_required_fields():
            showerror('Faltan campos requerido','Compruebe que el campo "Nombre(s) y apellidos" y "Carnet de Identidad" esten correctamente llenados')
        else:
            #metodo externo no reutilizable
            sc = self.treeview.curso.split('-')
            
            agregar_matricula(self.guardar, sc[0],sc[1])
            
            self.frame_container.destroy()
            actualizar_treeview(self.treeview)
    
    def cancelar(self):
        self.frame_container.destroy()
        
    
    def combobox(self, valores, width=20, modo=True):
        estado = 'readonly' if modo else 'normal'
        self.box = Combobox(self.frame_container, width=width,
                                state=estado)
        self.box['values'] = valores
        self.box.current(0)  # Selecciona el primer elemento de la tupla.
        self.box.bind("<<ComboboxSelected>>", self.combobox_elegir)
        return self.box
    
    def combobox_elegir(self, evento):
        #self.valor.set(self.box.get())
        pass

    def check_required_fields(self):
        return self.e_name.get() and self.e_ci.get()



if __name__ == '__main__':
    root = Tk()
    munic = get_municipios()
    form = Form_new_matric(root, munic)
    root.mainloop()
    
    if len(form.guardar) > 0:
        print(form.guardar[1])