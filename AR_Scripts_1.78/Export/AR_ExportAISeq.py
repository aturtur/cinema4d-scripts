"""
AR_ExportAISeq

Author: Arttu Rautio (aturtur) 
Website: http://aturtur.com/
Name-US: AR_ExportAISeq
Version: 1.1.0 / extend
Description-US: DEFAULT: Exports selected spline objects to Adobe Illustrator-sequence. Preview range will determine which frames will be exported. SHIFT: Export objects to separated folders. 

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (28.04.2021) - Support for R23
Update Aleksandrovsky: extend render region Aleksandrovsky
"""

# Libraries
import c4d, os, json
from c4d import plugins
from math import sqrt

# Functions
def GetFolderSeparator():
    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN:
        return "\\"
    else:
        return "/"

def GetKeyMod():
    bc = c4d.BaseContainer()
    keyMod = "None"
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
                    keyMod = 'Alt+Ctrl+Shift'
                else:
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
                keyMod = 'Alt+Shift'
            else:
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
                keyMod = 'Alt+Ctrl'
            else:
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
            keyMod = 'Alt'
        else:
            keyMod = 'None'
        return keyMod

def SetExporter(doc):
    plug = plugins.FindPlugin(1012074, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return
    data = {}
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
        if "imexporter" not in data:
            return
        aiExport = data["imexporter"]
        if aiExport is None:
            return
        aiExport[c4d.TUAIEXPORT_OUTPUTSIZE] = 0
        aiExport[c4d.TUAIEXPORT_ZSORT] = 0
        aiExport[c4d.TUAIEXPORT_SCALE] = 1
        aiExport[c4d.TUAIEXPORT_EXPORTLINES] = 1
        aiExport[c4d.TUAIEXPORT_LINEOPACITY] = 0
        aiExport[c4d.TUAIEXPORT_LINETHICKNESS] = 0
        aiExport[c4d.TUAIEXPORT_LINEPATTERNS] = 0
        aiExport[c4d.TUAIEXPORT_LINECONNECTIONS] = 1
        aiExport[c4d.TUAIEXPORT_EXPORTSURFACE] = 0
        aiExport[c4d.TUAIEXPORT_ANIMATION] = 1
        aiExport[c4d.TUAIEXPORT_ANIMTYPE] = 0
        aiExport[c4d.TUAIEXPORT_FRAMES] = 2
        aiExport[c4d.TUAIEXPORT_FRAME_START] = doc.GetLoopMinTime()
        aiExport[c4d.TUAIEXPORT_FRAME_END] = doc.GetLoopMaxTime()
        aiExport[c4d.TUAIEXPORT_FRAME_RATE] = doc.GetFps()

def SetRender(doc):
    renderData = doc.GetActiveRenderData()
    currVideoPost = renderData.GetFirstVideoPost()
    sntFound = False
    sketchEffect = None
    while currVideoPost is not None:
        if currVideoPost.GetType() == 1011015:
            sntFound = True
        currVideoPost = currVideoPost.GetNext()
    if not sntFound:
        sketchEffect = c4d.documents.BaseVideoPost(1011015)
        renderData.InsertVideoPostLast(sketchEffect)
    return sntFound, sketchEffect

def SaveJSONforAE(fn, ow, oh, osensor, nw, nh, d0, d1, ext_h, doc):
    jd = {
        'original_width': int(ow),
        'original_height': int(oh),
        'original_sensor': osensor,
        'extend_width': int(nw),
        'extend_height': int(nh),
        'extend_sensor': round(osensor*(d1/d0), 3),
        'user_extend': int(ext_h),
        'project_fps': doc.GetFps()
    }
    with open(os.path.splitext(fn)[0]+'_info.json', 'w', encoding='utf-8') as f:
        json.dump(jd, f, ensure_ascii=False)

class ExtendDialog(c4d.gui.GeDialog):
    def __init__(self):
        self.result = None

    ID_TEXT = 1000
    ID_INPUT = 1001
    ID_OK = 1002
    ID_CANCEL = 1003

    def CreateLayout(self):
        self.SetTitle("Extend Render Area")

        self.GroupBegin(3000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, cols=1, rows=2)
        self.GroupBorderSpace(10, 10, 10, 10)

        self.AddMultiLineEditText(self.ID_TEXT, c4d.BFH_SCALEFIT, 0, 80)
        self.SetString(self.ID_TEXT,
            "Enter number of pixels to extend render area:\n"
            "\n"
            "•  0px = No extension\n"
            "\n"
            "⚠️ Animating the camera's Sensor Size is not supported.\n"
            "Script overrides this value and resets it after exporting.")

        self.AddEditNumberArrows(self.ID_INPUT, c4d.BFH_SCALEFIT)
        self.SetInt32(self.ID_INPUT, 0)

        self.GroupEnd()

        self.GroupBegin(3001, c4d.BFH_CENTER, cols=2)
        self.GroupBorderSpace(0, 10, 0, 0)

        self.AddButton(self.ID_OK, c4d.BFH_LEFT, name="OK")
        self.AddButton(self.ID_CANCEL, c4d.BFH_LEFT, name="Cancel")

        self.GroupEnd()

        return True

    def Command(self, id, msg):
        if id == self.ID_OK:
            self.result = self.GetInt32(self.ID_INPUT)
            self.Close()
        elif id == self.ID_CANCEL:
            self.result = None
            self.Close()
        return True

def main():
    keyMod = GetKeyMod()
    extend_mode = 0
    doc = c4d.documents.GetActiveDocument()
    sketchTags = []

    dlg = ExtendDialog()
    dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, defaultw=400, defaulth=200)

    if dlg.result is None:
        return  # Cancel or Esc was pressed

    ext_h = dlg.result
    extend_mode = 1 if ext_h > 0 else 0

    if keyMod == "None":
        fn = c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "Select Save Path")
        if not fn: return

        sketchMat = c4d.BaseMaterial(1011014)
        doc.InsertMaterial(sketchMat)
        sntFound, sketchEffect = SetRender(doc)
        SetExporter(doc)
        
        if extend_mode == 1:
            rd = doc.GetActiveRenderData()
            ow = rd[c4d.RDATA_XRES]; oh = rd[c4d.RDATA_YRES]; ol = rd[c4d.RDATA_LOCKRATIO]
            cam = doc.GetActiveObject()
            if not cam or cam.GetType() != c4d.Ocamera:
                for o in doc.GetObjects():
                    if o.GetType() == c4d.Ocamera: cam = o; break
            osensor = cam[c4d.CAMERAOBJECT_APERTURE] or 36.0 if cam else None
            if ext_h == 0:
                rd[c4d.RDATA_XRES] = ow + 1; rd[c4d.RDATA_YRES] = oh + 1
            else:
                nh = oh + ext_h; nw = int(round(nh * ow / oh))
                rd[c4d.RDATA_XRES] = nw; rd[c4d.RDATA_YRES] = nh; rd[c4d.RDATA_LOCKRATIO] = True
                if cam and osensor:
                    d0 = sqrt(ow * ow + oh * oh); d1 = sqrt(nw * nw + nh * nh)
                    cam[c4d.CAMERAOBJECT_APERTURE] = osensor * (d1 / d0)
                SaveJSONforAE(fn, ow, oh, osensor, nw, nh, d0, d1, ext_h, doc)

        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
        for i in range(0, len(selection)):
            sketchTags.append(c4d.BaseTag(1011012))
            sketchTags[i][c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat
            sketchTags[i][c4d.OUTLINEMAT_LINE_SPLINES] = 1
            sketchTags[i][c4d.OUTLINEMAT_LINE_FOLD] = 0
            sketchTags[i][c4d.OUTLINEMAT_LINE_CREASE] = 0
            sketchTags[i][c4d.OUTLINEMAT_LINE_BORDER] = 0
            selection[i].InsertTag(sketchTags[i])

        name = os.path.splitext(fn)[0] + ".ai"
        c4d.documents.SaveDocument(doc, name, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1012074)

    elif keyMod == "Shift":
        fn = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select Save Path", flags=c4d.FILESELECT_DIRECTORY)
        if not fn: return

        sketchMat = c4d.BaseMaterial(1011014)
        doc.InsertMaterial(sketchMat)
        sketchTags = []
        sntFound, sketchEffect = SetRender(doc)
        SetExporter(doc)

        separator = GetFolderSeparator()
        selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
        for i in range(0, len(selection)):
            sketchTag = c4d.BaseTag(1011012)
            sketchTag[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat
            sketchTag[c4d.OUTLINEMAT_LINE_SPLINES] = 1
            sketchTag[c4d.OUTLINEMAT_LINE_FOLD] = 0
            sketchTag[c4d.OUTLINEMAT_LINE_CREASE] = 0
            sketchTag[c4d.OUTLINEMAT_LINE_BORDER] = 0
            selection[i].InsertTag(sketchTag)

            folderPath = os.path.splitext(fn)[0]
            objectName = selection[i].GetName()
            os.mkdir(folderPath + separator + objectName)
            fullFilePath = folderPath + separator + objectName + separator + objectName + ".ai"
            c4d.documents.SaveDocument(doc, fullFilePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1012074)
            sketchTag.Remove()

    for st in sketchTags:
        st.Remove()
    sketchMat.Remove()
    if not sntFound:
        sketchEffect.Remove()

    if extend_mode == 1: 
        rd[c4d.RDATA_XRES] = ow
        rd[c4d.RDATA_YRES] = oh
        rd[c4d.RDATA_LOCKRATIO] = ol
        if cam and osensor: 
            cam[c4d.CAMERAOBJECT_APERTURE] = osensor

    c4d.StatusClear()
    c4d.StatusSetText("Export complete!")
    c4d.EventAdd()

if __name__ == '__main__':
    main()
