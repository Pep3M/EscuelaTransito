
from msilib.schema import ComboBox
from tkinter import END, Button, Entry, Frame, Label, StringVar, Text, Tk, font
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox
from MultiListBox_class import MultiColumnListbox
from db_handler import agregar_matricula
from funciones import actualizar_treeview
from tkcalendar import Calendar, DateEntry


GREEN_BUTTON = '#1f6e4d'
RED_BUTTON = '#811e1d'

class Form_new_matric:
    
    def __init__(self, frame_container, municipios, horarios, cat_code, treeview:MultiColumnListbox):
        self.frame_container = frame_container
        self.treeview = treeview
        self.guardar = []
        # StringVars
        self.ci_sv = StringVar()
        self.ci_sv.trace('w', self.callback_ci_entry)
        self.name_sv = StringVar()
        # labels
        self.lb_name = Label(self.frame_container, text='Nombre(s) y apellidos')
        self.lb_ci = Label(self.frame_container, text='Carnet de Identidad')
        self.lb_tel = Label(self.frame_container, text='Telefono')
        self.lb_municipio = Label(self.frame_container, text='Municipio')
        self.lb_categoria = Label(self.frame_container, text='Categoria')
        self.lb_horario = Label(self.frame_container, text='Horario')
        self.lb_datos = Label(self.frame_container, text='Otros datos')
        # labels grid
        self.lb_name.grid(row=1,column=0, sticky='w', pady=5, padx=10)
        self.lb_ci.grid(row=2,column=0, sticky='w', pady=5, padx=10)
        self.lb_tel.grid(row=3,column=0, sticky='w', pady=5, padx=10)
        self.lb_municipio.grid(row=4,column=0, sticky='w', pady=5, padx=10)
        self.lb_categoria.grid(row=5,column=0, sticky='w', pady=5, padx=10)
        self.lb_horario.grid(row=6,column=0, sticky='w', pady=5, padx=10)
        self.lb_datos.grid(row=7,column=0, sticky='wn', pady=5, padx=10)
        
        # entrys
        self.e_name = Entry(self.frame_container, textvariable=self.name_sv, width=30)
        self.e_ci = Entry(self.frame_container, textvariable= self.ci_sv, width=30)
        self.e_tel = Entry(self.frame_container, width=10)
        self.e_municipio = self.combobox(municipios, width=27)
        self.e_categoria = self.combobox(cat_code, width=27)
        self.e_horario = self.combobox(horarios, width=27)
        self.e_datos = Entry(self.frame_container, width=30)
        # entrys grid
        self.e_name.grid(row=1,column=1, sticky='w', pady=5)
        self.e_ci.grid(row=2,column=1, sticky='w', pady=5)
        self.e_tel.grid(row=3,column=1, sticky='w', pady=5)
        self.e_municipio.grid(row=4,column=1, sticky='w', pady=5)
        self.e_categoria.grid(row=5,column=1, sticky='w', pady=5)
        self.e_horario.grid(row=6,column=1, sticky='w', pady=5)
        self.e_datos.grid(row=7,column=1, sticky='w', pady=5)
        
        self.e_name.focus_set()
    
        self.frame_bts = Frame(self.frame_container)
        self.frame_bts.grid(row=8, column=1, sticky='e')
        
        self.bt_aceptar = Button(self.frame_bts, text='Agregar', command=self.aceptar, background=GREEN_BUTTON, fg='white', width=8)
        self.bt_aceptar.grid(row=0, column=0, padx=10, pady=10)
        self.bt_cancelar = Button(self.frame_bts, text='Cancelar', command= self.cancelar, bg=RED_BUTTON, fg='white', width=8)
        self.bt_cancelar.grid(row=0, column=1, padx=10, pady=10)
        
        self.e_name.bind('<FocusOut>', self.event_change_name)
        self.frame_container.bind('<Return>', self.bind_aceptar)
        self.frame_container.bind('<Escape>', self.bind_cancelar)
    
    def aceptar(self):
        self.guardar.clear()
        self.guardar.append(self.e_name.get())
        self.guardar.append(self.e_ci.get())
        self.guardar.append(self.e_municipio.get())
        self.guardar.append(self.e_tel.get())
        self.guardar.append(self.e_horario.get())
        self.guardar.append(self.e_datos.get())
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
    
    # ---- BIND METHODS ----
    def bind_aceptar(self, evento):
        self.aceptar()
        pass
    
    def bind_cancelar(self, evento):
        self.cancelar()
        pass
    
    def event_change_name(self, e):
        capitalizado = self.capitalizar_palabras(self.name_sv.get())
        self.e_name.delete(0,'end')
        self.e_name.insert(0,capitalizado)
    
    def capitalizar_palabras(self, frase:str):
        palabras:list[str] = frase.split(' ')
        mayus_palabras = [palabra.capitalize() for palabra in palabras]
        return ' '.join(mayus_palabras)

    def callback_ci_entry(self, *args):
        ci = self.ci_sv.get()
        if not ci == "" and not len(ci) == 11 or not ci.isdigit():
            self.e_ci.config(foreground='red')
        else:
            self.e_ci.config(foreground='black')



class Form_curso():
    
    def __init__(self, frame_container:Frame | Tk, treeview:MultiColumnListbox) -> None:
        
        self.frame_container = frame_container
        # StringVar
        self.sv_name = StringVar()
        self.sv_year = StringVar()
        self.sv_fechaini = StringVar()
        self.sv_fechafin = StringVar()
        self.sv_datos = StringVar()
        
        # labels
        self.lb_name = Label(self.frame_container, text='Curso')
        self.lb_year = Label(self.frame_container, text='Año')
        self.lb_fecha_ini = Label(self.frame_container, text='Fecha inicio')
        self.lb_fecha_fin = Label(self.frame_container, text='Fecha final')
        self.lb_datos = Label(self.frame_container, text='Otros datos')
        # labels grid
        self.lb_name.grid(row=1,column=0, sticky='w', pady=5, padx=10)
        self.lb_year.grid(row=2,column=0, sticky='w', pady=5, padx=10)
        self.lb_fecha_ini.grid(row=3,column=0, sticky='w', pady=5, padx=10)
        self.lb_fecha_fin.grid(row=4,column=0, sticky='w', pady=5, padx=10)
        self.lb_datos.grid(row=5,column=0, sticky='wn', pady=5, padx=10)
        
        # entrys
        self.e_name = Entry(self.frame_container, textvariable=self.sv_name, width=30)
        self.e_year = Entry(self.frame_container, textvariable= self.sv_year, width=30)
        self.e_datos = Entry(self.frame_container, textvariable=self.sv_datos)
        # entrys grid
        self.e_name.grid(row=1,column=1, sticky='w', pady=5)
        self.e_year.grid(row=2,column=1, sticky='w', pady=5)
        self.e_datos.grid(row=7,column=1, sticky='w', pady=5)
        
        self.e_name.focus_set()






if __name__ == '__main__':


    
    
    """ root = Tk()
    munic = get_municipios()
    form = Form_new_matric(root, munic)
    root.mainloop()
    
    if len(form.guardar) > 0:
        print(form.guardar[1]) """