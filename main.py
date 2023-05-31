import tkinter as tk
from tkinter import font, filedialog, Canvas
from MainGUI import *
from SideGUI import *
from FilePanel import *
from PIL import ImageTk, Image
import shutil
import os
def OnClose():
    for img in MainGUIList:
        img.bg.close()
    for bg in BGList:
         os.remove(bg)
    window.destroy()

MASK_PATH = 'mask'
MASK_IMG_PATH = 'MaskImg'
INPAINT_PATH = 'InpaintImg'
IMG_NAME = None
FIRST = True
window = tk.Tk()
window.protocol("WM_DELETE_WINDOW", OnClose)
BtnFont = font.Font(size=20)

FilePanel = FilePanel(window, BtnFont)
FilePanel.FileMenu.entryconfig('Load Image', command = lambda:LoadImage())
FilePanel.TabSystem.bind('<<NotebookTabChanged>>', lambda event: OnTabSelect(event))
MainGUIList = []
EditList = []
BGList = []
SideGUI = SideGUI(window, BtnFont)
def LoadImage() :
    global IMG_NAME
    global FIRST
    ## load img
    file_path = filedialog.askopenfilename(filetypes=(('Image Files', "*.png *.jpg *.jpeg"),))
    IMG_NAME = os.path.basename(file_path)
    NewTab = FilePanel.NewTab(IMG_NAME)
    try:
        shutil.copyfile(file_path, f'{IMG_NAME}_bg.png')
    except shutil.SameFileError:
        pass
    BGList.append(f'{IMG_NAME}_bg.png')
    NewGUI = MainGUI(window, BtnFont)
    EditList.append(NewGUI.LoadImage(file_path, MASK_PATH, MASK_IMG_PATH, INPAINT_PATH, IMG_NAME, NewTab, FilePanel.PSBool.get()))
    FilePanel.OpenPsCheckbox.place_forget()
    NewGUI.canvas.bind('<B1-Motion>', NewGUI.mouse_B1motoion_handler)
    NewGUI.canvas.bind('<Button-1>', lambda event, maingui = NewGUI : ChangeEditByCtrl(event, maingui))
    MainGUIList.append(NewGUI)
    SideGUI.LoadImage(EditList[-1], IMG_NAME)
    if FIRST:
        SideGUI.CBoxVar.trace('w', CBoxEvent)
        SideGUI.ToBgBtn.config(command = lambda:ToBgEvent())
        SideGUI.MaskBlackBtn.config(command = lambda:MaskBrushEvent(False))
        SideGUI.MaskWhiteBtn.config(command = lambda:MaskBrushEvent(True))
        SideGUI.BrushBig.config(command = lambda:BrushSizeEvent(True))
        SideGUI.BrushSmall.config(command = lambda:BrushSizeEvent(False))
        SideGUI.SIBtn.config(command = lambda:SegmentAndInpaintImg())
        SideGUI.SaveMaskBtn.config(command = lambda:SaveMaskImg(False))
        SideGUI.SaveOtherBtn.config(command = lambda:SaveMaskImg(True))
        SideGUI.SaveImgBtn.config(command = lambda:SaveImg())
        SideGUI.EditBool.trace('w', EditModeCBox)
        FIRST = False
    FilePanel.TabSystem.select(len(MainGUIList) - 1)
def CBoxEvent(*args):
    MainGUIList[FilePanel.NowTabs].ChangeEdit(SideGUI.CBoxVar.get())
    MainGUIList[FilePanel.NowTabs].HideAllMaskImage()
    X = SideGUI.EditList[0].width + 200
    if SideGUI.ImgCBox.current() != 0 :
        SideGUI.EditBool.set(True)
        SideGUI.EditMaskCheckbox['state'] = 'disabled'
        SideGUI.SaveMaskBtn.place(x = X - 195, y = 300)
        SideGUI.SaveImgBtn.place_forget()
    else:
        SideGUI.EditMaskCheckbox['state'] = 'normal'
        SideGUI.SaveMaskBtn.place_forget()
        SideGUI.SaveImgBtn.place(x = X - 195, y = 360)
def ToBgEvent():
    SideGUI.CBoxVar.set(IMG_NAME)
def MaskBrushEvent(white):
    MainGUIList[FilePanel.NowTabs].BrushWhite = white
def BrushSizeEvent(Big):
    if Big :
        MainGUIList[FilePanel.NowTabs].PaintSize = MainGUIList[FilePanel.NowTabs].PaintSize + 1
    else :
        MainGUIList[FilePanel.NowTabs].PaintSize = max(MainGUIList[FilePanel.NowTabs].PaintSize - 1, 0)
def SegmentAndInpaintImg():
    merged_image = MainGUIList[FilePanel.NowTabs].MergeEdit()
    MainGUIList[FilePanel.NowTabs].SegmentAndInpaint(merged_image)
    ToBgEvent()
def SaveMaskImg(new):
    merged_image = MainGUIList[FilePanel.NowTabs].MergeEdit()
    if new:
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes = (('PNG files','*.png'),('all files','*.*')))
        merged_image.save(file_path)
    else:
        path = MainGUIList[FilePanel.NowTabs].GetEditPath(SideGUI.CBoxVar.get())
        merged_image.save(path)
def SaveImg():
    file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes = (('PNG files','*.png'),('all files','*.*')))
    MainGUIList[FilePanel.NowTabs].bg.save(file_path)
def OnTabSelect(event):
    global IMG_NAME
    selected_tab = event.widget.select()
    tab_index = event.widget.index(selected_tab)
    FilePanel.NowTabs = tab_index
    IMG_NAME =os.path.basename(MainGUIList[tab_index].originimg.filename) 
    window.geometry(f'{MainGUIList[tab_index].img.width() + 200}x{MainGUIList[tab_index].img.height()}')
    SideGUI.LoadImage(EditList[tab_index], IMG_NAME)
    MainGUIList[FilePanel.NowTabs].EditMode = SideGUI.EditBool.get()
def EditModeCBox(*args):
    MainGUIList[FilePanel.NowTabs].EditMode = SideGUI.EditBool.get()
def ChangeEditByCtrl(event, maingui):
    mouse_x = event.x
    mouse_y = event.y
    if maingui.EditMode:
        MainGUIList[FilePanel.NowTabs].mouse_B1press_handler(event)
    else :
        for mask in  maingui.masklist :
            id = maingui.mask2id[mask.filename]
            imgx, imgy = maingui.canvas.coords(id)
            if maingui.CheckMouseOut(imgx, imgy, event) :
                continue
            mask_alpha = mask.getpixel((mouse_x - imgx, mouse_y - imgy))
            if mask_alpha > 0 and event.state & 0x4:
                SideGUI.CBoxVar.set(os.path.basename(mask.filename))
window.title('InPaint In PhotoShop')
window.resizable(False, False)
window.geometry('320x150')
window.mainloop()