"""
AR_Folder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Folder
Version: 1.8.4
Description-US: Creates a folder null that keeps your project nice and tidy

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.8.4 (14.03.2023) - Fixed GetVersion bug
1.8.3 (18.02.2023) - Fixed adopt layer bug
1.8.2 (17.11.2022) - Fixed bug when user cancels picking a custom color
1.8.1 (16.09.2022) - Added support for Cinema 4D 2023
1.8.0 (04.04.2022) - 'Adopt layer' and 'open' options added
1.7.0 (02.04.2022) - Added icons! Color update. World Zero option added
1.6.0 (29.03.2022) - Instead of carrying txt-file for options along with the script, it will create options file to C4D's preference folder
1.5.1 (09.10.2021) - Updated for R25
1.5.0 (07.09.2021) - Added color option 'None' (No color, just default settings)
1.4.0 (15.03.2021) - Added and autolayer python tag and some kind of support for R20
1.3.0 (14.03.2021) - Cinema 4D R23 support for separator python tag
1.2.0 (12.03.2021) - Big update, a lot of changes and new features
1.1.0 (07.11.2020) - Added support for Esc and Enter keys

Color names from here:
    https://chir.ag/projects/name-that-color/
    https://www.color-name.com/
"""

# Libraries
import c4d
import os
import sys
import random
from c4d import gui
from c4d.gui import GeDialog
from c4d import storage
from c4d import bitmaps as bm

# Global variables
hierarchy   = {} # Initialize hierarchy dictionary
level       = 0  # Initialize level variable (how deep object is in hierarchy)
customColor = c4d.Vector(0,0,0) # Init custom color

"""
name icon-020    id 1059287
name icon-019    id 1059286
name icon-018    id 1059285
name icon-017    id 1059284
name icon-016    id 1059283
name icon-015    id 1059282
name icon-014    id 1059281
name icon-013    id 1059280
name icon-012    id 1059279
name icon-011    id 1059278
name icon-010    id 1059277
name icon-009    id 1059276
name icon-008    id 1059275
name icon-007    id 1059274
name icon-006    id 1059273
name icon-005    id 1059272
name icon-004    id 1059271
name icon-003    id 1059270
name icon-002    id 1059269
name icon-001    id 1059268

name color-020   id 1059267
name color-019   id 1059266
name color-018   id 1059265
name color-017   id 1059264
name color-016   id 1059263
name color-015   id 1059262
name color-014   id 1059261
name color-013   id 1059260
name color-012   id 1059259
name color-011   id 1059258
name color-010   id 1059257
name color-009   id 1059256
name color-008   id 1059255
name color-007   id 1059254
name color-006   id 1059253
name color-005   id 1059252
name color-004   id 1059251
name color-003   id 1059250
name color-002   id 1059249
name color-001   id 1059248

"""

# ICON IDs
ID_LAY_NOLAYER  = 1059268
ID_LAY_FOLDER   = 1059269
ID_LAY_ADD      = 1059270
ID_LAY_OVER     = 1059271
ID_LAY_AUTO     = 1059272
ID_LAY_ADOPT    = 1059273

ID_COL_NONE     = 1059248
ID_COL_CUSTOM   = 1059249
ID_COL_RAND     = 1059250
ID_COL_MIMOSA   = 1059251
ID_COL_SALMON   = 1059252
ID_COL_PERFUME  = 1059253
ID_COL_JELLYBEAN= 1059254
ID_COL_TOPAZ    = 1059255
ID_COL_ANZAC    = 1059256
ID_COL_LAVENBLUE= 1059257
ID_COL_PALECYAN = 1059258
ID_COL_MELROSE  = 1059259
ID_COL_AQUAMARINE=1059260
ID_COL_PASTELGRN= 1059261
ID_COL_NOBEL    = 1059262
ID_COL_GRANITE  = 1059263
ID_COL_CAPECOD  = 1059264

# GUI IDs
GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_ALT         = 1002
GRP_BTN         = 1003

FOL_NAMETEXT    = 3001
FOL_NAMEINPUT   = 3002
FOL_ICONCB      = 3003
FOL_COLORCB     = 3004
FOL_LAYERTEXT   = 3005
FOL_LAYERCB     = 3006

FOL_PROTECT     = 3007
FOL_SEPARATOR   = 3008
FOL_WORLDZERO   = 3009
FOL_OPEN        = 3010

COL_MIMOSA      = 4001
COL_SALMON      = 4002
COL_PARFUME     = 4003
COL_JELLYBEAN   = 4004
COL_TOPAZ       = 4005
COL_ANZAC       = 4006
COL_LAVENBLUE   = 4007
COL_PALECYAN    = 4008
COL_MELROSE     = 4009
COL_AQUAMARINE  = 4010
COL_PASTELGRN   = 4011
COL_PASTELGRN   = 4016
COL_NOBEL       = 4017
COL_GRANITE     = 4018
COL_CAPECOD     = 4019

COL_RANDOM      = 4012
COL_CUSTOM      = 4013
COL_SEP         = 4014
COL_NONE        = 4015

