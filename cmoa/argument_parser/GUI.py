from cmoa.GUI_lib.GUI import ProteinAnalysisGUI
from cmoa.GUI_lib.GUI_init import GUI_init

def show_window():
    GUI_init()
    window = ProteinAnalysisGUI()
    window.mainloop()