
import tkinter as tk
from tkinter import ttk
import correlation_analysis_GUI
from PIL import Image, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x500")
        self.title('Analysis')
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

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
        analysis_button = ttk.Button(self, text="Analysis",command=self.gene_correlation_curve_gui)
        analysis_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

        # self.pil_image = Image.open(self.gene_correlation_curve_gui.correlation_plot_result)
        # self.tk_image = ImageTk.PhotoImage(self.pil_image)
        # self.label = tk.Label(self.window, image=self.tk_image)
        # self.label.grid()

        # img = tk.PhotoImage(file=".\\gene_corelation\\GUI_tool\\gene_correlation.png")
        #
        # img = tk.PhotoImage()
        # img = img.subsample(1, 1)
        # image = ttk.Label(image=img)
        # image.image = img


    # 绘制相关性曲线
    def gene_correlation_curve_gui(self):
        cancer_name=self.var1.get()
        gene1 = self.var2.get()
        gene2 = self.var3.get()
        tumor_data_gui = correlation_analysis_GUI.get_cancer_data(cancer_name)
        correlation_analysis_GUI.gene_correlation_curve(gene1, gene2,tumor_data_gui)




if __name__ == "__main__":
    app = App()
    app.mainloop()







