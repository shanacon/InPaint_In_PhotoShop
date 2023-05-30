import photoshop.api as ps
from photoshop import Session
from PIL import Image
import os
import pathlib
def openimg(img):
    root = pathlib.Path(__file__).parent.resolve()
    img.save('tmp.png')
    filename = img.filename.split('_')[0]
    with Session(action='new_document', auto_close=True) as ps:
        desc = ps.ActionDescriptor
        desc.putPath(ps.app.charIDToTypeID("null"), os.path.join(root, 'tmp.png'))
        event_id = ps.app.charIDToTypeID("Plc ")  # `Plc` need one space in here.
        ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
        ps.app.activeDocument.crop([0, 0, img.width, img.height])
        bounds = ps.app.activeDocument.activeLayer.bounds
        ScaleX = img.width/(bounds[2] - bounds[0]) * 100
        ScaleY = img.height/(bounds[3] - bounds[1]) * 100
        ps.app.activeDocument.activeLayer.resize(ScaleX, ScaleY, 1)
        bounds = ps.app.activeDocument.activeLayer.bounds
        ps.app.activeDocument.activeLayer.translate(-bounds[0], -bounds[1])
        ps.active_document.artLayers[0].name = 'bg'
        os.remove("tmp.png")
        doc = ps.active_document
        options = ps.PhotoshopSaveOptions()
        doc.saveAs(f'{os.path.join(root, filename)}.psd', options, True)
    with Session(f'{os.path.join(root, filename)}.psd', action='open') as ps:
        pass
##
def addimg(img, imgname):
    root = pathlib.Path(__file__).parent.resolve()
    img.save('tmp.png')
    with Session() as ps:
        document = ps.app.documents.getByName(f'{imgname}.psd')
        ps.app.activeDocument = document
        desc = ps.ActionDescriptor
        desc.putPath(ps.app.charIDToTypeID("null"), os.path.join(root, 'tmp.png'))
        event_id = ps.app.charIDToTypeID("Plc ")  # `Plc` need one space in here.
        ps.app.executeAction(ps.app.charIDToTypeID("Plc "), desc)
        os.remove("tmp.png")
def replaceimg(img, imgname):
    root = pathlib.Path(__file__).parent.resolve()
    img.save('tmp.png')
    with Session() as ps:
        document = ps.app.documents.getByName(f'{imgname}.psd')
        ps.app.activeDocument = document
        ChangeActionLayer(name = 'bg')
        docRef = ps.app.activeDocument
        replace_contents = ps.app.stringIDToTypeID('placedLayerReplaceContents')
        desc = ps.ActionDescriptor
        idnull = ps.app.charIDToTypeID("null")
        desc.putPath(idnull, os.path.join(root, 'tmp.png'))
        ps.app.executeAction(replace_contents, desc)
        docRef.activeLayer.name = 'bg'
        os.remove("tmp.png")
def ChangeActionLayer(index = None, name = None):
    if index != None:
        with Session() as ps:
            art_layer = ps.active_document.artLayers.getByIndex(index)
            docRef = ps.app.activeDocument
            docRef.activeLayer = art_layer
    elif name != None:
        with Session() as ps:
            art_layer = ps.active_document.artLayers.getByName(name)
            docRef = ps.app.activeDocument
            docRef.activeLayer = art_layer
    else :
        print('Error: Index or Name must be input.')