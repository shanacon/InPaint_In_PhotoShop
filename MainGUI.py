from PhotoshopScript import *
from ModelAction import GenerateMask
from PIL import ImageTk, Image, ImageOps, ImageDraw, ImageChops
from tkinter.constants import *
from tkinter import Canvas
import os
import random
import shutil
import subprocess
openPS = False
lastx = None
lasty = None
class MainGUI:
    
    def __init__(self, window, BtnFont):
        ## Base
        self.originimg = None
        self.ImgName = None
        self.bg = None
        self.Editimg = None  ## PIL Image 
        self.img = None      ## Photo Image
        self.bgid = None
        self.canvas = None
        self.masklist = []    ## PIL Image List of Mask
        # self.RemoveMaskList = [] ## mask list after remove mask which in other mask
        self.maskimglist = [] ## for reference
        self.mask2id = {}
        self.window = window
        ## Mouse
        # self.select = None
        # self.selectpos = [None, None]
        # self.presspos = [None, None]
        ## Segment
        self.SegmentImage = []
        self.maskid2segid = {}
        ## Inpaint
        self.InpaintImgPath = None
        self.InpaintMaskPath = None
        ## EditMode
        self.EditMode = False
        self.BrushWhite = False
        self.PaintSize = 5

    def LoadImage(self, file_path, MaskPath, MaskImgPath, InpaintPath, imgname, Tabframe, OpenInPS):
        global openPS
        openPS = OpenInPS
        self.originimg = Image.open(file_path)
        self.ImgName = imgname
        self.bg = Image.open(f'{self.ImgName}_bg.png')
        self.img = ImageTk.PhotoImage(self.originimg)
        ## set canvas
        self.canvas = Canvas(Tabframe,  width= self.img.width(), height= self.img.height())
        self.bgid = self.canvas.create_image(0 , 0, anchor=NW, image=self.img, tags = 'bg_layer')
        self.canvas.place(x = 0, y = 0)
        ## Generate mask and set mask img
        if not os.path.exists(os.path.join(MaskPath, os.path.splitext(imgname)[0])):
            GenerateMask(file_path)
        self.InpaintImgPath = 'Inpaint_' + imgname
        self.InpaintImgPath = os.path.join(InpaintPath, self.InpaintImgPath)
        self.InpaintMaskPath = 'Inpaint_' + os.path.splitext(imgname)[0] + '_mask001' + os.path.splitext(imgname)[1]
        self.InpaintMaskPath = os.path.join(InpaintPath, self.InpaintMaskPath)
        os.makedirs(MaskImgPath, exist_ok=True)
        os.makedirs(InpaintPath, exist_ok=True)
        MaskPath = os.path.join('mask', os.path.splitext(imgname)[0])
        for BaseName in os.listdir(MaskPath):
            if os.path.splitext(BaseName)[1] == '.png' :
                FullPath = os.path.join(MaskPath, BaseName)
                self.masklist.append(Image.open(FullPath))
                self.GenerateMaskImage(FullPath, MaskImgPath)
                self.AddMaskImage(os.path.join(MaskImgPath, BaseName))
        # self.RemovedMaskList = self.RemoveMaskInMask()
        # for i, mask in  enumerate(self.masklist):
        #     BaseName = os.path.basename(mask.filename)
        #     self.AddMaskImage(os.path.join(MaskImgPath, BaseName), i)
                
        ## set Segment der 
        # self.SegImgPath = 'SegImg'
        # os.makedirs(self.SegImgPath, exist_ok=True)
        ##
        self.canvas.bind('<Motion>', self.mouse_motion_handler)
        # self.canvas.bind('<Button-1>', self.mouse_B1press_handler)
        # self.canvas.bind('<ButtonRelease-1>', self.mouse_B1release_handler)
        self.canvas.bind('<Double-Button-1>', self.Segment)
        ## photoshop_action
        if openPS :
            openimg(self.bg)
        tmp = self.masklist.copy()
        tmp.insert(0, self.bg)
        return tmp
    ### Mouse Action
    def mouse_motion_handler(self, event):
        mouse_x = event.x
        mouse_y = event.y
        if self.EditMode :
            pass
        else :
            for mask in self.masklist :
                id = self.mask2id[mask.filename]
                imgx, imgy = self.canvas.coords(id)
                if self.CheckMouseOut(imgx, imgy, event) :
                    continue
                mask_alpha = -1
                try :
                    mask_alpha = mask.getpixel((mouse_x - imgx, mouse_y - imgy))
                except:
                    pass
                if mask_alpha > 0:
                    self.ShowMaskImage(id)
                else :
                    self.HideMaskImage(id)
    def mouse_B1press_handler(self, event) :
        mouse_x = event.x
        mouse_y = event.y
        global lastx, lasty
        if self.EditMode:
            lastx, lasty = mouse_x, mouse_y
    def mouse_B1motoion_handler(self, event) :
        # if self.select == None:
        #     return
        global lastx, lasty
        mouse_x = event.x
        mouse_y = event.y
        if self.EditMode:
            if self.BrushWhite :
                self.canvas.create_line((lastx, lasty, mouse_x, mouse_y), fill='white', width = self.PaintSize, tags='line')
            else :
                if self.Editimg != self.bg :
                    self.canvas.create_line((lastx, lasty, mouse_x, mouse_y), fill='black', width = self.PaintSize, tags='line')
                else :
                    OverlapIDs = self.canvas.find_overlapping(lastx, lasty, mouse_x, mouse_y)
                    for id in OverlapIDs  :
                        if 'line' in self.canvas.gettags(id) :
                            self.canvas.delete(id)
            lastx, lasty = mouse_x, mouse_y
        # nowpos = [self.canvas.coords(self.select)[0], self.canvas.coords(self.select)[1]]
        # target = [mouse_x - self.presspos[0] + self.selectpos[0], mouse_y - self.presspos[1] + self.selectpos[1]]
        # if self.select != None :
        #     self.canvas.move(self.select, target[0] - nowpos[0], target[1] - nowpos[1])
        #     self.canvas.move(self.maskid2segid[self.select], target[0] - nowpos[0], target[1] - nowpos[1])
    # def mouse_B1release_handler(self, event):
    #     self.select = None
    #     self.selectpos = [None, None]
    #     self.presspos = [None, None]
    def CheckMouseOut(self, imgx, imgy, event):
        mouse_x = event.x
        mouse_y = event.y
        if mouse_x - imgx < 0 or mouse_x - imgx > self.img.width() or mouse_y - imgy < 0 or mouse_y - imgy > self.img.height():
            return True
        return False
    
    ### Mask Action
    def AddMaskImage(self, MaskImgPath):
        img = ImageTk.PhotoImage(Image.open(MaskImgPath))
        self.maskimglist.append(img)
        id = self.canvas.create_image(0 , 0, anchor=NW, image = img, tags='mask_layer')
        self.mask2id[self.masklist[-1].filename] = id
        self.HideMaskImage(id)

    def HideAllMaskImage(self):
        for mask in self.masklist :
                id = self.mask2id[mask.filename]
                self.HideMaskImage(id)
    def HideMaskImage(self, id):
        self.canvas.itemconfigure(id, state = 'hidden')
    def ShowMaskImage(self, id):
        self.canvas.itemconfigure(id, state = 'normal')
    def GenerateMaskImage(self, FullPath, SavePath):
        r = random.randint(40,200)
        g = random.randint(40,200)
        b = random.randint(40,200)
        img = Image.new('RGBA', (self.img.width(), self.img.height()), color = (150, r, g, b))
        mask_image = Image.open(FullPath)
        result_image = Image.new('RGBA', img.size)
        result_image.paste(img, mask=mask_image)
        result_image.save(os.path.join(SavePath, os.path.basename(FullPath)))

    ### Segment Action
    def Segment(self, event):
        mouse_x = event.x
        mouse_y = event.y
        if self.EditMode :
            pass
        else:
            for mask in self.masklist :
                id = self.mask2id[mask.filename]
                imgx, imgy = self.canvas.coords(id)
                if self.CheckMouseOut(imgx, imgy, event) :
                    continue
                mask_alpha = mask.getpixel((mouse_x - imgx, mouse_y - imgy))
                
                if mask_alpha > 0:
                    self.SegmentAndInpaint(mask)
                    break
    def SegmentAndInpaint(self, mask):
        self.DoSegment(mask)
        self.SetBackGround(mask)
        self.DoInpaint(mask)
        self.RemoveInpaintImg()
        if not self.EditMode :
            idx = self.masklist.index(mask)
            self.masklist.remove(mask)
            del self.maskimglist[idx]
        self.canvas.delete('line')
    def DoSegment(self, mask):         ## generate segment image
        SegmentImg = Image.new('RGBA', self.originimg.size)
        SegmentImg.paste(self.originimg, mask = mask)
        if openPS :
            addimg(SegmentImg, self.ImgName)
        # img = ImageTk.PhotoImage(SegmentImg)
        # self.SegmentImage.append(img)
        # id = self.canvas.create_image(0 , 0, anchor=NW, image = img, tags="img_layer")
        # self.canvas.tag_raise("mask_layer")
        # self.maskid2segid[self.mask2id[mask.filename]] = id
    def SetBackGround(self, mask):   ## generate image without segment image
        mask = ImageOps.invert(mask.convert('RGB'))
        result_image = Image.new('RGBA', self.bg.size)
        result_image.paste(self.bg, mask = mask.convert("RGBA"))
        self.bg = result_image
        self.img = ImageTk.PhotoImage(self.bg)
        self.canvas.itemconfig(self.bgid, image=self.img)
        result_image.save(self.InpaintImgPath)

    ### Inpaint Action
    def DoInpaint(self, mask):
        mask.save(self.InpaintMaskPath)
        # command = [
        #     'python',
        #     'lama/bin/predict.py',
        #     'refine=False',
        #     'model.path=%cd%/lama/big-lama',
        #     '%cd%/InpaintImg',
        #     '%cd%/outputs'
        # ]
        # process = subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # process.wait()
        os.system('python lama/bin/predict.py refine=False model.path=%cd%/lama/big-lama  indir=%cd%/InpaintImg outdir=%cd%/outputs')
        print('complete inpaint')
        shutil.copyfile(f'outputs/{os.path.basename(self.InpaintMaskPath)}', f'{self.ImgName}_bg.png')
        self.bg = Image.open(f'{self.ImgName}_bg.png')
        self.img = ImageTk.PhotoImage(self.bg)
        self.canvas.itemconfig(self.bgid, image=self.img)
        if openPS :
            replaceimg(self.bg, self.ImgName)
    ### remove img for inpaint
    def RemoveInpaintImg(self):
        os.remove(self.InpaintImgPath)
        os.remove(self.InpaintMaskPath)
    ###
    def ChangeEdit(self, FilePath):
        if FilePath == os.path.split(self.originimg.filename)[-1]:
            self.Editimg = Image.open(f'{self.ImgName}_bg.png')
            self.img = ImageTk.PhotoImage(self.Editimg)
            self.canvas.itemconfig(self.bgid, image=self.img)
        else :
            for mask in self.masklist :
                if FilePath == os.path.split(mask.filename)[-1]:
                    self.Editimg = mask
                    self.img = ImageTk.PhotoImage(self.Editimg)
                    break
            self.canvas.itemconfig(self.bgid, image=self.img)
        self.canvas.delete('line')
    ###
    def MergeEdit(self):
        EditBg = Image.new('RGBA', self.Editimg.size, color='black')
        if self.Editimg != self.bg :
            EditBg.paste(self.Editimg, self.Editimg)
        draw = ImageDraw.Draw(EditBg)
        for line_id in self.canvas.find_withtag('line'):
            line_coords = self.canvas.coords(line_id)
            width = self.canvas.itemconfig(line_id)['width'][-1]
            fill_color = self.canvas.itemcget(line_id, 'fill')
            draw.line(line_coords, fill_color, width = int(float(width)))
        return EditBg.convert('L')
    ###
    def GetEditPath(self, maskname):
        for mask in self.masklist :
            if maskname == os.path.split(mask.filename)[-1]:
                return mask.filename
            
    # def RemoveMaskInMask(self) :
    #     RemovedMaskList = []
    #     for i in range(0, len(self.masklist)):
    #         for j in range(0, len(self.masklist)) :
    #             if i != j :
    #                 mask_bin_1 = self.masklist[i].convert('1')
    #                 mask_bin_2 = self.masklist[j].convert('1')
    #                 intersection = ImageChops.logical_and(mask_bin_1, mask_bin_2)
    #                 if ImageChops.difference(intersection, mask_bin_1).getbbox() is None:
    #                     break ## i in j
    #             if j == len(self.masklist) - 1 : ## i is not in any mask
    #                 RemovedMaskList.append(self.masklist[i])
    #     return RemovedMaskList