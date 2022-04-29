"""
AR_OpenRenderFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenRenderFolder
Version: 1.0.2
Description-US: Opens folder where project is rendered.
NOTE: Does not support all of the tokens!

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.2 (26.04.2022) - Bug fix and cleaning the code
1.0.1 (11.01.2022) - MacOS support
"""
# Libraries
import c4d
import os
import re
import storage


# Functions
def CheckFolders(path):
    separator = GetFolderSeparator()
    folders = path.split(".."+separator)
    if len(folders)>1:
        p = doc.GetDocumentPath()
        for x in range(0, len(folders)-1):
            p = os.path.dirname(p)
        path = p + separator + folders[-1]
    current = path.split("."+separator)
    if len(current)>1:
        path = doc.GetDocumentPath() + separator + current[1]
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

    s = "_"

    tokenPrj    = os.path.splitext(doc.GetDocumentName())[0]
    tokenPrj    = str(tokenPrj.replace(" ", s))
    tokenRes    = str(int(width))+"x"+str(int(height))
    tokenFps    = str(int(fps))
    tokenTake   = str(take.replace(" ", s))
    tokenCamera = str(camera.replace(" ", s))

    renderPath = renderPath.replace("\\","/")

    path = renderPath.replace("$prj", tokenPrj) # Solve project name ($prj) token
    path = path.replace("$res", tokenRes) # Solve esolution ($res) token
    path = path.replace("$fps", tokenFps) # Solve frame rate ($fps) token
    path = path.replace("$take", tokenTake) # Solve take ($take) token
    path = path.replace("$camera", tokenCamera) # Solve camera ($camera) token

    path = os.path.dirname(path)
    storage.ShowInFinder(path, True) # Open the folder

# Execute main()
if __name__=='__main__':
    main()