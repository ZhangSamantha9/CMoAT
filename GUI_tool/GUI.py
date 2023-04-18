import tkinter as tk
from tkinter import ttk
import correlation_analysis_GUI
import os
from PIL import ImageTk, Image



class protein_analysis_GUI:
    def __init__(self,master):
        master.title("Protein Analysis")

        master.geometry("650x700")
        master.resizable(0, 0)


        text_box=ttk.Frame(master)
        text_box.grid(sticky="W")

        correlation_label = ttk.Label(text_box, text="Gene correlation")
        correlation_label.grid(row=0, column=0, sticky="W")


        cancername_label = ttk.Label(text_box, text="Cancer name:")
        cancername_label.grid(row=1, column=0, sticky="W")

        self.var1 = tk.StringVar()
        cancer_name_entry = ttk.Entry(text_box,textvariable=self.var1)
        cancer_name_entry.grid(row=1, column=1, pady=10)

        gene1_label = ttk.Label(text_box, text="Gene 1:")
        gene1_label.grid(row=2, column=0, sticky="W")

        self.var2 = tk.StringVar()
        gene1_entry = ttk.Entry(text_box,textvariable=self.var2)
        gene1_entry.grid(row=2, column=1, pady=10)


        gene2_label = ttk.Label(text_box, text="Gene 2:")
        gene2_label.grid(row=3, column=0, sticky="W")

        self.var3 = tk.StringVar()
        gene2_entry = ttk.Entry(text_box,textvariable=self.var3)
        gene2_entry.grid(row =3, column = 1, pady = 2)

        # login button
        analysis_button = ttk.Button(text_box, text="Analysis", command=self.draw_correlation_curve)
        analysis_button.grid(row=4,column=0,columnspan=3,sticky="E")


        image_box=ttk.Frame()
        image_box.grid(sticky="W")
        img = tk.PhotoImage()
        img = img.subsample(1,1)
        self.image = ttk.Label(image_box,image=img)
        self.image.image = img
        self.image.grid(row=5, rowspan=2, column=1, padx=20,columnspan=3)

    # 绘制相关性曲线
    def draw_correlation_curve(self):
        cancer_name=self.var1.get()
        gene1 = self.var2.get()
        gene2 = self.var3.get()

        tumor_data_gui = correlation_analysis_GUI.get_cancer_data(cancer_name)

        filename= correlation_analysis_GUI.gene_correlation_curve(gene1, gene2,tumor_data_gui)
        fullpath=os.path.join(os.getcwd(),filename)+'.png'



        img = tk.PhotoImage(file=fullpath)
        img = img.subsample(1,1)
        self.image.configure(image=img)
        self.image.image = img


# 创建主窗口
root = tk.Tk()

# 运行GUI
my_gui =protein_analysis_GUI(root)

# 运行主循环
root.mainloop()








