from tkinter import *
from tkinter import ttk


root: Tk = Tk()
root.title("Hello world")

frm = ttk.Frame(root, padding=10)
frm.grid()
box = ttk.Frame(frm, padding=10)
box.grid()
ttk.Label(box, text="Hello World").grid(column=0, row=0)
ttk.Button(box, text="Quit", command=root.destroy).grid(column=1, row=0)

ttk.Label(frm, text="11111111111111111111111111111111111111111").grid(column=0, row=1)

root.mainloop()


