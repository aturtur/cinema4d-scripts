"""
AR_OpenRenderFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenRenderFolder
Version: 1.0.3
Description-US: Opens folder where project is rendered.

NOTE: Does not support all of the tokens!

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.3 (02.05.2022) - Bug fixes and support for some tokens added
1.0.2 (26.04.2022) - Bug fix and cleaning the code
1.0.1 (11.01.2022) - MacOS support
"""

# Libraries
import c4d
import os
import re
from c4d import storage
from datetime import datetime

# Functions
def GetFullYear():
    now = datetime.now()
    return now.strftime("%Y")

def GetYear():
    now = datetime.now()
    return now.strftime("%y")

def GetMonth():
    now = datetime.now()
    return now.strftime("%m")

def GetComputerName():
    return os.environ['COMPUTERNAME']

def GetUserName():
    return os.environ['USERNAME']

def GetRendererName():
    renderData = doc.GetActiveRenderData() # Get document active render data
    rendererId = renderData[c4d.RDATA_RENDERENGINE]
    if rendererId != 0:
        return c4d.plugins.FindPlugin(rendererId, 0).GetName().split(' ', 1)[0]
    else:
        return "Standard"

def CheckTokens(path):
    """ Convert tokens in the path to absolute format """

    doc = c4d.documents.GetActiveDocument() # Get active document
    bd = doc.GetActiveBaseDraw() # Get active base draw
    renderData = doc.GetActiveRenderData() # Get document active render data

    width       = renderData[c4d.RDATA_XRES_VIRTUAL] # Render resolution width
    height      = renderData[c4d.RDATA_YRES_VIRTUAL] # Render resolution height
    fps         = renderData[c4d.RDATA_FRAMERATE]    # Render fps

    take = doc.GetTakeData().GetCurrentTake().GetName() # Render take name
    camera = bd.GetSceneCamera(doc).GetName()           # Render camera name

    s = "_"

    tokenPrj    = os.path.splitext(doc.GetDocumentName())[0]
    tokenPrj    = str(tokenPrj.replace(" ", s))
    tokenRes    = str(int(width))+"x"+str(int(height))
    tokenFps    = str(int(fps))
    tokenTake   = str(take.replace(" ", s))
    tokenCamera = str(camera.replace(" ", s))
    tokenYear2  = str(GetYear())
    tokenYear4  = str(GetFullYear())
    tokenMonth  = str(GetMonth())
    tokenRE     = str(GetRendererName())
    tokenRS     = str(renderData.GetName().replace(" ", s))
    tokenHeight = str(int(height))
    tokenPC     = str(GetComputerName().replace(" ", s))
    tokenUser   = str(GetUserName().replace(" ", s))

    tokenAuthor = str(doc[c4d.DOCUMENT_INFO_AUTHOR])
    if tokenAuthor != "":
        tokenAuthor = tokenAuthor.replace(" ", s)

    path = path.replace("$prj", tokenPrj)       # Solve project name ($prj) token
    path = path.replace("$res", tokenRes)       # Solve esolution ($res) token
    path = path.replace("$fps", tokenFps)       # Solve frame rate ($fps) token
    path = path.replace("$take", tokenTake)     # Solve take ($take) token
    path = path.replace("$camera", tokenCamera) # Solve camera ($camera) token
    path = path.replace("$YYYY", tokenYear4)    # Solve year(4) ($YYYY) token
    path = path.replace("$YY", tokenYear2)      # Solve year(2) ($YY) token
    path = path.replace("$MM", tokenMonth)      # Solve month ($MM) token
    path = path.replace("$renderer", tokenRE)   # Solve render engine ($renderer) token
    path = path.replace("$height", tokenHeight) # Solve height ($height) token
    path = path.replace("$username", tokenUser) # Solve user name ($username) token
    path = path.replace("$computer", tokenPC)   # Solve computer name ($computer) token
    path = path.replace("$rs", tokenRS)         # Solve render settings ($rs) token
    path = path.replace("$author", tokenAuthor) # Solve project author ($author) token

    return path

def main():
    doc = c4d.documents.GetActiveDocument()     # Get active document
    renderData = doc.GetActiveRenderData()      # Get document active render data
    renderPath  = renderData[c4d.RDATA_PATH]    # Get render path

    path = os.path.abspath(renderPath)          # Get absolute path
    path = os.path.dirname(path)                # Get folder path
    path = CheckTokens(path)                    # Convert tokens to absolute

    storage.ShowInFinder(path, True)            # Open the folder

# Execute main()
if __name__=='__main__':
    main()