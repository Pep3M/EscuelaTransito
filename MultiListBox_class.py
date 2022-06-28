'''
Here the TreeView widget is configured as a multi-column listbox
with adjustable column width and column-header-click sorting.
'''
from tkinter import END, messagebox
import tkinter as tk
import tkinter.ttk as ttk


class MultiColumnListbox(object):
    """use a ttk.TreeView as a multicolumn ListBox"""


    def __init__(self, frame_container:tk.Frame, column_header, list: list):
        """
        Constructor de la clase MultiColumnListBox. Genera una lista con encabezados. Necesita un frame contenedor (tkinter), una lista de encabezado y una lista de tuplas, donde el largo de cada una es igual al largo de la lista de encabezado

        Args:
            frame_container (tk.Frame): Frame que contendra este objeto
            column_header (list): Una lista de cada encabezado
            list (list[tuple | list]): Una lista de tuplas. Cada tupla representa una fila
        """
        
        self.tree = None
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
                        background = '#393939',
                        foreground = 'white',
                        fieldbackground = '#393939'                        
                        )
        
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=self.column_header, show="headings", style='Treeview')
       
        #si tenemos datos en columnas, mostrar las columnas q seran visibles
        self.tree.config(height=30, displaycolumns=self.column_header)
        self.tree.pack(expand=True, fill='both')

        # scroll bars
        vsb = ttk.Scrollbar(orient="vertical",
                            command=self.tree.yview)
        
        #hsb = ttk.Scrollbar(orient="horizontal",
        #                    command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set
                            #,xscrollcommand=hsb.set
                            )

        # ubicacion del tree dentro del frame contenedor
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        self.tree.rowconfigure(0, weight=1)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        #hsb.grid(column=0, row=1, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col, i in zip(self.column_header, range(len(self.column_header))):

            # creando el head de cada columna, y el comando de ordenar
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))

            # adjust the column's width to the header string
            #self.tree.column(col, width=tkFont.Font().measure(col.title()), minwidth=100)

            # ancho de columnas condicionales (cambiar codigo por uno mas reutilizable)
            if i == 0:
                self.tree.column(col, width=220)
            if i == 1:
                self.tree.column(col, width=220)
            if i == 2:
                self.tree.column(col, width=220)
            if i == 3:
                self.tree.column(col, width=150)
            if i == 4:
                self.tree.column(col, width=80)
            if i == 5:
                self.tree.column(col, width=70)
            if i == 6:
                self.tree.column(col, width=60)
            if i == 7:
                self.tree.column(col, width=60)
            if i == 8:
                self.tree.column(col, width=60)

        # Para crear una cebra, actualmente se borra al escribir
        self.tree.tag_configure('dark', background='#252525', foreground='white')
        self.tree.tag_configure('light', background='#393939', foreground='white')

        cont = 0
        for item in self.list:
            color = 'dark' if cont % 2 == 0 else 'light'
            self.tree.insert('', 'end', values=item
                             #, tags=('fuente',color)
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
        #try:
        id = self.tree.selection()[0]
        diccionario = self.tree.item(id)
        texto = diccionario['values'][2]
        print(texto)
        #except IndexError:
            #print('No se ha selecionado ninguna fila, dobleclick no abrira ninguna carpeta')


    def change(self, list):
        #borrar toda la lista para crear una nueva
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        self.list = list
        
        cont = 0
        
        for item in list:
            self.tree.insert('', 'end', values=item)
            cont += 1


    def on_select_action(self,event):
    
        item_selected = self.tree.focus()
        if not item_selected: return

        idx = self.tree.index(item_selected)
        item = self.tree.item(item_selected)
        valoresItem = item['values']

        print('Se selecciono',valoresItem)
    

    # -------------- Menu Contextual ------------

    """ 
    def abrir(self):
        if self.idRow:
            self.tree.selection_set(self.idRow)
            idx = self.tree.index(self.idRow)
            valoresItem = self.list[idx]
            #print('id:',valoresItem[0])
            abrirCarpeta(valoresItem[9])
            
    def renombrar(self):
        if self.idRow:
            self.tree.selection_set(self.idRow)
            idx = self.tree.index(self.idRow)
            valoresItem = self.list[idx]
            id = valoresItem[0]
            titulo = valoresItem[1]
    
        
            top = tk.Toplevel()
            top.geometry('400x80')
            top.title('Renombrar pelicula')
            
            entry = tk.Entry(top)
            entry.pack(pady=10, padx=10, fill='x')
            entry.insert(0,titulo)
            entry.select_range(0, END)
            entry.focus()
            
            frameB = tk.Frame(top)
            frameB.pack()
            
            def aceptar():
                valoresItem[1] = entry.get()
                
                self.list.pop(idx)
                self.list.insert(idx,valoresItem)

                if not db.updateNameById(id=id, new_name=valoresItem[1]):
                    messagebox.showerror('Nombre repetido',f'Ya existe una pelicula guardada con ese nombre ({valoresItem[1]}). Escriba otro diferente. \n\nTambien considere que debe eliminar los duplicados.')
                    top.focus()
                    entry.focus()
                    return
                self.change(self.list)

                top.destroy()
                
            bAceptar = tk.Button(frameB, text='Aceptar', command=aceptar)
            bAceptar.pack(side='left', padx=10)
            
            bCancelar = tk.Button(frameB, text='Cancelar', command=top.destroy)
            bCancelar.pack(side='right')

        

        
        top.mainloop()
            
    def corregir_datos(self):
        if self.idRow:
            self.tree.selection_set(self.idRow)
            idx = self.tree.index(self.idRow)
            valoresItem = self.list[idx]
            id = valoresItem[0]
            titulo = valoresItem[1]
    
            pelisOpciones()
        
            

    def eliminar(self):
        if messagebox.askokcancel('Confirmar eliminacion',
        f'Seguro que desea eliminar la pelicula seleccionada?\n\n(Nota: NO se borrara del ordenador, solo del listado)'):

            indexes = [self.tree.index(idx) for idx in self.tree.selection()]
            
            reductor = 0 #al ir reduciendo la lista, corre de lugar los index
            for index in indexes:    
                idxFinal = index - reductor
                valoresItem = self.list[idxFinal]
                id = valoresItem[0]

                print('index:',index,'id:',id)
                
                self.list.pop(idxFinal)
                db.deleteByIdPeli(id)
                reductor += 1

                self.change(self.list)
    

    def setupMenuContextual(self):

        self.mc = tk.Menu(self.frame, tearoff=0)
        self.mc.add_command(label='Abrir',command=self.abrir)
        self.mc.add_separator()
        self.mc.add_command(label='Renombrar', command=self.renombrar)
        self.mc.add_command(label='Corregir datos...', command=self.corregir_datos)
        self.mc.add_separator()
        self.mc.add_command(label='Eliminar', command=self.eliminar)
     """
    def do_popup(self, event):
        self.idRow = ''
        try:
            self.idRow = self.tree.identify_row(event.y)
            if self.idRow:
                self.tree.selection_set(self.idRow)
                
                idx = self.tree.index(self.idRow)
                
                valoresItem = self.list[idx]

                self.actualizarFrameLateral(valoresItem)
                
                self.mc.post(event.x_root, event.y_root)

            
        finally:
            self.mc.grab_release()

    """ def actualizarFrameLateral(self, valoresItem:list):
    
        NombFila = valoresItem[1]
        NombAltFila = valoresItem[2]
        descrFila = valoresItem[4]
        castFila = valoresItem[10]
        
        rutaFila = valoresItem[9]
        imagen_file = funciones.scanImgsInDir(rutaFila)
        imagenYruta = '{}/{}'.format(rutaFila,imagen_file)
        FrameLateral.setImg(self.frameLateral,imagenYruta, imagen_file)
            
        FrameLateral.setNombre(self.frameLateral,texto=NombFila)
        FrameLateral.setNombreAlt(self.frameLateral,texto=NombAltFila)
        FrameLateral.setDescripcion(self.frameLateral,texto=descrFila)
        FrameLateral.setCast(self.frameLateral,texto=castFila) """   
    
    def getIdsSelected(self):
        indexes = [self.tree.index(idx) for idx in self.tree.selection()]
        ids = []
        for index in indexes:    
                valoresItem = self.list[index]
                ids.append(valoresItem[0])
        return ids


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort

    data = [(tree.set(child, col), child)
            for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(
        tree, col, int(not descending)))


# the test data ...

carros_header = ['car', 'repair', '3']
lista_carros = [
    ('Hyundai', 'brakes', '3'),
    ('Honda', 'light', '3'),
    ('Lexus', 'battery', '3'),
    ('Benz', 'wiper', '3'),
    ('Ford', 'tire', '3'),
    ('Chevy', 'air', '3'),
    ('Chrysler', 'piston', '3'),
    ('Toyota', 'brake pedal', '3'),
    ('BMW', 'seat', '3')
]


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multicolumn Treeview/Listbox")
    frame1 = tk.Frame(root)
    listbox = MultiColumnListbox(frame1, carros_header, lista_carros)
    root.mainloop()


