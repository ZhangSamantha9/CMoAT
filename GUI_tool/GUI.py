
import tkinter as tk
from doctest import master
from tkinter import ttk
import correlation_analysis_GUI
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x650")
        self.title('Analysis')
        # self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        # self.root = root

        self.create_widgets()

        img = tk.PhotoImage()
        # img = tk.PhotoImage(file="C:/Users/SUISUISHOU/Documents/Python/gene_correlation/GUI_tool/EGFR and MET correlation curve.png")
        img = img.subsample(1, 1)
        self.image = ttk.Label(image=img)
        self.image.image = img
        self.image.grid(row=5)
        # img1 = tk.PhotoImage(file="C:/Users/SUISUISHOU/Documents/Python/gene_correlation/GUI_tool/EGFR and MET correlation curve.png")


    def create_widgets(self):
        # username
        correlation_label = ttk.Label(self, text="Gene correlation")
        correlation_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        cancername_label = ttk.Label(self, text="Cancer name:")
        cancername_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.var1 = tk.StringVar()
        cancer_name_entry = ttk.Entry(self,textvariable=self.var1)
        cancer_name_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # password
        gene1_label = ttk.Label(self, text="Gene 1:")
        gene1_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.var2 = tk.StringVar()
        gene1_entry = ttk.Entry(self,textvariable=self.var2)
        gene1_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)

        gene2_label = ttk.Label(self, text="Gene 2:")
        gene2_label.grid(column=0, row=3, sticky=tk.W, padx=5, pady=5)

        self.var3 = tk.StringVar()
        gene2_entry = ttk.Entry(self,textvariable=self.var3)
        gene2_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)


        # login button
        analysis_button = ttk.Button(self, text="Analysis", command=self.draw_correlation_curve)
        analysis_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)



        # self.figure = self.draw_correlation_curve()
        #
        # self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        # self.canvas.get_tk_widget().pack()


        # R_label = ttk.Label(self, text='r')
        # R_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)
        # pvalue_label = ttk.Label(self, text='p')
        # pvalue_label.grid(column=0, row=7, sticky=tk.W, padx=5, pady=5)
    # 绘制相关性曲线
    def draw_correlation_curve(self):
        cancer_name=self.var1.get()
        gene1 = self.var2.get()
        gene2 = self.var3.get()

        tumor_data_gui = correlation_analysis_GUI.get_cancer_data(cancer_name)

        filename= correlation_analysis_GUI.gene_correlation_curve(gene1, gene2,tumor_data_gui)
        fullpath=os.path.join(os.getcwd(),filename)+'.png'
        img = tk.PhotoImage(file=fullpath)
        img = img.subsample(1, 1)
        self.image.configure(image=img)
        self.image.image = img
        # sns.set(style="darkgrid")
        # gene_corrlation_plot = sns.regplot(x=gene1_data, y=gene2_data)
        # gene_corrlation_plot.set(xlabel=str(self.var2), ylabel=str(self.var3))
        # return  gene_corrlation_plot


# if __name__ == '__main__':
#     root = tk.Tk()
#     # app=App()
#     root.mainloop()
if __name__ == "__main__":
    app = App()
    app.mainloop()








