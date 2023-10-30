import tkinter as tk
from tkinter import ttk

from cmoa.libs import cptac_data as cd

class ProteinAnalysisGUI(tk.Tk):
    def __init__(self):
        # Enable high dpi support
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

        # init super
        super().__init__()

        self.title("Protein Analysis")
        self.geometry("650x700")
        self.resizable(0, 0)

        # Create notebook (tab menu)
        notebook: ttk.Notebook = ttk.Notebook(self)
        notebook.pack(expand=1, fill='both')

        # Create & init correlation&expression tab frame
        correlation_frm: ttk.Frame = ttk.Frame(notebook)
        self.init_correlation_tab(correlation_frm)
        expression_frm: ttk.Frame = ttk.Frame(notebook)
        self.init_expression_tab(expression_frm)

        # Add to Notebook (tab menu)
        notebook.add(correlation_frm, text='Correlation')
        notebook.add(expression_frm, text='Expression')

    def init_correlation_tab(self, tab: ttk.Frame):
        """
        Init correlation frame in the input param [tab]
        """
        input_frm = ttk.Frame(tab, padding=5)
        input_frm.pack(expand=1, fill='x', anchor='n')

        correlation_label = ttk.Label(input_frm, text="Gene correlation")
        correlation_label.pack()

        cancername_frm = ttk.Frame(input_frm)
        cancername_frm.pack(expand=1, fill='x')

        cancername_label = ttk.Label(cancername_frm, text="Cancer name:")
        cancername_label.pack(side='left', anchor='w')

        self.cancername_value = tk.StringVar()
        cancer_name_entry = ttk.Entry(
            cancername_frm, textvariable=self.cancername_value)
        cancer_name_entry.pack(side='right', anchor='e')

        gene1_frm: ttk.Frame = ttk.Frame(input_frm)
        gene1_frm.pack(expand=1, fill='x')

        gene1_label = ttk.Label(gene1_frm, text="Gene 1:")
        gene1_label.pack(side='left', anchor='w')

        self.gene1_value = tk.StringVar()
        gene1_entry = ttk.Entry(gene1_frm, textvariable=self.gene1_value)
        gene1_entry.pack(side='right', anchor='e')

        gene2_frm: ttk.Frame = ttk.Frame(input_frm)
        gene2_frm.pack(expand=1, fill='x')

        gene2_label = ttk.Label(gene2_frm, text="Gene 2:")
        gene2_label.pack(side='left', anchor='w')

        self.gene2_value = tk.StringVar()
        gene2_entry = ttk.Entry(gene2_frm, textvariable=self.gene2_value)
        gene2_entry.pack(side='right', anchor='e')

        # login button
        analysis_button = ttk.Button(
            input_frm, text="Analysis", command=self.draw_correlation_curve)
        analysis_button.pack(side='right', anchor='e')

        image_box = ttk.Frame(tab)
        image_box.pack()

        self.image = ttk.Label(image_box, image=tk.PhotoImage())
        self.image.pack()

    def init_expression_tab(self, tab):
        """
        Init expression frame in the input param [tab]
        """

        ttk.Label(tab, text="Expression").pack()

    def render_correlation_image(self, img: tk.PhotoImage):
        """
        Render image to correlation image label
        """
        self.image.configure(image=img)
        self.image.image = img

    # 绘制相关性曲线
    def draw_correlation_curve(self):
        cancer_name = self.cancername_value.get()
        gene1 = self.gene1_value.get()
        gene2 = self.gene2_value.get()

        cancer_data = cd.load_cancer(cancer_name)
        # TODO: Cptac 1.5.5 No task
        # if cancer_data:
        #     tumor_data = ca.dataset_preprocess(cancer_data)
        #     path = ca.draw_correlation_curve(gene1, gene2, tumor_data)

        #     if path:
        #         img = tk.PhotoImage(file=path)
        #         img = img.subsample(1, 1)
        #         self.render_correlation_image(img)

        # else:
        #     print(f'Load dataset {cancer_name} failed.')


if __name__ == '__main__':
    my_gui = ProteinAnalysisGUI()
    my_gui.mainloop()
