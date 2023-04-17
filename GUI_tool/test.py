import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CorrelationCurveApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Correlation Curve")

        # Define X and Y data
        self.x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.y = np.array([2, 4, 5, 7, 9, 10, 12, 14, 15])

        self.button = tk.Button(self.root, text="Draw", command=self.draw_correlation_curve)
        self.button.pack()

        self.correlation_coefficient_label = tk.Label(self.root, text="")
        self.correlation_coefficient_label.pack()

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().pack()

    def draw_correlation_curve(self):
        self.plot.clear()
        corr_coef = np.corrcoef(self.x, self.y)[0][1]
        self.correlation_coefficient_label.config(text="Correlation Coefficient: {:.2f}".format(corr_coef))
        self.plot.scatter(self.x, self.y)
        self.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    app = CorrelationCurveApp(root)
    root.mainloop()


