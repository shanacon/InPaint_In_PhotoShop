import tkinter as tk
import tkinter.ttk as ttk

class FilePanel:

    def __init__(self, window, BtnFont):
        self.Menu = tk.Menu(window)
        window.config(menu = self.Menu)
        self.FileMenu = tk.Menu(self.Menu, tearoff=0)
        self.Menu.add_cascade(label='File',menu = self.FileMenu)
        # add menu items to the File menu
        self.FileMenu.add_command(label='Load Image')
        self.TabSystem = ttk.Notebook(window)
        self.TabList = []
        self.TabSystem.pack(expand=1, fill="both")
        self.NowTabs = 0
        self.PSBool = tk.BooleanVar()#布林值變數
        self.OpenPsCheckbox = tk.Checkbutton(window, text = 'Open in Photoshop', variable = self.PSBool)
        self.OpenPsCheckbox.pack()
    def NewTab(self, TabName):
        self.TabList.append(tk.Frame(self.TabSystem))
        self.TabSystem.add(self.TabList[-1], text = TabName)
        return self.TabList[-1]