ICO_FOLDER      = 5001
ICO_OPEN        = 5002
ICO_CIRCLE      = 5003
ICO_STAR        = 5004
ICO_NULL        = 5005
ICO_BIN         = 5006

LAY_FOLDER      = 6001
LAY_ADD         = 6002
LAY_OVER        = 6003
LAY_NONE        = 6004
LAY_ADOPT       = 6006
LAY_AUTOTAG     = 6005

BTN_OK          = 7001
BTN_CANCEL      = 7002

# Functions
def GetVersion():
    version = c4d.GetC4DVersion() # Get Cinema 4D version
    if len(str(version)) >= 7: # Cinema 2023 or newer
        app = True # New enough
    elif len(str(version)) == 5: # Older than 2023
        majorVersion = int(str(version)[:2])
        if majorVersion >= 20: # If newer than R20
            app = True
        else:
            app = False # Too old
    return app

def GetFolderSeparator():
    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
        return "\\"
    else: # If operating system is Mac or Linux
        return "/"

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_Folder.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("Null\n4012\n1\n0\n5001\n6004\n0,0,0\n1\n0") # Default settings
        f.close()
    return filePath

def CreateUserDataString(obj, name, link, parentGroup=None, shortname=None):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_STRING)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_DEFAULT] = link
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = link
    return element

def CreateUserDataInteger(obj, name, val=0, parentGroup=None, unit=c4d.DESC_UNIT_INT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_STEP] = 1
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataCycle(obj, name, link, cycle, parentGroup=None, shortname=None, unit=c4d.DESC_UNIT_INT):
    if obj is None: return False
    if shortname is None: shortname = name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc.SetInt32(c4d.DESC_CUSTOMGUI, c4d.CUSTOMGUI_CYCLE)
    cycleContainer = c4d.BaseContainer()
    for i, c in enumerate(cycle):
        cycleContainer.SetString(i, c)
    bc[c4d.DESC_CYCLE] = cycleContainer
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = shortname
    bc[c4d.DESC_DEFAULT] = link
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = link
    return element

def loadSettings():
    optionsFile = CheckFiles()
    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile) # Open the file for reading
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"))

    optionsArray = [] # Initialize an array for options
    for line in f: # Iterate through every row
        line = line.rstrip('\n') # Strip newline stuff
        optionsArray.append(line)
    f.close() # Close the file
    options = {
        'setName'     : optionsArray[0],
        'setColor'    : optionsArray[1],
        'setProtect'  : optionsArray[2],
        'setSeparator': optionsArray[3],
        'setIcon'     : optionsArray[4],
        'setLayer'    : optionsArray[5],
        'setCustom'   : optionsArray[6],
        'setWorldZero': optionsArray[7],
        'setOpenFolder': optionsArray[8]
    }

    return options

def saveSettings(name, color, protect, separator, icon, layer, customColor, worldzero, openfolder):
    #path, fn = os.path.split(__file__)
    #optionsFile = os.path.join(path, "AR_Folder.txt")
    optionsFile = CheckFiles() #

    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile, 'w') # Open the file for writing
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"), 'w') # Open the file for writing

    settings = [str(name),
                str(color),
                str(protect),
                str(separator),
                str(icon),
                str(layer),
                str(customColor.x)+","+str(customColor.y)+","+str(customColor.z),
                str(worldzero),
                str(openfolder)]

    settings = "\n".join(settings) # Create a string from an array
    f.write(settings) # Write settings to the file
    f.close() # Close the file
    return True # Everything is fine

def GetNextObject(op): # Get next object from Object Manager
    global level # Access to global variable (level)
    if op is None: # If there is no object
        return None # Return none
    if op.GetDown(): # If can go deeper in hierarchy
        level += 1 # Going deeper in levels
        return op.GetDown() # Return object
    while not op.GetNext() and op.GetUp(): # If can't go to next object, but can go up
        level -= 1 # Going up in levels
        op = op.GetUp() # Object is parent object
    return op.GetNext() # Return object

def BuildHierarchyPath(obj): # Build hierarchy path for object
    global level # Access to global variable (level)
    path = [] # Initialize empty list for path
    for i in range(0,level+1): # Iterate through levels
        path.append(obj) # Add object to path list
        if obj.GetUp() is not None: # If can go up in Object Manager
            obj = obj.GetUp() # Going up
    path.reverse() # Reverse path list
    return path # Return hierarchy path

def BuildHierarchy(): # Build hierarchy dictionary
    global level # Access to global variable (level)
    global hierarchy # Access to global dictionary (hierarchy)
    doc = c4d.documents.GetActiveDocument()
    op = doc.GetFirstObject()
    #hierarchy = {} # Initialize empty dictionary
    i = 0 # Iteration variable
    if op is None: # If there is no object
        return # Return nothing
    while op: # While there is object
        hierarchy[i]={ # Add object information to hierarchy dictionary
            'object': op, # Object
            'level': level, # Object's level (how deep object is in Object Manager)
            'name': op.GetName(), # Object's name
            'root': FindRoot(op), # Object's root
            'path': BuildHierarchyPath(op) # Object's full path in hierarchy
        }
        op = GetNextObject(op) # Get next object from Object Manager
        i += 1 # Increase iteration variable
    return hierarchy # Return hierarchy dictionary

