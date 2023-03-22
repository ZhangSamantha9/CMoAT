from tkinter import *
import tkinter.messagebox as messagebox
import correlation_analysis

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.title = Label(self, text='Gene correlation')
        self.title.pack()
        self.cancer_name = Label(self, text='Cancer name')
        self.cancer_name.pack()
        self.gene_1 = Label(self, text='Gene 1')
        self.gene_1.pack()
        self.gene_2 = Label(self, text='Gene 2')
        self.gene_2.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
    # def hello(self):
    #     name = self.nameInput.get() or 'world'
    #     messagebox.showinfo('Message', 'Hello, %s' % name)

app = Application()
# 设置窗口标题:
app.master.title('Gene correlation')
app.master.maxsize(600, 800)
# 主消息循环:
app.mainloop()
