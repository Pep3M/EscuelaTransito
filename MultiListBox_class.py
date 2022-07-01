'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
from tkinter import CENTER, END, W, Button, Text, Entry, Frame, Label, Toplevel, messagebox
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont


from db_handler import actualizar_matricula, eliminar_matr_by_ci_and_curso, get_all_cat_code, get_cursos, get_horarios, get_idcurso_by_curso_year, get_last_curso_id, get_municipios, get_view_matriculas_by_idcurso


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

        self.tree = None
        self.curso = '10-2022'  # inicial
        self.frame = frame_container
        self.column_header = column_header
        self.list = list

        self._setup_widgets()
        self._build_tree()

        self.idRow = ''

    def _setup_widgets(self):

        container = self.frame
        container.config(background='#252525')

        # Style and theme
        style = ttk.Style()

        style.theme_use('clam')

        style.configure('Treeview',
                        background='#292d3e',
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
                             minwidth=100, anchor=CENTER)

            # ancho de columnas condicionales (cambiar codigo por uno mas reutilizable)
            if i == 0:
                self.tree.column(col, width=220, anchor=W)
            if i == 1:
                self.tree.column(col, width=100)
            if i == 2:
                self.tree.column(col, width=150, anchor=W)
            if i == 3:
                self.tree.column(col, width=50)
            if i == 4:
                self.tree.column(col, width=80)
            if i == 5:
                self.tree.column(col, width=50)
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

    def on_select_action(self, event):

        item_selected = self.tree.focus()
        if not item_selected:
            return

        idx = self.tree.index(item_selected)
        item = self.tree.item(item_selected)
        valoresItem = item['values']

        print('Se selecciono', valoresItem)

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
            h = 325
            top.geometry("%dx%d+%d+%d" % (w, h, x + 350, y + 150))

            top.title('Editando matricula')
            top.attributes('-topmost', 'true')

            municipios = get_municipios()
            horarios = get_horarios()
            cat_code = get_all_cat_code()

            def check_required_fields():
                return e_name.get() and e_ci.get()

            def aceptar():
                guardar.clear()
                guardar.append(e_name.get())
                guardar.append(e_ci.get())
                guardar.append(e_municipio.get())
                guardar.append(e_tel.get())
                guardar.append(e_horario.get())
                guardar.append(e_datos.get('1.0', END))
                guardar.append(e_categoria.get())

                if not check_required_fields():
                    messagebox.showerror(
                        'Faltan campos requerido', 'Compruebe que el campo "Nombre(s) y apellidos" y "Carnet de Identidad" esten correctamente llenados')
                else:
                    # metodo externo no reutilizable
                    sc = self.curso.split('-')
                    id_curso = get_idcurso_by_curso_year(sc[0], sc[1])

                    actualizar_matricula(guardar, ci, id_curso)
                    # print(guardar)
                    top.destroy()
                    self.change(get_view_matriculas_by_idcurso(id_curso))

            def cancelar():
                top.destroy()

            guardar = []
            # labels
            lb_name = Label(top, text='Nombre(s) y apellidos')
            lb_ci = Label(top, text='Carnet de Identidad')
            lb_municipio = Label(top, text='Municipio')
            lb_tel = Label(top, text='Telefono')
            lb_horario = Label(top, text='Horario')
            lb_categoria = Label(top, text='Categoria')
            lb_datos = Label(top, text='Otros datos')
            # labels grid
            lb_name.grid(row=1, column=0, sticky='w', pady=5, padx=10)
            lb_ci.grid(row=2, column=0, sticky='w', pady=5, padx=10)
            lb_municipio.grid(row=3, column=0, sticky='w', pady=5, padx=10)
            lb_tel.grid(row=4, column=0, sticky='w', pady=5, padx=10)
            lb_horario.grid(row=5, column=0, sticky='w', pady=5, padx=10)
            lb_categoria.grid(row=6, column=0, sticky='w', pady=5, padx=10)
            lb_datos.grid(row=7, column=0, sticky='wn', pady=5, padx=10)

            # entrys
            e_name = Entry(top, width=30)
            e_ci = Entry(top, width=30)
            e_municipio = self.combobox(top, municipios, width=27)
            e_tel = Entry(top, width=10)
            e_horario = self.combobox(top, horarios, width=27)
            e_categoria = self.combobox(top, cat_code, width=27)
            e_datos = Text(top, width=22, height=4)
            # entrys grid
            e_name.grid(row=1, column=1, sticky='w', pady=5)
            e_ci.grid(row=2, column=1, sticky='w', pady=5)
            e_municipio.grid(row=3, column=1, sticky='w', pady=5)
            e_tel.grid(row=4, column=1, sticky='w', pady=5)
            e_horario.grid(row=5, column=1, sticky='w', pady=5)
            e_categoria.grid(row=6, column=1, sticky='w', pady=5)
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

            e_datos.insert('1.0', datos)

            e_name.focus_set()

            frame_bts = Frame(top)
            frame_bts.grid(row=8, column=1, sticky='e')

            bt_aceptar = Button(frame_bts, text='Actualizar', command=aceptar)
            bt_aceptar.grid(row=0, column=0, padx=10, pady=10)
            bt_cancelar = Button(frame_bts, text='Cancelar', command=cancelar)
            bt_cancelar.grid(row=0, column=1, padx=10, pady=10)

            top.mainloop()

    def eliminar(self):
        if messagebox.askokcancel('Confirmar eliminacion',
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
        box = ttk.Combobox(top, width=width,
                           state=estado)
        box['values'] = valores
        box.current(0)  # Selecciona el primer elemento de la tupla.
        #box.bind("<<ComboboxSelected>>", combobox_elegir)
        return box


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