def FindRoot(data): # Find object's root
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        collection = [] # Initialize empty list for root object(s)
        for obj in lst: # Loop through objects in
            while obj: # Infinite loop
                if obj.GetUp() == None: # If can't go up in hierarchy
                    collection.append(obj) # Add object to collection list
                    break # Break the loop
                obj = obj.GetUp() # Go up
        return collection # Return collection of root object(s)
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        while obj: # Infinite loop
            if obj.GetUp() == None: # If can't go up in Object Manager
                return obj # Return object
                break # Break the loop
            obj = obj.GetUp() # Get up

def FindChildren(start, targetLevel=0, addRest=False): # Find children of the object
    global level # Access to global variable (level)
    global hierarchy # Access to global dictionary (hierarchy)
    collection = [] # Initialize empty list for children
    for h in hierarchy: # Loop through hierarchy
        if start == hierarchy[h]['object']: # Starting position in hierarchy
            l = hierarchy[h]['level'] # Starting level
    for counter, item in hierarchy.items(): # Loop through items in hierarchy dictionary
        for p in item['path']: # Loop through objects' paths
            if p == start: # Starting position in hierarchy
                for c, i in enumerate(item['path']): # Loop through object's path
                    if c > l: # If child of the selected object
                        if targetLevel != 0: # If there is custom target level
                            if addRest:
                                if c >= l + targetLevel: # If level match
                                    collection.append(i) # Add object to collection
                            else:
                                if c == l + targetLevel: # If level match
                                    collection.append(i) # Add object to collection
                        else: # If there is no target level (default)
                            collection.append(i) # Add object to collection
    return collection # Return collection of children

def Select(data): # Select object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Loop through list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.SetBit(c4d.BIT_ACTIVE) # Select object in Object Manager

def Deselect(data): # Deselect object(s)
    dataType = type(data).__name__ # Get incoming data type name
    # List (data)
    if dataType == "list": # If data is list do following
        lst = data # Data is list
        for obj in lst: # Data is list
            doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
            obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager
    # Single object (data)
    elif dataType == "BaseObject": # If data is single object do following
        obj = data # Data is object
        doc.AddUndo(c4d.UNDOTYPE_BITS, obj) # Add undo command for changing bits
        obj.DelBit(c4d.BIT_ACTIVE) # Deselect object in Object Manager

