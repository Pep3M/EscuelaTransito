'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
from tkinter import CENTER, END, EW, LEFT, RIGHT, W, Button, StringVar, Text, Entry, Frame, Label, Toplevel, messagebox
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from db_handler import actualizar_matricula, eliminar_matr_by_ci_and_curso, get_all_cat_code, get_cursos, get_cursos_by_ci, get_horarios, get_idcurso_by_curso_year, get_last_curso_id, get_matricula_by_ci_curso, get_municipios, get_view_matriculas_by_idcurso
from general_constants import *




class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, frame_container: tk.Frame, column_header, list: list):
        """
        Constructor de la clase MultiColumnListBox. Genera una lista con encabezados. Necesita un frame contenedor (tkinter), una lista de encabezado y una lista de tuplas, donde el largo de cada una es igual al largo de la lista de encabezado

        Args:
            frame_container (tk.Frame): Frame que contendra este objeto
            column_header (list): Una lista de cada encabezado
            list (list[tuple | list]): Una lista de tuplas. Cada tupla representa una fila
        """
        self.myFont = ('Arial 10')
        self.tree = None
        self.curso = '10-2022'  # inicial
        self.horario = 'CURSO COMPLETO'  # inicial
        self.frame = frame_container
        self.column_header = column_header
        self.list = list

        self._setup_widgets()
        self._build_tree()
        self.setup_frame_estado()

        self.idRow = ''

    def _setup_widgets(self):

        container = self.frame
        container.config(background='#252525')

        # Style and theme
        style = ttk.Style()

        style.theme_use('clam')

        style.configure('Treeview',
                        background='#292d3e',
                        font=self.myFont,
                        foreground='white',
                        fieldbackground='#292d3e')

        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self.column_header,
                                 show="headings",
                                 style='Treeview')

        # si tenemos datos en columnas, mostrar las columnas q seran visibles
        self.tree.config(height=30, displaycolumns=self.column_header)
        self.tree.pack(expand=True, fill='both')

        # scroll bars
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)

        # hsb = ttk.Scrollbar(orient="horizontal",
        #                    command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set
                            # ,xscrollcommand=hsb.set
                            )

        # ubicacion del tree dentro del frame contenedor
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        self.tree.rowconfigure(0, weight=1)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        #hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.setupMenuContextual()

    def _build_tree(self):
        for col, i in zip(self.column_header, range(len(self.column_header))):

            # creando el head de cada columna, y el comando de ordenar
            self.tree.heading(col,
                              text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))

            # adjust the column's width to the header string
            self.tree.column(col,
                             width=tkFont.Font().measure(col.title()),
                             minwidth=50,
                             anchor=CENTER)

            # ancho de columnas condicionales (cambiar codigo por uno mas reutilizable)
            if i == 0:
                self.tree.column(col, width=220, anchor=W)
            if i == 1:
                self.tree.column(col, width=70)
            if i == 2:
                self.tree.column(col, width=120, anchor=W)
            if i == 3:
                self.tree.column(col, width=100)
            if i == 4:
                self.tree.column(col, width=100)
            if i == 5:
                self.tree.column(col, width=40)
            if i == 6:
                self.tree.column(col, width=150, anchor=W)

        # Para crear una cebra, actualmente se borra al escribir
        self.tree.tag_configure('dark',
                                background='#252525',
                                foreground='white')
        self.tree.tag_configure('light',
                                background='#393939',
                                foreground='white')

        cont = 0
        for item in self.list:
            color = 'dark' if cont % 2 == 0 else 'light'
            self.tree.insert('', 'end', values=item
                             # , tags=('fuente',color)
                             )

            # ajustar el nivel de cada columna segun sus valores
            """ for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                max_width = 300
                if self.tree.column(self.column_header[ix], width=None) < col_w:
                    self.tree.column(self.column_header[ix], width=col_w)
                if self.tree.column(self.column_header[ix], width=None) > max_width:
                    self.tree.column(self.column_header[ix], width=max_width) """
            cont += 1

        self.frame.pack(expand=True, fill=tk.BOTH)

        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_action)
        self.tree.bind('<ButtonRelease-3>', self.do_popup)


    def setup_frame_estado(self):
        self.frame_estado = Frame(self.frame, bg=COLOR_DARK_BG)
        self.frame_estado.grid(row=1,column=0, columnspan=2, sticky=EW)
        self.lb_estado = Label(self.frame_estado, text= '', bg=COLOR_DARK_BG, fg=COLOR_FB)
        self.lb_estado.pack(side=LEFT)
        self.lb_estado_2 = Label(self.frame_estado, text= '', bg=COLOR_DARK_BG, fg=COLOR_FB)
        self.lb_estado_2.pack(side=RIGHT, padx=20)
        
        self.actualizar_estado()



    # Evento creado para cuando se de doble click en un item
    def on_double_click(self, event):
        # try:
        id = self.tree.selection()[0]
        diccionario = self.tree.item(id)
        texto = diccionario['values'][2]
        print(texto)
        # except IndexError:
        #print('No se ha selecionado ninguna fila, dobleclick no abrira ninguna carpeta')

    def change(self, list):
        # borrar toda la lista para crear una nueva
        for child in self.tree.get_children():
            self.tree.delete(child)

        self.list = list

        cont = 0

        for item in list:
            self.tree.insert('', 'end', values=item)
            cont += 1
            
        self.actualizar_estado()
        
    def change_temp (self, list):
        # borrar toda la lista para crear una nueva
        for child in self.tree.get_children():
            self.tree.delete(child)

        cont = 0

        for item in list:
            self.tree.insert('', 'end', values=item)
            cont += 1
            
        self.actualizar_estado(list)

    def on_select_action(self, event):

        item_selected = self.tree.focus()
        if not item_selected:
            return

        idx = self.tree.index(item_selected)
        item = self.tree.item(item_selected)
        valoresItem = item['values']
        valoresIndex = self.list[idx]

        cursos = get_cursos_by_ci(valoresItem[1])
        if not cursos: return
        
        string_cursos = ", ".join(cursos) if len(cursos)>1 else cursos[0]
        nombre = valoresItem[0]
        self.lb_estado_2['text'] = f'{nombre} ({string_cursos})'
        
            

    # -------------- Menu Contextual ------------

    def editar(self):
        if self.idRow:
            self.tree.selection_set(self.idRow)
            idx = self.tree.index(self.idRow)
            valoresItem = self.list[idx]
            nombre = valoresItem[0]
            ci = valoresItem[1]
            municipio = valoresItem[2]
            tel = valoresItem[3]
            horario = valoresItem[4]
            cat = valoresItem[5]
            datos = valoresItem[6]

            # ejecutando un toplevel para editar
            x = 100
            y = 100

            top = Toplevel()
            w = 340
            h = 270
            top.geometry("%dx%d+%d+%d" % (w, h, x + 350, y + 150))

            top.title('Editando matricula')
            top.attributes('-topmost', 'true')

            municipios = get_municipios()
            horarios = get_horarios()
            cat_code = get_all_cat_code()

            # StringVars
            sv_name = StringVar()
            sv_ci = StringVar()
            sv_tel = StringVar()

            def check_required_fields():
                return e_name.get() and e_ci.get()

            def ci_duplicado_en_matricula():
                sc = self.curso.split('-')
                id_curso = get_idcurso_by_curso_year(sc[0], sc[1])

                ci_actual = ci
                ci_nuevo = sv_ci.get()
                if not ci_actual == ci_nuevo:
                    return get_matricula_by_ci_curso(ci_nuevo, id_curso)
                return False

            def aceptar():
                guardar.clear()
                guardar.append(e_name.get().strip())
                guardar.append(e_ci.get().strip())
                guardar.append(e_municipio.get().strip())
                guardar.append(e_tel.get().strip())
                guardar.append(e_horario.get().strip())
                guardar.append(e_datos.get().strip())
                guardar.append(e_categoria.get().strip())

                ci_data_dupl = ci_duplicado_en_matricula()

                if not check_required_fields():
                    messagebox.showerror(
                        'Faltan campos requerido',
                        'Compruebe que el campo "Nombre(s) y apellidos" y "Carnet de Identidad" esten correctamente llenados'
                    )
                if ci_data_dupl:
                    messagebox.showerror(
                        'Matricula duplicada',
                        f'Esta tratando de agregar una matricula cuyo Carnet de Identidad coicide con un alumno ya agregado previamente a este curso.\n\nAlumno: {ci_data_dupl[0]} en el horario de {ci_data_dupl[1]}'
                    )
                else:
                    # metodo externo no reutilizable
                    sc = self.curso.split('-')
                    id_curso = get_idcurso_by_curso_year(sc[0], sc[1])

                    horario = self.horario
                    horario_final = horario if not horario == 'CURSO COMPLETO' else None
    
                    actualizar_matricula(guardar, ci, id_curso)
                    # print(guardar)
                    top.destroy()
                    self.change(get_view_matriculas_by_idcurso(id_curso, horario_final))

            def cancelar():
                top.destroy()

            # BINDS METHODS
            # ---- BIND METHODS ----
            def bind_aceptar(evento):
                aceptar()
                pass

            def bind_cancelar(evento):
                cancelar()
                pass

            def event_change_name(e):
                capitalizado = capitalizar_palabras(sv_name.get())
                e_name.delete(0, 'end')
                e_name.insert(0, capitalizado)

            def capitalizar_palabras(frase: str):
                palabras: list[str] = frase.split(' ')
                mayus_palabras = [palabra.capitalize() for palabra in palabras]
                return ' '.join(mayus_palabras)

            def callback_ci_entry(*args):
                ci = sv_ci.get()
                if not ci == "" and not len(ci) == 11 or not ci.isdigit():
                    e_ci.config(foreground='red')
                else:
                    e_ci.config(foreground='black')

            def callback_tel(*args):
                tel = sv_tel.get()
                if tel and not tel[-1:].isdigit() and not tel[-1:] == ' ':
                    sv_tel.set(tel[:-1])
            sv_ci.trace('w', callback_ci_entry)
            sv_tel.trace('w', callback_tel)

            guardar = []
            # labels
            lb_name = Label(top, text='Nombre(s) y apellidos')
            lb_ci = Label(top, text='Carnet de Identidad')
            lb_tel = Label(top, text='Telefono')
            lb_municipio = Label(top, text='Municipio')
            lb_categoria = Label(top, text='Categoria')
            lb_horario = Label(top, text='Horario')
            lb_datos = Label(top, text='Otros datos')
            # labels grid
            lb_name.grid(row=1, column=0, sticky='w', pady=5, padx=10)
            lb_ci.grid(row=2, column=0, sticky='w', pady=5, padx=10)
            lb_tel.grid(row=3, column=0, sticky='w', pady=5, padx=10)
            lb_municipio.grid(row=4, column=0, sticky='w', pady=5, padx=10)
            lb_categoria.grid(row=5, column=0, sticky='w', pady=5, padx=10)
            lb_horario.grid(row=6, column=0, sticky='w', pady=5, padx=10)
            lb_datos.grid(row=7, column=0, sticky='wn', pady=5, padx=10)

            # entrys
            e_name = Entry(top, width=30, textvariable=sv_name)
            e_ci = Entry(top, width=30, textvariable=sv_ci)
            e_tel = Entry(top, width=30, textvariable=sv_tel)
            e_municipio = self.combobox(top, municipios, width=27)
            e_categoria = self.combobox(top, cat_code, width=27)
            e_horario = self.combobox(top, horarios, width=27)
            e_datos = Entry(top, width=30)

            # entrys grid
            e_name.grid(row=1, column=1, sticky='w', pady=5)
            e_ci.grid(row=2, column=1, sticky='w', pady=5)
            e_tel.grid(row=3, column=1, sticky='w', pady=5)
            e_municipio.grid(row=4, column=1, sticky='w', pady=5)
            e_categoria.grid(row=5, column=1, sticky='w', pady=5)
            e_horario.grid(row=6, column=1, sticky='w', pady=5)
            e_datos.grid(row=7, column=1, sticky='w', pady=5)

            # valores que carga por defecto
            e_name.insert(0, nombre)
            e_ci.insert(0, ci)
            munic_values = e_municipio['values']
            coinc = 0
            for i in range(len(munic_values)):
                if munic_values[i] == municipio:
                    coinc = i
                    break
            e_municipio.current(coinc)

            e_tel.insert(0, tel)

            hor_values = e_horario['values']
            coinc = 0
            for i in range(len(hor_values)):
                if hor_values[i] == horario:
                    coinc = i
                    break
            e_horario.current(coinc)

            cat_values = e_categoria['values']
            coinc = 0
            for i in range(len(cat_values)):
                if cat_values[i] == cat:
                    coinc = i
                    break
            e_categoria.current(coinc)

            e_datos.insert(0, datos)

            e_name.focus_set()

            frame_bts = Frame(top)
            frame_bts.grid(row=8, column=1, sticky='e')

            bt_aceptar = Button(frame_bts,
                                text='Actualizar',
                                command=aceptar,
                                bg=GREEN_BUTTON,
                                fg='white',
                                width=8)
            bt_aceptar.grid(row=0, column=0, padx=10, pady=10)
            bt_cancelar = Button(frame_bts,
                                 text='Cancelar',
                                 command=cancelar,
                                 bg=RED_BUTTON,
                                 fg='white',
                                 width=8)
            bt_cancelar.grid(row=0, column=1, padx=10, pady=10)

            e_name.bind('<FocusOut>', event_change_name)
            top.bind('<Return>', bind_aceptar)
            top.bind('<Escape>', bind_cancelar)

            top.mainloop()

    def eliminar(self):
        if messagebox.askokcancel(
                'Confirmar eliminacion',
                f'Confirme que desea eliminar la matricula seleccionada'):

            indexes = [self.tree.index(idx) for idx in self.tree.selection()]

            reductor = 0  # al ir reduciendo la lista, corre de lugar los index
            sc = self.curso.split('-')
            for index in indexes:
                idxFinal = index - reductor
                valoresItem = self.list[idxFinal]
                ci = valoresItem[1]
                curso_num = sc[0]
                year = sc[1]

                print('index:', index, 'id:', id)

                self.list.pop(idxFinal)
                reductor += 1

                eliminar_matr_by_ci_and_curso(ci, curso_num, year)

                self.change(self.list)

    def setupMenuContextual(self):

        self.mc = tk.Menu(self.frame, tearoff=0)
        self.mc.add_command(label='Editar datos...', command=self.editar)
        self.mc.add_separator()
        self.mc.add_command(label='Eliminar', command=self.eliminar)

    def do_popup(self, event):
        self.idRow = ''
        try:
            self.idRow = self.tree.identify_row(event.y)
            if self.idRow:
                self.tree.selection_set(self.idRow)

                idx = self.tree.index(self.idRow)

                valoresItem = self.list[idx]

                # self.actualizarFrameLateral(valoresItem)

                self.mc.post(event.x_root, event.y_root)

        finally:
            self.mc.grab_release()

    def getIdsSelected(self):
        indexes = [self.tree.index(idx) for idx in self.tree.selection()]
        ids = []
        for index in indexes:
            valoresItem = self.list[index]
            ids.append(valoresItem[0])
        return ids

    def combobox(self, top, valores, width=20, modo=True):
        estado = 'readonly' if modo else 'normal'
        box = ttk.Combobox(top, width=width, state=estado)
        box['values'] = valores
        box.current(0)  # Selecciona el primer elemento de la tupla.
        #box.bind("<<ComboboxSelected>>", combobox_elegir)
        return box

    def actualizar_estado(self, lista=None):
        cantidad_matriculas = len(self.list) if lista == None else len(lista)
        
        texto_matri = f'{cantidad_matriculas} matriculas' if int(cantidad_matriculas) > 1 else f'{cantidad_matriculas} matricula'
        
        if self.list:
            if self.list[0][0] == '': texto_matri=''
        
        self.lb_estado.config(text=texto_matri)
        
    
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    return
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(
        col, command=lambda col=col: sortby(tree, col, int(not descending)))


# the test data ...

carros_header = ['car', 'repair', '3']
lista_carros = [('Hyundai', 'brakes', '3'), ('Honda', 'light', '3'),
                ('Lexus', 'battery', '3'), ('Benz', 'wiper', '3'),
                ('Ford', 'tire', '3'), ('Chevy', 'air', '3'),
                ('Chrysler', 'piston', '3'), ('Toyota', 'brake pedal', '3'),
                ('BMW', 'seat', '3')]

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multicolumn Treeview/Listbox")
    frame1 = tk.Frame(root)
    listbox = MultiColumnListbox(frame1, carros_header, lista_carros)
    root.mainloop()
