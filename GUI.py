
import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x500")
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

        img = tk.PhotoImage(file="C:\\Users\\126614\\Downloads\\documents.png")
        img = img.subsample(1, 1)
        image = ttk.Label(image=img)
        image.image = img
        image.grid()


if __name__ == "__main__":
    app = App()
    app.mainloop()
