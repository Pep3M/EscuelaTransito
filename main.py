from tkinter import Button, Frame, Tk


root = Tk()
root.title('Transito matriculas')
root.minsize(width=600, height=350)

body_frame = Frame(root)
body_frame.pack(expand=True, fill='both')

buttons_frame = Frame(body_frame, width=150, background='green')
buttons_frame.pack(fill='y', side='left')

bt_new_matr = Button(buttons_frame, text='Nueva matricula')
bt_new_matr.pack()


tree_frame = Frame(body_frame, background='blue')
tree_frame.pack(expand=True, fill='both', side='right')

root.mainloop()