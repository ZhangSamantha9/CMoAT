import tkinter as tk
from tkinter import filedialog


class MyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Gene Correlation Analysis")

        # 创建标签和输入框
        self.input_label = tk.Label(master, text="Select the input data file:")
        self.input_label.grid(row=0, column=0, sticky="E")

        self.input_entry = tk.Entry(master)
        self.input_entry.grid(row=0, column=1, pady=10)

        self.output_label = tk.Label(master, text="Select the output directory:")
        self.output_label.grid(row=1, column=0, sticky="E")

        self.output_entry = tk.Entry(master)
        self.output_entry.grid(row=1, column=1, pady=10)

        # 创建按钮
        self.input_button = tk.Button(master, text="Browse", command=self.select_input_file)
        self.input_button.grid(row=0, column=2)

        self.output_button = tk.Button(master, text="Browse", command=self.select_output_directory)
        self.output_button.grid(row=1, column=2)

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.grid(row=2, column=1, pady=20)

    def select_input_file(self):
        file_path = filedialog.askopenfilename()
        self.input_entry.insert(0, file_path)

    def select_output_directory(self):
        directory_path = filedialog.askdirectory()
        self.output_entry.insert(0, directory_path)

    def submit(self):
        # 在这里添加您的代码，以获取输入和输出路径并进行相应的操作
        pass


# 创建主窗口
root = tk.Tk()

# 运行GUI
my_gui = MyGUI(root)

# 运行主循环
root.mainloop()