def createFolderNull(name, selColor, selProtect, selSeparator, selIcon, selLayer, customColor, worldzero, openfolder):
    global hierarchy # Access to global dictionary (hierarchy)
    c4dver = GetVersion()
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos

    # Separator null code
    separatorTagCode = "import c4d\n\
def check(baseWeight, string):\n\
    weight = getWeight(string)\n\
    pp = True\n\
    while weight > baseWeight:\n\
        if pp == True:\n\
            string = string[:-1]\n\
            pp = False\n\
        elif pp == False:\n\
            string = string[1:]\n\
            pp = True\n\
        weight = getWeight(string)\n\
    return string\n\
\n\
def insert_string(org_string, string, pos=None):\n\
    if pos is None:\n\
        pos = int(len(org_string) / 2)\n\
    return org_string[:pos] + ' ' + string + ' ' + org_string[pos:]\n\
\n\
def getWeight(st): # Unit\n\
    weight = 0\n\
    for s in st:\n\
        if   s in 'W@': weight += 3.4\n\
        elif s in 'M½': weight += 3.2\n\
        elif s in 'OÖÓÒÔmw%&': weight += 3\n\
        elif s in 'DGHNQUÚÙÛÜ+=^><~': weight += 2.5\n\
        elif s in 'AÁÀÂÅÄCRVbdrghnoöóòôpqu#': weight += 2.4\n\
        elif s in '0123456789BEÉÈÊËFKPSTXZaáàäâåeéèëêk$€£¤': weight += 2\n\
        elif s in 'LYcsvxyz?*§_': weight += 1.6\n\
        elif s in 'Jfrt-\"/\\\\': weight += 1.5\n\
        elif s in 'Iijl.,:!|[](){}\\'´` ': weight += 1\n\
    return weight\n\
\n\
def main():\n\
    width = op.GetObject()[c4d.ID_USERDATA,3]\n\
    style = op.GetObject()[c4d.ID_USERDATA,2]\n\
\n\
    if style == 0:\n\
        char = '-'\n\
        baseStr = char*int(width)\n\
    elif style == 1:\n\
        char = '='\n\
        baseStr = char*int(((width+8)/2))\n\
    elif style == 2:\n\
        char = '_'\n\
        baseStr = char*int((width-3))\n\
    elif style == 3:\n\
        char = '~'\n\
        baseStr = char*int(((width+8)/2))\n\
\n\
    baseWeight = getWeight(baseStr)\n\
    nameStr = op.GetObject()[c4d.ID_USERDATA,1]\n\
    newName = check(baseWeight, insert_string(baseStr, nameStr))\n\
    op.GetObject().SetName(newName)"

    autoLayerTagCode = "import c4d\n\
def FindParent(op, parent):\n\
    while op.GetUp() is not None:\n\
        op = op.GetUp()\n\
        if op == parent:\n\
            return op\n\
    return op\n\
\n\
def GetNext(op):\n\
    if op is None: return None\n\
    if op.GetDown():\n\
        return op.GetDown()\n\
    while not op.GetNext() and op.GetUp():\n\
        op = op.GetUp()\n\
    return op.GetNext()\n\
\n\
def CollectAllChildren(op):\n\
    root = op\n\
    if op is None: return\n\
    collected = []\n\
    while op:\n\
        if FindParent(op, root) == root:\n\
            collected.append(op)\n\
        op = GetNext(op)\n\
    return collected\n\
\n\
def main():\n\
    obj = op.GetObject()\n\
    children = obj.GetChildren()\n\
    layer = obj[c4d.ID_LAYER_LINK]\n\
    if layer is None: return False\n\
    allChildren = CollectAllChildren(obj)\n\
    for child in allChildren:\n\
        child[c4d.ID_LAYER_LINK] = layer"

    # Choose color and icon
    randRed     = random.random()
    randGreen   = random.random()
    randBlue    = random.random()
    randomColor = c4d.Vector(randRed, randGreen, randBlue)

    colors = {
        COL_MIMOSA:      c4d.Vector(float(251.0/255.0), float(253.0/255.0), float(212.0/255.0)),
        COL_SALMON:      c4d.Vector(float(255.0/255.0), float(159.0/255.0), float(155.0/255.0)),
        COL_PARFUME:     c4d.Vector(float(239.0/255.0), float(175.0/255.0), float(245.0/255.0)),
        COL_JELLYBEAN:   c4d.Vector(float(227.0/255.0), float(91.0/255.0), float(91.0/255.0)),
        COL_TOPAZ:       c4d.Vector(float(255.0/255.0), float(197.0/255.0), float(121.0/255.0)),
        COL_ANZAC:       c4d.Vector(float(222.0/255.0), float(151.0/255.0), float(69.0/255.0)),
        COL_LAVENBLUE:   c4d.Vector(float(197.0/255.0), float(212.0/255.0), float(248.0/255.0)),
        COL_PALECYAN:    c4d.Vector(float(142.0/255.0), float(220.0/255.0), float(252.0/255.0)),
        COL_MELROSE:     c4d.Vector(float(153.0/255.0), float(153.0/255.0), float(255.0/255.0)),
        COL_AQUAMARINE:  c4d.Vector(float(143.0/255.0), float(255.0/255.0), float(188.0/255.0)),
        COL_PASTELGRN:   c4d.Vector(float(108.0/255.0), float(229.0/255.0), float(130.0/255.0)),
        COL_NOBEL:       c4d.Vector(float(179.0/255.0), float(179.0/255.0), float(179.0/255.0)),
        COL_GRANITE:     c4d.Vector(float(102.0/255.0), float(102.0/255.0), float(102.0/255.0)),
        COL_CAPECOD:     c4d.Vector(float(60.0/255.0), float(61.0/255.0), float(61.0/255.0)),
        COL_RANDOM:      randomColor, # Random color
        COL_CUSTOM:      customColor, # Custom color
        COL_NONE:        None         # No color
    }

    icons = {
        ICO_NULL:   "5140", # Null icon
        ICO_FOLDER: "1052837", # Folder
        ICO_OPEN:   "1052838", # Open folder
        ICO_CIRCLE: "17106" # Circle
    }

    color = colors[selColor] # Get selected color
    icon = icons[selIcon] # Get selected icon

    selection = doc.GetActiveObjects(0) # Get active selection

    # Null object
    null = c4d.BaseObject(c4d.Onull) # Initialize a null object
    null.SetName(name) # Set null object's name
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Display: None

    if not worldzero:
        if len(selection) > 1: # If more than one object selected
            helperAxis = doc.GetHelperAxis() # Get helper axis
            null.SetMg(helperAxis.GetMg()) # Set matrix from multi selection
        elif len(selection) == 1: # If only one object selected
            null.SetMg(selection[0].GetMg()) # Set matrix from selected object
        else: # Otherwise
            pass # Do nothing

    null[c4d.ID_BASELIST_ICON_FILE] = icon # Folder icon
    if color != None:
        null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Icon Color: Custom
        null[c4d.ID_BASELIST_ICON_COLOR] = color
    else:
        pass

    if color != None:
        null[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color: On
        null[c4d.ID_BASEOBJECT_COLOR] = color

    # Protection tag
    if selProtect == True:
        protectionTag = c4d.BaseTag(5629) # Initialize a protection tag
        protectionTag[c4d.PROTECTION_ALLOW_EXPRESSIONS] = True # Allow expressions
        protectionTag[c4d.PROTECTION_ALLOW_DUPLICATION] = True # Allow viewport duplication
        null.InsertTag(protectionTag) # Insert tag to the object

    if (selLayer == LAY_ADOPT): # Adopt layer from selected object
        if len(selection) > 0: # If there's a selected object
            adoptLayer = selection[0][c4d.ID_LAYER_LINK]
            if adoptLayer != None: # If there's layer
                null[c4d.ID_LAYER_LINK] = adoptLayer # Adopt layer
                if (c4dver == True):
                    if color == None:
                        null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Icon Color: Custom
                        null[c4d.ID_BASELIST_ICON_COLOR] = adoptLayer[c4d.ID_LAYER_COLOR] # Set color
    elif (selLayer != LAY_NONE):
        layerRoot = doc.GetLayerObjectRoot() # Get layer object root
        layer = c4d.documents.LayerObject() # Initialize a layer object
        layer.SetName(name) # Set layer's name
        if color != None:
            layer[c4d.ID_LAYER_COLOR] = color # Set layer's color
        layer.InsertUnder(layerRoot) # Insert layer to layer root
        doc.AddUndo(c4d.UNDOTYPE_NEW, layer) # Record undo for creating a new layer
        null[c4d.ID_LAYER_LINK] = layer # Set layer to the null
    else:
        pass

    # Separator tag
    if selSeparator == True:
        separatorTag = c4d.BaseTag(1022749) # Initialize a python tag
        separatorTag[c4d.TPYTHON_CODE] = separatorTagCode
        null.InsertTag(separatorTag) # Put the tag to the null
        CreateUserDataString(null, "Name", name) # Crete user data string input
        CreateUserDataCycle(null, "Style", 0, ['-', '=', '_', '~']) # Create user data cycle data
        CreateUserDataInteger(null, "Width", 25) # Create user data integer stuff
        separatorTag[c4d.ID_BASELIST_NAME] = "Separator"

    # Other stuff
    doc.AddUndo(c4d.UNDOTYPE_NEW, null) # Add undo command for creating a new object
    doc.InsertObject(null) # Insert null object to the document

    if len(selection) != 0: # If there are selected objects
        null.InsertBefore(selection[0]) # Move null
        hierarchy = BuildHierarchy() # Build hierarchy
        for s in selection: # Iterate through selected objects
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for changing object
            mat = s.GetMg() # Get global matrix
            s.InsertUnderLast(null) # Move under the null object
            s.SetMg(mat) # Set global matrix
            s.DelBit(c4d.BIT_ACTIVE) # Deselect object

            # If object doesn't have a layer -> add it
            if (selLayer == LAY_ADD):
                objectLayer = s.GetLayerObject(doc) # Get object's layer
                if objectLayer == None: # If object does not already have a layer
                    s[c4d.ID_LAYER_LINK] = layer # Set layer to the object
                children = FindChildren(s, 0, True) # Get children
                for child in children: # Iterate through children
                    objectLayer = child.GetLayerObject(doc) # Get object's layer
                    if objectLayer == None: # If object does not already have a layer
                        child[c4d.ID_LAYER_LINK] = layer # Set layer to the object

            # Force add layers
            if (selLayer == LAY_OVER):
                s[c4d.ID_LAYER_LINK] = layer # Set layer to the object
                children = FindChildren(s, 0, True)
                for child in children:
                    child[c4d.ID_LAYER_LINK] = layer # Set layer to the object

    # Auto layer python tag
    if (selLayer == LAY_AUTOTAG):
        autoLayerTag = c4d.BaseTag(1022749) # Initialize a python tag
        autoLayerTag[c4d.TPYTHON_CODE] = autoLayerTagCode
        null.InsertTag(autoLayerTag) # Put the tag to the null
        autoLayerTag[c4d.ID_BASELIST_NAME] = "Auto Layer"

    # Open folder null
    if openfolder:
        null.ChangeNBit(c4d.NBIT_OM1_FOLD, c4d.NBITCONTROL_SET) # Unfold

    null.SetBit(c4d.BIT_ACTIVE) # Select null
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        global customColor

        self.SetTitle("Create Folder Null") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, 1, 2) # Begin 'Mega1' group
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        # Inputs
        self.GroupBegin(GRP_MAIN, c4d.BFH_LEFT, 4, 1, "") # Begin 'Main' group
        self.GroupBorderSpace(5, 3, 5, 3)
        #self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
        self.AddEditText(FOL_NAMEINPUT, c4d.BFH_LEFT, initw=200, inith=0)

        # Icon
        self.AddComboBox(FOL_ICONCB, c4d.BFH_LEFT, 35, 13)
        self.AddChild(FOL_ICONCB, ICO_NULL, "Null&i5140&") # Null
        self.AddChild(FOL_ICONCB, COL_SEP, "") # Separator line
        self.AddChild(FOL_ICONCB, ICO_OPEN, "Folder 1&i1052838&") # Open folder
        self.AddChild(FOL_ICONCB, ICO_FOLDER, "Folder 2&i1052837&") # Closed folder
        self.AddChild(FOL_ICONCB, ICO_CIRCLE, "Circle&i17106&") # Circle

        # Color
        self.AddComboBox(FOL_COLORCB, c4d.BFH_LEFT, 35, 13)
        self.AddChild(FOL_COLORCB, COL_NONE, "None&i"+str(ID_COL_NONE)+"&") # No Color
        self.AddChild(FOL_COLORCB, COL_CUSTOM, "Custom&i"+str(ID_COL_CUSTOM)+"&") # Custom
        self.AddChild(FOL_COLORCB, COL_RANDOM, "Random&i"+str(ID_COL_RAND)+"&") # Random
        self.AddChild(FOL_COLORCB, COL_SEP, "") # Separator line
        self.AddChild(FOL_COLORCB, COL_MIMOSA, "Mimosa&i"+str(ID_COL_MIMOSA)+"&")
        self.AddChild(FOL_COLORCB, COL_SALMON, "Salmon&i"+str(ID_COL_SALMON)+"&")
        self.AddChild(FOL_COLORCB, COL_PARFUME, "Perfume&i"+str(ID_COL_PERFUME)+"&")
        self.AddChild(FOL_COLORCB, COL_JELLYBEAN, "Jelly Bean&i"+str(ID_COL_JELLYBEAN)+"&")
        self.AddChild(FOL_COLORCB, COL_TOPAZ, "Topaz&i"+str(ID_COL_TOPAZ)+"&")
        self.AddChild(FOL_COLORCB, COL_ANZAC, "Anzac&i"+str(ID_COL_ANZAC)+"&")
        self.AddChild(FOL_COLORCB, COL_LAVENBLUE, "Lavender Blue&i"+str(ID_COL_LAVENBLUE)+"&")
        self.AddChild(FOL_COLORCB, COL_PALECYAN, "Pale Cyan&i"+str(ID_COL_PALECYAN)+"&")
        self.AddChild(FOL_COLORCB, COL_MELROSE, "Melrose&i"+str(ID_COL_MELROSE)+"&")
        self.AddChild(FOL_COLORCB, COL_AQUAMARINE, "Aquamarine&i"+str(ID_COL_AQUAMARINE)+"&")
        self.AddChild(FOL_COLORCB, COL_PASTELGRN, "Pastel Green&i"+str(ID_COL_PASTELGRN)+"&")
        self.AddChild(FOL_COLORCB, COL_NOBEL, "Nobel&i"+str(ID_COL_NOBEL)+"&")
        self.AddChild(FOL_COLORCB, COL_GRANITE, "Granite&i"+str(ID_COL_GRANITE)+"&")
        self.AddChild(FOL_COLORCB, COL_CAPECOD, "Cape Cod&i"+str(ID_COL_CAPECOD)+"&")

        # Layers
        self.AddComboBox(FOL_LAYERCB, c4d.BFH_RIGHT, 35, 13)
        self.AddChild(FOL_LAYERCB, LAY_NONE, "No Layer&i"+str(ID_LAY_NOLAYER)+"&")
        self.AddChild(FOL_LAYERCB, LAY_FOLDER, "Folder Only&i"+str(ID_LAY_FOLDER)+"&")
        self.AddChild(FOL_LAYERCB, LAY_ADD, "Add Layer&i"+str(ID_LAY_ADD)+"&")
        self.AddChild(FOL_LAYERCB, LAY_OVER, "Overwrite Layer&i"+str(ID_LAY_OVER)+"&")
        self.AddChild(FOL_LAYERCB, LAY_ADOPT, "Adopt Layer&i"+str(ID_LAY_ADOPT)+"&")
        self.AddChild(FOL_LAYERCB, LAY_AUTOTAG, "Auto Layer Tag&i"+str(ID_LAY_AUTO)+"&")
        #
        self.GroupEnd() # End 'Main' group

        #
        self.GroupBegin(9000, c4d.BFH_SCALEFIT, 4, 1, "") # Begin 'Alt' group
        #self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
        #self.GroupBorder(c4d.BORDER_NONE)
        self.GroupBorderSpace(5, 0, 5, 0)
        self.AddCheckbox(FOL_WORLDZERO, c4d.BFH_CENTER | c4d.BFH_SCALEFIT, 0, 13, "Place to origin ")
        self.AddCheckbox(FOL_PROTECT, c4d.BFH_CENTER | c4d.BFH_SCALEFIT, 0, 13, "Protected ")
        self.AddCheckbox(FOL_SEPARATOR, c4d.BFH_CENTER | c4d.BFH_SCALEFIT, 0, 13, "Separator ")
        self.AddCheckbox(FOL_OPEN, c4d.BFH_CENTER | c4d.BFH_SCALEFIT, 0, 13, "Open")
        self.GroupEnd() # End 'Alt' group

        # Set default options
        settings = loadSettings()
        self.SetString(FOL_NAMEINPUT, str(settings['setName']))
        self.SetInt32(FOL_COLORCB,    int(settings['setColor']))

        self.SetInt32(FOL_ICONCB, int(settings['setIcon']))

        self.SetInt32(FOL_LAYERCB,   int(settings['setLayer']))
        self.SetBool(FOL_PROTECT,    int(settings['setProtect']))
        self.SetBool(FOL_SEPARATOR,  int(settings['setSeparator']))
        self.SetBool(FOL_WORLDZERO,  int(settings['setWorldZero']))
        self.SetBool(FOL_OPEN,       int(settings['setOpenFolder']))

        cRGB = str(settings['setCustom']).split(",")
        customColor = c4d.Vector(float(cRGB[0]), float(cRGB[1]), float(cRGB[2]))

        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Mega1' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End 'Buttons' group

        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global customColor
        bc = c4d.BaseContainer() # Initialize a base container

        name        = str(self.GetString(FOL_NAMEINPUT)) # Get name
        color       = int(self.GetInt32(FOL_COLORCB)) # Get color
        protect     = int(self.GetBool(FOL_PROTECT)) # Get protected
        separator   = int(self.GetBool(FOL_SEPARATOR)) # Get separator
        worldzero   = int(self.GetBool(FOL_WORLDZERO)) # Get world zero
        openfolder  = int(self.GetBool(FOL_OPEN)) # Get open
        icon        = int(self.GetInt32(FOL_ICONCB)) # Get icon
        layer       = int(self.GetInt32(FOL_LAYERCB)) # Get layer option

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            if (color == COL_CUSTOM):
                customColor = c4d.gui.ColorDialog(0, customColor)
                if customColor == None:
                    self.Close() # Close dialog
                    return False

            createFolderNull(name, color, protect, separator, icon, layer, customColor, worldzero, openfolder) # Run the main algorithm
            saveSettings(name, color, protect, separator, icon, layer, customColor, worldzero, openfolder)
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            if (color == COL_CUSTOM):
                customColor = c4d.gui.ColorDialog(0, customColor)
            createFolderNull(name, color, protect, separator, icon, layer, customColor, worldzero, openfolder) # Run the main algorithm
            saveSettings(name, color, protect, separator, icon, layer, customColor, worldzero, openfolder)
            self.Close() # Close dialog

        return True # Everything is fine

