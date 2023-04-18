import tkinter as tk
from tkinter import ttk
import correlation_analysis_GUI
import os



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x650")
        self.title('Analysis')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)


        self.create_widgets()

        img = tk.PhotoImage()
        img = img.subsample(1, 1)
        self.image = ttk.Label(image=img)
        self.image.image = img
        self.image.grid(row=5)


    def create_widgets(self):

        correlation_label = ttk.Label(self, text="Gene correlation")
        correlation_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        text_box=ttk.Frame(self)
        text_box.grid()

        cancer_part=ttk.Frame(text_box)
        cancer_part.grid(row=1,columnspan=3)


        cancername_label = ttk.Label(cancer_part, text="Cancer name:")
        cancername_label.grid(column=0,row=1,sticky=tk.W, pady = 2)

        self.var1 = tk.StringVar()
        cancer_name_entry = ttk.Entry(cancer_part,textvariable=self.var1)
        cancer_name_entry.grid(column = 2, row=1,sticky=tk.E,pady = 2)

        gene1_part = ttk.Frame(text_box)
        gene1_part.grid()

        gene1_label = ttk.Label(gene1_part, text="Gene 1:")
        gene1_label.grid(column=0, row=2,sticky=tk.W, pady = 2)

        self.var2 = tk.StringVar()
        gene1_entry = ttk.Entry(gene1_part,textvariable=self.var2)
        gene1_entry.grid(column = 2, row =2, pady = 2)

        gene2_part = ttk.Frame(text_box)
        gene2_part.grid()
        gene2_label = ttk.Label(gene2_part, text="Gene 2:")
        gene2_label.grid(column=0, row=3,sticky=tk.W, pady = 2)

        self.var3 = tk.StringVar()
        gene2_entry = ttk.Entry(gene2_part,textvariable=self.var3)
        gene2_entry.grid(row =3, column = 1, pady = 2)

        # login button
        analysis_button = ttk.Button(text_box, text="Analysis", command=self.draw_correlation_curve)
        analysis_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()








