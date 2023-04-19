import tkinter as tk
from tkinter import ttk

# 创建主窗口
root = tk.Tk()
root.title("My Notebook")

# 创建ttk.Notebook小部件
notebook = ttk.Notebook(root)

# 创建第一个选项卡
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Tab 1")

# 在第一个选项卡中添加一个标签
label1 = ttk.Label(tab1, text="This is tab 1!")
label1.pack(padx=10, pady=10)

# 创建第二个选项卡
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Tab 2")

# 在第二个选项卡中添加一个按钮
button1 = ttk.Button(tab2, text="Click me!")
button1.pack(padx=10, pady=10)

# 将ttk.Notebook小部件添加到主窗口中
notebook.pack(expand=True, fill="both")

# 运行主循环
root.mainloop()