# Registering icons etc.
fsep = GetFolderSeparator() # Get folder separator
fn = __file__ # Get script filepath
fn = fn[:fn.rfind(fsep)] # Get script's folder path

icn_c01 = gui.GetIcon(ID_COL_NONE) # Get icon
if icn_c01 == None: # If icon not registered, do it
    bm_c01 = bm.BaseBitmap() # Init basebitmap
    fn_c01 = os.path.join(fn, "AR_Folder", "Colors", "color_empty.tif") # Icon iamge path
    res = bm_c01.InitWith(fn_c01)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_NONE, bm_c01) # Register icon

icn_c02 = gui.GetIcon(ID_COL_CUSTOM)
if icn_c02 == None:
    bm_c02 = bm.BaseBitmap()
    fn_c02 = os.path.join(fn, "AR_Folder", "Colors", "color_custom.tif")
    res = bm_c02.InitWith(fn_c02)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_CUSTOM, bm_c02)

icn_c03 = gui.GetIcon(ID_COL_RAND)
if icn_c03 == None:
    bm_c03 = bm.BaseBitmap()
    fn_c03 = os.path.join(fn, "AR_Folder", "Colors", "color_random.tif")
    res = bm_c03.InitWith(fn_c03)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_RAND, bm_c03)

icn_c04 = gui.GetIcon(ID_COL_MIMOSA)
if icn_c04 == None:
    bm_c04 = bm.BaseBitmap()
    fn_c04 = os.path.join(fn, "AR_Folder", "Colors", "color_001.tif")
    res = bm_c04.InitWith(fn_c04)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_MIMOSA, bm_c04)

