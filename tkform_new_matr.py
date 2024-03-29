from datetime import datetime
from msilib.schema import ComboBox
from tkinter import CENTER, END, Button, Entry, Frame, Label, StringVar, Text, Tk, font
from tkinter.messagebox import showerror
from tkinter.ttk import Combobox
from MultiListBox_class import MultiColumnListbox
from db_handler import actualizar_curso, agregar_curso, agregar_matricula, get_campo_datos_idcursos, get_curso_by_id, get_fecha_inicio_fin_by_idcurso, get_idcurso_by_curso_year, get_matric_model_init_by_idcurso, get_matricula_by_ci_curso, get_new_matric_model_init, get_view_matriculas_by_idcurso
from funciones import actualizar_treeview, formato_fecha_natural, get_new_curso_number, valores_by_cbcursos
from tkcalendar import DateEntry

GREEN_BUTTON = '#1f6e4d'
RED_BUTTON = '#811e1d'


class Form_new_matric:

    def __init__(self, frame_container, municipios, horarios, cat_code,
                 treeview: MultiColumnListbox):
        self.frame_container = frame_container
        self.treeview = treeview
        self.guardar = []

        # StringVars
        self.ci_sv = StringVar()
        self.ci_sv.trace('w', self.callback_ci_entry)
        self.name_sv = StringVar()
        self.name_sv.trace('w', self.name_on_change)
        self.tel_sv = StringVar()
        self.tel_sv.trace('w', self.callback_tel)
        # labels
        self.lb_name = Label(self.frame_container,
                             text='Nombre(s) y apellidos')
        self.lb_ci = Label(self.frame_container, text='Carnet de Identidad')
        self.lb_tel = Label(self.frame_container, text='Telefono')
        self.lb_municipio = Label(self.frame_container, text='Municipio')
        self.lb_categoria = Label(self.frame_container, text='Categoria')
        self.lb_horario = Label(self.frame_container, text='Horario')
        self.lb_datos = Label(self.frame_container, text='Otros datos')
        # labels grid
        self.lb_name.grid(row=1, column=0, sticky='w', pady=5, padx=10)
        self.lb_ci.grid(row=2, column=0, sticky='w', pady=5, padx=10)
        self.lb_tel.grid(row=3, column=0, sticky='w', pady=5, padx=10)
        self.lb_municipio.grid(row=4, column=0, sticky='w', pady=5, padx=10)
        self.lb_categoria.grid(row=5, column=0, sticky='w', pady=5, padx=10)
        self.lb_horario.grid(row=6, column=0, sticky='w', pady=5, padx=10)
        self.lb_datos.grid(row=7, column=0, sticky='wn', pady=5, padx=10)

        # entrys
        self.e_name = Entry(self.frame_container,
                            textvariable=self.name_sv,
                            width=30)
        self.e_ci = Entry(self.frame_container,
                          textvariable=self.ci_sv,
                          width=30)
        self.e_tel = Entry(self.frame_container, width=30, textvariable=self.tel_sv)
        self.e_municipio = self.combobox(municipios, width=27)
        self.e_categoria = self.combobox(cat_code, width=27)
        self.e_horario = self.combobox(horarios, width=27)
        pos = self.posicion_horario()
        self.e_horario.current(pos)
        self.e_datos = Entry(self.frame_container, width=30)
        # entrys grid
        self.e_name.grid(row=1, column=1, sticky='w', pady=5)
        self.e_ci.grid(row=2, column=1, sticky='w', pady=5)
        self.e_tel.grid(row=3, column=1, sticky='w', pady=5)
        self.e_municipio.grid(row=4, column=1, sticky='w', pady=5)
        self.e_categoria.grid(row=5, column=1, sticky='w', pady=5)
        self.e_horario.grid(row=6, column=1, sticky='w', pady=5)
        self.e_datos.grid(row=7, column=1, sticky='w', pady=5)

        self.e_name.focus_set()

        self.frame_bts = Frame(self.frame_container)
        self.frame_bts.grid(row=8, column=1, sticky='e')

        self.bt_aceptar = Button(self.frame_bts,
                                 text='Agregar',
                                 command=self.aceptar,
                                 background=GREEN_BUTTON,
                                 fg='white',
                                 width=8)
        self.bt_aceptar.grid(row=0, column=0, padx=10, pady=10)
        self.bt_cancelar = Button(self.frame_bts,
                                  text='Cancelar',
                                  command=self.cancelar,
                                  bg=RED_BUTTON,
                                  fg='white',
                                  width=8)
        self.bt_cancelar.grid(row=0, column=1, padx=10, pady=10)

        self.e_name.bind('<FocusOut>', self.event_change_name)
        self.frame_container.bind('<Return>', self.bind_aceptar)
        self.frame_container.bind('<Escape>', self.bind_cancelar)

    def aceptar(self):
        self.guardar.clear()
        self.guardar.append(self.e_name.get().strip())
        self.guardar.append(self.e_ci.get().strip())
        self.guardar.append(self.e_municipio.get().strip())
        self.guardar.append(self.e_tel.get().strip())
        self.guardar.append(self.e_horario.get().strip())
        self.guardar.append(self.e_datos.get().strip())
        self.guardar.append(self.e_categoria.get().strip())

        ci_data_dupl = self.ci_duplicado_en_matricula()
        if not self.check_required_fields():
            showerror(
                'Faltan campos requerido',
                'Compruebe que el campo "Nombre(s) y apellidos" y "Carnet de Identidad" esten correctamente llenados'
            )
            self.e_name.focus()
        elif ci_data_dupl:
            showerror(
                'Matricula duplicada',
                f'Esta tratando de agregar una matricula cuyo Carnet de Identidad coicide con un alumno ya agregado previamente a este curso.\n\nAlumno: {ci_data_dupl[0]} en el horario de {ci_data_dupl[1]}'
            )
            self.e_name.focus()
        else:
            #metodo externo no reutilizable
            sc = self.treeview.curso.split('-')

            agregar_matricula(self.guardar, sc[0], sc[1])

            self.frame_container.destroy()
            actualizar_treeview(self.treeview)

    def cancelar(self):
        self.frame_container.destroy()

    def combobox(self, valores, width=20, modo=True):
        estado = 'readonly' if modo else 'normal'
        self.box = Combobox(self.frame_container, width=width, state=estado)
        self.box['values'] = valores
        self.box.current(0)  # Selecciona el primer elemento de la tupla.
        self.box.bind("<<ComboboxSelected>>", self.combobox_elegir)
        return self.box

    def combobox_elegir(self, evento):
        #self.valor.set(self.box.get())
        pass
    
    def posicion_horario(self):
        horario = self.treeview.horario
        horario_final = horario if not horario == 'CURSO COMPLETO' else None
        if horario_final:
            for i, hor in enumerate(self.e_horario['values']):
                print(hor, horario_final)
                if hor == horario_final:
                    return i
                
            return 0

    def ci_duplicado_en_matricula(self):
        sc = self.treeview.curso.split('-')
        id_curso = get_idcurso_by_curso_year(sc[0], sc[1])

        return get_matricula_by_ci_curso(self.ci_sv.get(), id_curso)

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
        self.e_name.delete(0, 'end')
        self.e_name.insert(0, capitalizado)

    def capitalizar_palabras(self, frase: str):
        palabras: list[str] = frase.split(' ')
        mayus_palabras = [palabra.capitalize() for palabra in palabras]
        return ' '.join(mayus_palabras)

    def callback_ci_entry(self, *args):
        ci = self.ci_sv.get()
        if not len(ci) == 11 or not ci.isdigit():
            self.e_ci.config(foreground='red')
        else:
            self.e_ci.config(foreground='black')

    def name_on_change(self, *args):
        text = self.name_sv.get()

        if text and text[-1:].isdigit():
            self.name_sv.set(text[:-1])
            self.ci_sv.set(self.ci_sv.get()+text[-1:])
            self.e_ci.focus()
            self.e_ci.icursor(len(self.ci_sv.get()))
            
    def callback_tel(self, *args):
        tel = self.tel_sv.get()
        if tel and not tel[-1:].isdigit() and not tel[-1:] == ' ':
            self.tel_sv.set(tel[:-1])
    
