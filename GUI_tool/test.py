import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('X-Y Plot')

        self.x_values = []
        self.y_values = []

        # 添加 X 值输入框
        x_label = tk.Label(master, text='X values:')
        x_label.grid(row=0, column=0)
        self.x_entry = tk.Entry(master)
        self.x_entry.grid(row=0, column=1)

        # 添加 Y 值输入框
        y_label = tk.Label(master, text='Y values:')
        y_label.grid(row=1, column=0)
        self.y_entry = tk.Entry(master)
        self.y_entry.grid(row=1, column=1)

        # 添加“添加数据”按钮
        add_button = tk.Button(master, text='Add data', command=self.add_data)
        add_button.grid(row=2, column=1)

        # 添加“绘图”按钮
        plot_button = tk.Button(master, text='Plot', command=self.plot)
        plot_button.grid(row=2, column=2)

        # 添加图形绘制区域
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot_area = self.fig.add_subplot(111)
        self.plot_area.set_xlabel('X values')
        self.plot_area.set_ylabel('Y values')

        self.canvas = FigureCanvasTkAgg(self.fig, master)
        self.canvas.get_tk_widget().grid(row=3, columnspan=3)

    def add_data(self):
        # 从输入框中获取 X 和 Y 值
        x_value = float(self.x_entry.get())
        y_value = float(self.y_entry.get())

        # 将 X 和 Y 值添加到列表中
        self.x_values.append(x_value)
        self.y_values.append(y_value)

        # 清空输入框
        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)

    def plot(self):
        # 绘制 X-Y 图形
        self.plot_area.plot(self.x_values, self.y_values)
        self.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
