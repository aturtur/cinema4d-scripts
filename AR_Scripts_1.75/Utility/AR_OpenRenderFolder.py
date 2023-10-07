"""
AR_OpenRenderFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenRenderFolder
Version: 1.2.0
Description-US: Opens folder where project is rendered.

NOTE: Does not support all of the tokens!

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.2.0 (25.05.2023) - Support for Variable Tokens
1.1.0 (18.05.2022) - Some custom tokens added
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
def GetNextObject(op):
    if op == None: return None
    if op.GetDown(): return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

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

def GetVersion(filePath, delimiter):
    """ Get version number from a file path"""
    versionList = re.findall(delimiter+"\\d+",filePath) # Search delimiter+digits (e.g. _v001) string in file path and store those in a [list]
    if len(versionList) == 0: # If no versions found
        return None, None
    rawVersion = re.compile(delimiter).split(versionList[len(versionList)-1])[1] # Version number with zero padding [string]
    version = str(int(rawVersion)) # Version number without zero padding [integer]
    return version, rawVersion # (e.g. 1, 001)

def GetProjectVersion(name, delimiter):
    """ Project Version """
    ver, rawVer = GetVersion(name, delimiter)
    if ver == None:
        return ""
    else:
        return rawVer

def GetCleanProjectName(name, delimiter):
    """ Clean project name """
    name = name.rsplit(delimiter, 1)[0]
    if name == None:
        return ""
    else:
        return name

def SearchVT(token):
    """ Variable Token """
    tokenVariableObject = None
    op = doc.GetFirstObject() # Get the first object in the project
    if op is None: return
    while op:
        if op.GetType() == 1060651: # If Variable Tokens object
            if op[c4d.ID_BASEOBJECT_GENERATOR_FLAG] == True: # If object is enabled
                tokenVariableObject = op
                break
        op = GetNextObject(op) # Get next object
    if tokenVariableObject != None:
        return tokenVariableObject[token]
    else:
        return None

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
    d = "_v"

    # Native tokens
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

    # Custom tokens
    tokenAprj   = str(GetCleanProjectName(tokenPrj, d))
    tokenVer    = str(GetProjectVersion(tokenPrj, d))

    # Modify the path
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

    path = path.replace("$aprj", tokenAprj)     # Solve clean project name ($aprj) token (CUSTOM)
    path = path.replace("$ver", tokenVer)       # Solve project version ($ver) token (CUSTOM)

    try:
        path = path.replace("$t0", SearchVT(c4d.VT_TOKEN0)) # Solve variable tokens ($t0-9) (PLUG-IN)
        path = path.replace("$t1", SearchVT(c4d.VT_TOKEN1))
        path = path.replace("$t2", SearchVT(c4d.VT_TOKEN2))
        path = path.replace("$t3", SearchVT(c4d.VT_TOKEN3))
        path = path.replace("$t4", SearchVT(c4d.VT_TOKEN4))
        path = path.replace("$t5", SearchVT(c4d.VT_TOKEN5))
        path = path.replace("$t6", SearchVT(c4d.VT_TOKEN6))
        path = path.replace("$t7", SearchVT(c4d.VT_TOKEN7))
        path = path.replace("$t8", SearchVT(c4d.VT_TOKEN8))
        path = path.replace("$t9", SearchVT(c4d.VT_TOKEN9))
    except:
        pass

    return path

def main():
    doc = c4d.documents.GetActiveDocument()     # Get active document
    renderData = doc.GetActiveRenderData()      # Get document active render data
    renderPath  = renderData[c4d.RDATA_PATH]    # Get render path

    path = os.path.abspath(renderPath)          # Get absolute path
    path = os.path.dirname(path)                # Get folder path
    path = CheckTokens(path)                    # Convert tokens to absolute

    print(path)

    storage.ShowInFinder(path, True)            # Open the folder

# Execute main()
if __name__=='__main__':
    main()