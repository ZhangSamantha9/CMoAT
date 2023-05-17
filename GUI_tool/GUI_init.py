import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from app_init import packages_check

import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk

def GUI_init() -> None:
    """
    Init GUI, check packages and return if packages check success
    """

    uninstall_packages = packages_check.get_uninstalled_packages()

    if len(uninstall_packages) > 0:
        PackagesInstallGUI()

    print('Packages check success')

class PackagesInstallGUI(tk.Tk):
    def __init__(self) -> None:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)

        self.refresh_packages()

        super().__init__()

        self.title("APP Init")
        self.geometry("600x700")

        # store all install labels for refresh after install packages process
        self.install_labels: list[ttk.Label] = []

        packages_frm = ttk.Frame(self, padding=5)
        packages_frm.pack(fill=tk.BOTH, expand=True, anchor=tk.N)

        ttk.Label(packages_frm, text="Install dependence packages").pack()

        denpendence_packages_frm = ttk.Frame(packages_frm, padding=5)
        denpendence_packages_frm.pack(fill=tk.X, expand=True, anchor=tk.N, side=tk.TOP)
        ttk.Label(denpendence_packages_frm, text="Dependence packages:").pack(anchor='w')
        for package in self.dependence_packages:
            package_frm = ttk.Frame(denpendence_packages_frm)
            package_frm.pack(fill=tk.X, expand=True, anchor=tk.N, side=tk.TOP)

            ttk.Label(package_frm, text=package).pack(side=tk.LEFT)
            is_installed: bool = package not in self.uninstall_packages
            install_label = ttk.Label(package_frm, text="Installed" if is_installed else "Not installed")
            install_label.pack(side=tk.RIGHT)
            self.install_labels.append(install_label)

        # store btn for refresh after install packages process, after install all packages, change btn text to "Next" and close window
        self.btn = ttk.Button(packages_frm)
        self.btn.pack(side='right', anchor=tk.S)

        self.refresh_frame_content()
        self.mainloop()

    def refresh_frame_content(self) -> None:
        self.refresh_packages()

        for i, package in enumerate(self.dependence_packages):
            is_installed: bool = package not in self.uninstall_packages
            self.install_labels[i].config(text="Installed" if is_installed else "Not installed")

        if len(self.uninstall_packages) == 0:
            self.btn.config(text="Next", command=self.destroy)
        else:
            self.btn.config(text="Install All", command=self.install_packages)

    def refresh_packages(self) -> None:
        self.dependence_packages = packages_check.dependence_packages
        self.uninstall_packages = packages_check.get_uninstalled_packages()

    class InstallPackagesDialog(simpledialog.Dialog):
        def __init__(self, master, title: str, packages: list[str]):
            self.packages = packages
            super().__init__(master, title)

        def body(self, master):
            self.package_index = 0
            self.package_count = len(self.packages)
            self.prompt = ttk.Label(master, text='Wait for installing')
            self.prompt.pack(expand=True, anchor=tk.W, side=tk.TOP)
            self.prograssbar = ttk.Progressbar(master, orient=tk.HORIZONTAL
                                               , mode='determinate'
                                               , maximum=self.package_count
                                               , length=500)
            self.prograssbar.pack(fill=tk.BOTH, expand=True)

        def buttonbox(self):
            self.btn = ttk.Button(self, text='Start Install', command=self.install_all)
            self.btn.pack(anchor=tk.E)
        
        def go_next(self, package: str):
            self.prograssbar.step()
            self.package_index += 1
            if self.package_index >= len(self.packages):
                self.destroy()
            else: self.refresh()

        def install_all(self):
            self.refresh()
            self.btn.config(state=tk.DISABLED)
            packages_check.install_packages(self.packages, None, self.go_next)

        def refresh(self):
            self.prompt.config(text=f"Installing package [{self.packages[self.package_index]}] {self.package_index}/{self.package_count}...")
            self.update()

    def install_packages(self) -> None:
        dialog = PackagesInstallGUI.InstallPackagesDialog(self, 'Installing packages...', self.uninstall_packages)

        self.refresh_frame_content()

if __name__ == "__main__":
    GUI_init()