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

Update: extend render region (ChatGPT+Aleksandrovsky)

"""
# Libraries
import c4d, os, json
from math import sqrt
from c4d import plugins

# Functions
def GetFolderSeparator():
    return "\\" if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN else "/"

def GetKeyMod():
    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.BFM_INPUT_CHANNEL, bc):
        q = bc[c4d.BFM_INPUT_QUALIFIER]
        if q & c4d.QSHIFT: return 'Shift'
        if q & c4d.QCTRL:  return 'Ctrl'
        if q & c4d.QALT:   return 'Alt'
    return 'None'

def SetExporter(doc):
    plug = plugins.FindPlugin(1012074, c4d.PLUGINTYPE_SCENESAVER)
    if not plug: return
    data = {}
    if not plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data): return
    aiExport = data.get('imexporter')
    if not aiExport: return
    aiExport[c4d.TUAIEXPORT_OUTPUTSIZE]      = 0
    aiExport[c4d.TUAIEXPORT_ZSORT]           = 0
    aiExport[c4d.TUAIEXPORT_SCALE]           = 1
    aiExport[c4d.TUAIEXPORT_EXPORTLINES]     = 1
    aiExport[c4d.TUAIEXPORT_LINEOPACITY]     = 0
    aiExport[c4d.TUAIEXPORT_LINETHICKNESS]   = 0
    aiExport[c4d.TUAIEXPORT_LINEPATTERNS]    = 0
    aiExport[c4d.TUAIEXPORT_LINECONNECTIONS] = 1
    aiExport[c4d.TUAIEXPORT_EXPORTSURFACE]   = 0
    aiExport[c4d.TUAIEXPORT_ANIMATION]       = 1
    aiExport[c4d.TUAIEXPORT_ANIMTYPE]        = 0
    aiExport[c4d.TUAIEXPORT_FRAMES]          = 2
    aiExport[c4d.TUAIEXPORT_FRAME_START]     = doc.GetLoopMinTime()
    aiExport[c4d.TUAIEXPORT_FRAME_END]       = doc.GetLoopMaxTime()
    aiExport[c4d.TUAIEXPORT_FRAME_RATE]      = doc.GetFps()

def SetRender(doc):
    rd = doc.GetActiveRenderData()
    vp = rd.GetFirstVideoPost()
    found=False
    while vp:
        if vp.GetType()==1011015: found=True
        vp=vp.GetNext()
    effect = None
    if not found:
        effect=c4d.documents.BaseVideoPost(1011015)
        rd.InsertVideoPostLast(effect)
    return found, effect

def main():
    doc = c4d.documents.GetActiveDocument()
    rd  = doc.GetActiveRenderData()
    key = GetKeyMod()

    # Save Original Settings
    ow = rd[c4d.RDATA_XRES]; oh = rd[c4d.RDATA_YRES]; ol = rd[c4d.RDATA_LOCKRATIO]
    cam = doc.GetActiveObject()
    if not cam or cam.GetType()!=c4d.Ocamera:
        for o in doc.GetObjects():
            if o.GetType()==c4d.Ocamera: cam=o; break
    osensor = cam[c4d.CAMERAOBJECT_APERTURE] or 36.0 if cam else None

    # Dialogs
    if key=='Shift':
        fn=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select Folder',flags=c4d.FILESELECT_DIRECTORY)
        if not fn: return
        ext_h= None
    else:
        fn=c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING,'Select Save Path')
        if not fn: return
        try:
            ext_h=int(c4d.gui.InputDialog('Extend (pixels):','40'))
        except:
            c4d.gui.MessageDialog('Invalid value.'); return

    mat = c4d.BaseMaterial(1011014); doc.InsertMaterial(mat)
    tags=[]
    snt, eff=SetRender(doc); SetExporter(doc)

    try:
        # Change Resolution and Sensor Size in Camera
        if ext_h is not None:
            if ext_h==0:
                rd[c4d.RDATA_XRES]=ow+1; rd[c4d.RDATA_YRES]=oh+1
            else:
                nh=oh+ext_h; nw=int(round(nh*ow/oh))
                rd[c4d.RDATA_XRES]=nw; rd[c4d.RDATA_YRES]=nh; rd[c4d.RDATA_LOCKRATIO]=True
                if cam and osensor:
                    d0=sqrt(ow*ow+oh*oh); d1=sqrt(nw*nw+nh*nh)
                    cam[c4d.CAMERAOBJECT_APERTURE]=osensor*(d1/d0)
                # Save JSON
                jd={
                    'original_width': int(ow),
                    'original_height': int(oh),
                    'original_sensor': osensor,
                    'extend_width': int(nw),  # ensure int
                    'extend_height': int(nh),  # ensure int
                    'extend_sensor': round(osensor*(d1/d0),3),
                    'user_extend': int(ext_h),
                    'project_fps': doc.GetFps()  
                }
                with open(os.path.splitext(fn)[0]+'_info.json','w',encoding='utf-8') as f: json.dump(jd,f,ensure_ascii=False)


        sel=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
        sep=GetFolderSeparator()
        if key=='Shift':
            base=fn
            for o in sel:
                t=c4d.BaseTag(1011012); o.InsertTag(t)
                t[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V]=mat; t[c4d.OUTLINEMAT_LINE_SPLINES]=1
                tags.append(t)
                p=os.path.join(base,o.GetName()); os.makedirs(p,exist_ok=True)
                c4d.documents.SaveDocument(doc,os.path.join(p,o.GetName()+'.ai'),c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,1012074)
        else:
            for o in sel:
                t=c4d.BaseTag(1011012); o.InsertTag(t)
                t[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V]=mat; t[c4d.OUTLINEMAT_LINE_SPLINES]=1
                tags.append(t)
            c4d.documents.SaveDocument(doc,os.path.splitext(fn)[0]+'.ai',c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,1012074)

    finally:
        for t in tags: t.Remove()
        rd[c4d.RDATA_XRES]=ow; rd[c4d.RDATA_YRES]=oh; rd[c4d.RDATA_LOCKRATIO]=ol
        if cam and osensor: cam[c4d.CAMERAOBJECT_APERTURE]=osensor
        mat.Remove()
        if not snt and eff: eff.Remove()
        c4d.StatusClear(); c4d.StatusSetText('Export complete!'); c4d.EventAdd()

if __name__=='__main__': main()