icn_c05 = gui.GetIcon(ID_COL_SALMON)
if icn_c05 == None:
    bm_c05 = bm.BaseBitmap()
    fn_c05 = os.path.join(fn, "AR_Folder", "Colors", "color_002.tif")
    res = bm_c05.InitWith(fn_c05)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_SALMON, bm_c05)

icn_c06 = gui.GetIcon(ID_COL_PERFUME)
if icn_c06 == None:
    bm_c06 = bm.BaseBitmap()
    fn_c06 = os.path.join(fn, "AR_Folder", "Colors", "color_003.tif")
    res = bm_c06.InitWith(fn_c06)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_PERFUME, bm_c06)

icn_c07 = gui.GetIcon(ID_COL_JELLYBEAN)
if icn_c07 == None:
    bm_c07 = bm.BaseBitmap()
    fn_c07 = os.path.join(fn, "AR_Folder", "Colors", "color_004.tif")
    res = bm_c07.InitWith(fn_c07)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_JELLYBEAN, bm_c07)

icn_c08 = gui.GetIcon(ID_COL_TOPAZ)
if icn_c08 == None:
    bm_c08 = bm.BaseBitmap()
    fn_c08 = os.path.join(fn, "AR_Folder", "Colors", "color_005.tif")
    res = bm_c08.InitWith(fn_c08)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_TOPAZ, bm_c08)

