import tkinter as tk
import tkinter.ttk as ttk
import os

class SideGUI:
    def __init__(self, window, BtnFont):
        self.window = window
        self.BtnFont = BtnFont
        self.EditList = [] ## mask add bg
        self.GoLastBtn = tk.Button(window, text ='<', bg = 'light yellow', width = '3', height = '1', font = BtnFont)
        self.GoNextBtn = tk.Button(window, text ='>', bg = 'light yellow', width = '3', height = '1', font = BtnFont)
        self.GoLastBtn.config(command = lambda:self.GoBtnEvent(False))
        self.GoNextBtn.config(command = lambda:self.GoBtnEvent(True))
        self.CBoxVar = tk.StringVar()
        self.ImgCBox = ttk.Combobox(window, width = '9', textvariable = self.CBoxVar)

        self.ToBgBtn = tk.Button(window, text ='Back to image', bg = 'light yellow', width = '15', height = '1',)
        self.MaskWhiteBtn = tk.Button(window, text ='Mask White', bg = 'light yellow', width = '10', height = '1')
        self.MaskBlackBtn = tk.Button(window, text ='Mask Black', bg = 'light yellow', width = '10', height = '1')
        self.BrushBig = tk.Button(window, text ='+', bg = 'light yellow', width = '3', height = '1', font = BtnFont)
        self.BrushSmall = tk.Button(window, text ='-', bg = 'light yellow', width = '3', height = '1', font = BtnFont)

        self.SIBtn = tk.Button(window, text ='Segment and inpaint with this mask', bg = 'light yellow', height = '1') ## segment and inpaint
        self.SaveMaskBtn = tk.Button(window, text ='Save Mask', bg = 'light yellow', height = '1')
        self.SaveOtherBtn = tk.Button(window, text ='Save Mask as new file', bg = 'light yellow', height = '1')
        self.SaveImgBtn = tk.Button(window, text ='Save Image', bg = 'light yellow', height = '1')

        self.EditBool = tk.BooleanVar()#布林值變數
        self.EditMaskCheckbox = tk.Checkbutton(window, text = 'Mask Brush', variable = self.EditBool)
    def LoadImage(self, EditList, imgname):
        X = EditList[0].width + 200
        self.EditList = EditList
        EditStrList = []
        for img in EditList :
            EditStrList.append(os.path.basename(img.filename))
        EditStrList[0] = imgname
        self.ImgCBox['values'] = EditStrList
        self.ImgCBox.current(0)
        
        ###
        self.GoLastBtn.place(x = X - 197, y = 20)
        self.GoNextBtn.place(x = X - 55, y = 20)
        self.ImgCBox.place(x = X - 143, y = 20)
        self.ToBgBtn.place(x = X - 197, y = 75)
        self.EditMaskCheckbox.place(x = X - 195, y = 150)
        self.MaskWhiteBtn.place(x = X - 195, y = 190)
        self.MaskBlackBtn.place(x = X - 100, y = 190)
        self.BrushBig.place(x = X - 197, y = 220)
        self.BrushSmall.place(x = X - 55, y = 220)
        self.SIBtn.place(x = X - 195, y = 270)
        self.SaveOtherBtn.place(x = X - 195, y = 330)
    def GoBtnEvent(self, next):
        selection = self.ImgCBox.current()
        last = len(self.ImgCBox['values']) - 1
        if next:
            try:
                self.ImgCBox.current(selection + 1)  # set the combobox to the previous item
            except tk.TclError:  # end of list reached
                self.ImgCBox.current(0)  # wrap around to last item
        else:
            try:
                self.ImgCBox.current(selection - 1)  # set the combobox to the previous item
            except tk.TclError:  # end of list reached
                self.ImgCBox.current(last)  # wrap around to last item
        