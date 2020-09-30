"""
AR_OpenRenderFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenRenderFolder
Version: 1.0
Description-US: Opens folder where project is rendered
NOTE: Does not support all of the tokens!

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d
import os
import subprocess
import re


# Functions
def CheckFolders(path):
    folders = path.split("..\\")
    if len(folders)>1:
        p = doc.GetDocumentPath()
        for x in range(0, len(folders)-1):
            p = os.path.dirname(p)
        path = p + "\\" + folders[-1]
    current = path.split(".\\")
    if len(current)>1:
        path = doc.GetDocumentPath() + "\\" + current[1]
    return path

def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    bd = doc.GetActiveBaseDraw() # Get active base draw
    renderData = doc.GetActiveRenderData() # Get document active render data
    
    renderPath  = renderData[c4d.RDATA_PATH]
    width       = renderData[c4d.RDATA_XRES_VIRTUAL]
    height      = renderData[c4d.RDATA_YRES_VIRTUAL]
    fps         = renderData[c4d.RDATA_FRAMERATE]

    take = doc.GetTakeData().GetCurrentTake().GetName()
    camera = bd.GetSceneCamera(doc).GetName()
        
    tokenPrj    = os.path.splitext(doc.GetDocumentName())[0]
    tokenPrj    = str(tokenPrj.replace(" ", "_"))
    tokenRes    = str(int(width))+"x"+str(int(height))
    tokenFps    = str(int(fps))
    tokenTake   = str(take.replace(" ", "_"))
    tokenCamera = str(camera.replace(" ", "_"))

    renderPath = renderPath.replace("/","\\")

    path = renderPath.replace("$prj", tokenPrj) # Solve project name ($prj) token
    path = path.replace("$res", tokenRes) # Solve esolution ($res) token
    path = path.replace("$fps", tokenFps) # Solve frame rate ($fps) token
    path = path.replace("$take", tokenTake) # Solve take ($take) token
    path = path.replace("$camera", tokenCamera) # Solve camera ($camera) token

    path = CheckFolders(path)    
    path = os.path.dirname(path)
    
    subprocess.Popen(r'explorer "'+path+'"') # Open project folder

# Execute main()
if __name__=='__main__':
    main()