icn_c09 = gui.GetIcon(ID_COL_ANZAC)
if icn_c09 == None:
    bm_c09 = bm.BaseBitmap()
    fn_c09 = os.path.join(fn, "AR_Folder", "Colors", "color_006.tif")
    res = bm_c09.InitWith(fn_c09)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_ANZAC, bm_c09)

icn_c10 = gui.GetIcon(ID_COL_LAVENBLUE)
if icn_c10 == None:
    bm_c10 = bm.BaseBitmap()
    fn_c10 = os.path.join(fn, "AR_Folder", "Colors", "color_007.tif")
    res = bm_c10.InitWith(fn_c10)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_LAVENBLUE, bm_c10)

icn_c11 = gui.GetIcon(ID_COL_PALECYAN)
if icn_c11 == None:
    bm_c11 = bm.BaseBitmap()
    fn_c11 = os.path.join(fn, "AR_Folder", "Colors", "color_008.tif")
    res = bm_c11.InitWith(fn_c11)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_PALECYAN, bm_c11)

icn_c12 = gui.GetIcon(ID_COL_MELROSE)
if icn_c12 == None:
    bm_c12 = bm.BaseBitmap()
    fn_c12 = os.path.join(fn, "AR_Folder", "Colors", "color_009.tif")
    res = bm_c12.InitWith(fn_c12)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_MELROSE, bm_c12)

