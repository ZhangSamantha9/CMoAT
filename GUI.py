# from tkinter import *
# import tkinter.messagebox as messagebox
# import correlation_analysis
#
# class Application(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.grid()
#         self.createWidgets()
#     def createWidgets(self):
#
#         self.title = Label(self, text='Gene correlation')
#         self.title.grid(row=1, column=0)
#
#         self.cancer_name = Label(self, text='Cancer name',anchor="w", width=20)
#         self.cancer_name.grid(row=0, column=1, sticky="ew")
#         self.cancer_entry = Entry()
#         self.cancer_entry.grid(row=1, column=1)
#         self.gene_1 = Label(self, text='Gene 1',anchor="w", width=20)
#         self.gene_1.grid(row=0, column=3, sticky="ew")
#         self.gene1_entry = Entry()
#         self.gene1_entry.grid(row=1, column=3)
#         self.gene_2 = Label(self, text='Gene 2',anchor="w", width=20)
#         self.gene_2.grid()
#         self.gene2_entry = Entry()
#         self.gene2_entry.grid(row=1, column=4)
#         self.quitButton = Button(self, text='Quit', command=self.quit)
#         self.quitButton.grid()
#
#     # def hello(self):
#     #     name = self.nameInput.get() or 'world'
#     #     messagebox.showinfo('Message', 'Hello, %s' % name)
#
# app = Application()
# # 设置窗口标题:
# app.master.title('Gene correlation')
# app.master.maxsize(600, 800)
# # 主消息循环:
# app.mainloop()

import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x700")
        self.title('Analysis')
        # self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

    def create_widgets(self):
        # username
        correlation_label = ttk.Label(self, text="Gene correlation")
        correlation_label.grid(row=0,sticky='nsew', padx=5, pady=5)

        cancername_label = ttk.Label(self, text="cancer name:")
        cancername_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        cancer_name_entry = ttk.Entry(self)
        cancer_name_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # password
        gene1_label = ttk.Label(self, text="Gene 1:")
        gene1_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        gene1_entry = ttk.Entry(self,  show="*")
        gene1_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        gene2_label = ttk.Label(self, text="Gene 2:")
        gene2_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        gene2_entry = ttk.Entry(self,  show="*")
        gene2_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)


        # login button
        analysis_button = ttk.Button(self, text="Analysis")
        analysis_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)


if __name__ == "__main__":
    app = App()
    app.mainloop()