class Form_curso():

    def __init__(self, frame_father: Frame | Tk, treeview: MultiColumnListbox,
                 combobox, lb_fecha) -> None:

        year_hoy = datetime.now().year
        matr_model_init = get_new_matric_model_init()
        new_curso_number = get_new_curso_number()

        self.frame_father = frame_father
        self.frame_container = Frame(frame_father)
        self.frame_container.pack(padx=10, pady=10)
        self.combobox = combobox
        self.lb_fecha = lb_fecha
        self.treeview = treeview

        # StringVar
        self.sv_name = StringVar()
        self.sv_name.set(new_curso_number)
        self.sv_year = StringVar()
        self.sv_year.set(year_hoy)
        self.sv_fechaini = StringVar()
        self.sv_fechafin = StringVar()
        self.sv_datos = StringVar()
        self.sv_matr_ini = StringVar()
        self.sv_matr_ini.set(matr_model_init[0])
        self.sv_model_ini = StringVar()
        self.sv_model_ini.set(matr_model_init[1])

        # labels
        self.lb_name = Label(self.frame_container, text='Curso')
        self.lb_year = Label(self.frame_container, text='Año')
        self.lb_fecha_ini = Label(self.frame_container, text='Fecha inicio')
        self.lb_fecha_fin = Label(self.frame_container, text='Fecha final')
        self.lb_datos = Label(self.frame_container, text='Otros datos')
        frame_numbers = Frame(self.frame_container, bg='#dddddd', padx=5, pady=5)
        Label(frame_numbers, text='Valores iniciales del curso (no modificar)', bg='#dddddd').grid(row=0, column=0, columnspan=2, sticky='ew', pady=5, padx=10)
        Label(frame_numbers, text='Matricula', bg='#dddddd').grid(row=1, column=0, sticky='ew', pady=2, padx=5)
        Label(frame_numbers, text='Modelos', bg='#dddddd').grid(row=1, column=1, sticky='ew', pady=2, padx=5)
        # labels grid
        self.lb_name.grid(row=1, column=0, sticky='w', pady=5, padx=10)
        self.lb_year.grid(row=2, column=0, sticky='w', pady=5, padx=10)
        self.lb_fecha_ini.grid(row=3, column=0, sticky='w', pady=5, padx=10)
        self.lb_fecha_fin.grid(row=4, column=0, sticky='w', pady=5, padx=10)
        self.lb_datos.grid(row=5, column=0, sticky='wn', pady=5, padx=10)
        frame_numbers.grid(row=6, column=0, columnspan=2, sticky='w', pady=10, padx=10)

        # entrys
        self.e_name = Entry(self.frame_container,
                            textvariable=self.sv_name,
                            width=15)
        self.e_year = Entry(self.frame_container,
                            textvariable=self.sv_year,
                            width=15)
        self.e_fechaini = DateEntry(self.frame_container,
                                    values='Text',
                                    state='readonly',
                                    date_pattern='dd/mm/yyyy',
                                    textvariable=self.sv_fechaini)
        self.e_fechafin = DateEntry(self.frame_container,
                                    values='Text',
                                    state='readonly',
                                    date_pattern='dd/mm/yyyy',
                                    textvariable=self.sv_fechafin)
        self.e_datos = Entry(self.frame_container,
                             textvariable=self.sv_datos,
                             width=15)
        self.e_matr_ini = Entry(frame_numbers,
                             textvariable=self.sv_matr_ini,
                             width=8, justify=CENTER)
        self.e_model_ini = Entry(frame_numbers,
                             textvariable=self.sv_model_ini,
                             width=8, justify=CENTER)
        # entrys grid
        self.e_name.grid(row=1, column=1, sticky='w', pady=5)
        self.e_year.grid(row=2, column=1, sticky='w', pady=5)
        self.e_fechaini.grid(row=3, column=1, sticky='w', pady=5)
        self.e_fechafin.grid(row=4, column=1, sticky='w', pady=5)
        self.e_datos.grid(row=5, column=1, sticky='w', pady=5)
        self.e_matr_ini.grid(row=2, column=0, pady=5)
        self.e_model_ini.grid(row=2, column=1, pady=5)

        self.e_name.focus()
        self.e_name.selection_to(END)
        """ self.frame_bts = Frame(self.frame_container)
        self.frame_bts.grid(row=8, column=1, rowspan=2, sticky='e') """

        self.bt_aceptar = Button(self.frame_container,
                                 text='Agregar',
                                 command=self.aceptar,
                                 background=GREEN_BUTTON,
                                 fg='white',
                                 width=8)
        self.bt_aceptar.grid(row=8, column=0, padx=10, pady=20, sticky='e')
        self.bt_cancelar = Button(self.frame_container,
                                  text='Cancelar',
                                  command=self.cancelar,
                                  bg=RED_BUTTON,
                                  fg='white',
                                  width=8)
        self.bt_cancelar.grid(row=8, column=1, padx=10, pady=20, sticky='w')

        self.e_name.bind('<FocusOut>', self.bind_check_dos_dig)
        self.frame_father.bind('<Return>', self.bind_aceptar)
        self.frame_father.bind('<Escape>', self.bind_cancelar)

    def aceptar(self):
        self.dos_digitos_en_name_curso()

        name_curso = self.sv_name.get()
        year = self.sv_year.get()
        f_ini = self.sv_fechaini.get()
        f_fin = self.sv_fechafin.get()
        datos = self.sv_datos.get()
        matr_ini = self.sv_matr_ini.get()
        model_ini = self.sv_model_ini.get()

        if not self.check_required_fields():
            showerror(
                'Faltan campos requerido',
                'Compruebe que los campos "Curso" y "Año" esten correctamente llenados'
            )
        else:
            #metodo externo no reutilizable
            id_curso_agregado = agregar_curso(name_curso, year, f_ini, f_fin,
                                              datos, matr_ini, model_ini)

            if id_curso_agregado == 0:
                showerror(
                    'Error al agregar el curso',
                    'No se pudo agregar el curso, revice bien los campos o pongase en contacto con su programador'
                )
                return

            self.frame_father.destroy()
            valores_by_cbcursos(self.combobox, f'{name_curso}-{year}')
            self.elegir_curso(id_curso_agregado, self.lb_fecha)

    def cancelar(self):
        self.frame_father.destroy()

    def check_required_fields(self):
        return self.sv_name.get() and self.sv_year.get()

    def dos_digitos_en_name_curso(self):
        self.sv_name.set(self.sv_name.get().strip())
        if len(self.sv_name.get()) == 1:
            self.sv_name.set(f'0{self.sv_name.get()}')

    def elegir_curso(self, id_curso, lb_fecha):

        horario = self.treeview.horario
        horario_final = horario if not horario == 'CURSO COMPLETO' else None

        matriculas_lista = get_view_matriculas_by_idcurso(
            id_curso, horario_final)
        fechas = get_fecha_inicio_fin_by_idcurso(id_curso)
        curso = get_curso_by_id(id_curso, curso_formateado=True)

        if not matriculas_lista:
            matricula_empty = ['' for _ in range(7)]
            matriculas_lista = []
            matriculas_lista.append(matricula_empty)

        lb_fecha.config(text=formato_fecha_natural(fechas))
        self.treeview.curso = curso
        self.treeview.change(matriculas_lista)

    # ---- BIND METHODS ----
    def bind_check_dos_dig(self, evento):
        self.dos_digitos_en_name_curso()

    def bind_aceptar(self, evento):
        self.aceptar()

    def bind_cancelar(self, evento):
        self.cancelar()