icn_c13 = gui.GetIcon(ID_COL_AQUAMARINE)
if icn_c13 == None:
    bm_c13 = bm.BaseBitmap()
    fn_c13 = os.path.join(fn, "AR_Folder", "Colors", "color_010.tif")
    res = bm_c13.InitWith(fn_c13)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_AQUAMARINE, bm_c13)

icn_c14 = gui.GetIcon(ID_COL_PASTELGRN)
if icn_c14 == None:
    bm_c14 = bm.BaseBitmap()
    fn_c14 = os.path.join(fn, "AR_Folder", "Colors", "color_011.tif")
    res = bm_c14.InitWith(fn_c14)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_PASTELGRN, bm_c14)

icn_c15 = gui.GetIcon(ID_COL_NOBEL)
if icn_c15 == None:
    bm_c15 = bm.BaseBitmap()
    fn_c15 = os.path.join(fn, "AR_Folder", "Colors", "color_012.tif")
    res = bm_c15.InitWith(fn_c15)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_NOBEL, bm_c15)

icn_c16 = gui.GetIcon(ID_COL_GRANITE)
if icn_c16 == None:
    bm_c16 = bm.BaseBitmap()
    fn_c16 = os.path.join(fn, "AR_Folder", "Colors", "color_013.tif")
    res = bm_c16.InitWith(fn_c16)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_GRANITE, bm_c16)

icn_c17 = gui.GetIcon(ID_COL_CAPECOD)
if icn_c17 == None:
    bm_c17 = bm.BaseBitmap()
    fn_c17 = os.path.join(fn, "AR_Folder", "Colors", "color_014.tif")
    res = bm_c17.InitWith(fn_c17)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_COL_CAPECOD, bm_c17)

# -------------------------------------------------------------------

icn_l01 = gui.GetIcon(ID_LAY_NOLAYER)
if icn_l01 == None:
    bm_l01 = bm.BaseBitmap()
    fn_l01 = os.path.join(fn, "AR_Folder", "Layer", "no_layer.tif")
    res = bm_l01.InitWith(fn_l01)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_NOLAYER, bm_l01)

icn_l02 = gui.GetIcon(ID_LAY_FOLDER)
if icn_l02 == None:
    bm_l02 = bm.BaseBitmap()
    fn_l02 = os.path.join(fn, "AR_Folder", "Layer", "folder_only.tif")
    res = bm_l02.InitWith(fn_l02)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_FOLDER, bm_l02)

icn_l03 = gui.GetIcon(ID_LAY_ADD)
if icn_l03 == None:
    bm_l03 = bm.BaseBitmap()
    fn_l03 = os.path.join(fn, "AR_Folder", "Layer", "add_layer.tif")
    res = bm_l03.InitWith(fn_l03)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_ADD, bm_l03)

icn_l04 = gui.GetIcon(ID_LAY_OVER)
if icn_l04 == None:
    bm_l04 = bm.BaseBitmap()
    fn_l04 = os.path.join(fn, "AR_Folder", "Layer", "overwrite.tif")
    res = bm_l04.InitWith(fn_l04)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_OVER, bm_l04)

icn_l05 = gui.GetIcon(ID_LAY_AUTO)
if icn_l05 == None:
    bm_l05 = bm.BaseBitmap()
    fn_l05 = os.path.join(fn, "AR_Folder", "Layer", "autolayertag.tif")
    res = bm_l05.InitWith(fn_l05)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_AUTO, bm_l05)

icn_l06 = gui.GetIcon(ID_LAY_ADOPT)
if icn_l06 == None:
    bm_l06 = bm.BaseBitmap()
    fn_l06 = os.path.join(fn, "AR_Folder", "Layer", "adopt_layer.tif")
    res = bm_l06.InitWith(fn_l06)
    if res[0] == c4d.IMAGERESULT_OK:
        gui.RegisterIcon(ID_LAY_ADOPT, bm_l06)

# -------------------------------------------------------------------
# Open the dialog
dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog