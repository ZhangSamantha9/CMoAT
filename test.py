import tkinter as tk


class MyApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.var1 = tk.StringVar()
        self.label1 = tk.Label(self, text="Variable 1:")
        self.label1.pack(side="left")
        self.entry1 = tk.Entry(self, textvariable=self.var1)
        self.entry1.pack(side="left")

        self.var2 = tk.StringVar()
        self.label2 = tk.Label(self, text="Variable 2:")
        self.label2.pack(side="left")
        self.entry2 = tk.Entry(self, textvariable=self.var2)
        self.entry2.pack(side="left")

        self.button = tk.Button(self, text="OK", command=self.process_variables)
        self.button.pack(side="left")

    def process_variables(self):
        var1_value = self.var1.get()
        var2_value = self.var2.get()
        # 在这里对变量进行处理
        print("Variable 1:", var1_value)
        print("Variable 2:", var2_value)


root = tk.Tk()
app = MyApplication(master=root)
app.mainloop()