class Form_edit_curso(Form_curso):

    def __init__(self, frame_father: Frame | Tk, treeview: MultiColumnListbox,
                 combobox: Combobox, lb_fecha) -> None:
        super().__init__(frame_father, treeview, combobox, lb_fecha)
        
        curso_year = combobox.get().split('-')
        curso_name = curso_year[0]
        curso_year = curso_year[1]
        self.id_curso = get_idcurso_by_curso_year(curso_name, curso_year)
        fechas = get_fecha_inicio_fin_by_idcurso(self.id_curso)
        datos = get_campo_datos_idcursos(self.id_curso)
        if not datos:
            datos = ''
        matri_model_ini = get_matric_model_init_by_idcurso(self.id_curso)
        matr_ini = matri_model_ini[0]
        model_ini = matri_model_ini[1]

        self.sv_name.set(curso_name)
        self.sv_year.set(curso_year)
        self.sv_fechaini.set(fechas[0])
        self.sv_fechafin.set(fechas[1])
        self.sv_datos.set(datos)
        self.sv_matr_ini.set(matr_ini)
        self.sv_model_ini.set(model_ini)

        self.e_name.selection_adjust(END)

        self.bt_aceptar.config(text='Actualizar')

    def aceptar(self):
        self.dos_digitos_en_name_curso()

        name_curso = self.sv_name.get()
        year = self.sv_year.get()
        f_ini = self.sv_fechaini.get()
        f_fin = self.sv_fechafin.get()
        datos = self.sv_datos.get()
        matr_ini = self.sv_matr_ini.get()
        model_ini = self.sv_model_ini.get()

        if not self.check_required_fields():
            showerror(
                'Faltan campos requerido',
                'Compruebe que los campos "Curso" y "Año" esten correctamente llenados'
            )
        else:
            actualizar_curso(self.id_curso, name_curso, year, f_ini, f_fin,
                             datos, matr_ini, model_ini)

            self.frame_father.destroy()
            valores_by_cbcursos(self.combobox, f'{name_curso}-{year}')
            self.elegir_curso(self.id_curso, self.lb_fecha)


if __name__ == '__main__':

    root = Tk()
    form = Form_edit_curso()
    root.mainloop()