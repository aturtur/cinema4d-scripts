"""
AR_Folder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_Folder
Version: 1.0.5
Description-US: Creates a folder null that keeps your project tidy

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.5 (07.09.2021) - Added color option 'None' (No color, just default settings)
1.0.4 (15.03.2021) - Added and autolayer python tag and some kind of support for R20
1.0.3 (14.03.2021) - Cinema 4D R23 support for separator python tag
1.0.2 (12.03.2021) - Big update, a lot of changes and new features
1.0.1 (07.11.2020) - Added support for Esc and Enter keys

To Do:
> Shift modifier: Modify Folder Null, change color and name ... 

"""
# Libraries
import c4d
import os
import sys
import random
from c4d.gui import GeDialog

# Global variables
hierarchy = {} # Initialize hierarchy dictionary
level     = 0  # Initialize level variable (how deep object is in hierarchy)

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

COL_BLUE        = 4001
COL_FUCHIA      = 4002
COL_GREEN       = 4003
COL_ORANGE      = 4004
COL_SEANCE      = 4005
COL_RED         = 4006
COL_YELLOW      = 4007
COL_DARK        = 4008
COL_BRIGHT      = 4009
COL_DARKBLUE    = 4010
COL_PURPLEHEART = 4011
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
LAY_AUTOTAG     = 6005

BTN_OK          = 7001
BTN_CANCEL      = 7002

customColor     = c4d.Vector(0,0,0)


# Functions
def GetC4DVersion():
    c4dversion = c4d.GetC4DVersion()
    releaseVersion = int(str(c4dversion)[:2])
    buildVersion = int(str(c4dversion)[:2])
    return releaseVersion, buildVersion

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
    path, fn = os.path.split(__file__)
    optionsFile = os.path.join(path, "AR_Folder.txt")
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
        'setCustom'   : optionsArray[6]
    }

    return options

def saveSettings(name, color, protect, separator, icon, layer, customColor):
    path, fn = os.path.split(__file__)
    optionsFile = os.path.join(path, "AR_Folder.txt")

    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile, 'w') # Open the file for writing
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"), 'w') # Open the file for writing

    settings = [ str(name),
                 str(color),
                 str(protect),
                 str(separator),
                 str(icon),
                 str(layer),
                 str(customColor.x)+","+str(customColor.y)+","+str(customColor.z)]

    settings = "\n".join(settings) # Create a string from an array
    f.write(settings) # Write settings to the file
    f.close() # Close the file

    return True # Everything is fine

    path, fn = os.path.split(__file__)
    optionsFile = os.path.join(path, "res", "AR_Folder.txt")

    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile) # Open the file for reading
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"))

    optionsArray = [] # Initialize an array for options
    for line in f: # Iterate through every row
        line = line.rstrip('\n') # Strip newline stuff
        if line == 'True': # If line is true
            optionsArray.append(1) # Add 1 to the array
        else: # If line is false
            optionsArray.append(0) # Add 0 to the array
    f.close() # Close the file

    options = {
        'setName'     : optionsArray[0],
        'setColor'    : optionsArray[1],
        'setProtect'  : optionsArray[2],
        'setSeparator': optionsArray[3],
        'setIcon'     : optionsArray[4],
        'setLayer'    : optionsArray[5],
        'setCustom'   : optionsArray[6]
    }
    pass

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

def createFolderNull(name, selColor, selProtect, selSeparator, selIcon, selLayer, customColor):
    global hierarchy # Access to global dictionary (hierarchy)
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
        COL_BLUE:        c4d.Vector(float(3.0/255.0), float(169.0/255.0), float(244.0/255.0)),  # Blue
        COL_FUCHIA:      c4d.Vector(float(233.0/255.0), float(30.0/255.0), float(99.0/255.0)),  # Fuchia
        COL_GREEN:       c4d.Vector(float(76.0/255.0), float(175.0/255.0), float(80.0/255.0)),  # Green
        COL_ORANGE:      c4d.Vector(float(255.0/255.0), float(152.0/255.0), float(1.0/255.0)),  # Orange
        COL_SEANCE:      c4d.Vector(float(156.0/255.0), float(39.0/255.0), float(176.0/255.0)), # Seance
        COL_RED:         c4d.Vector(float(244.0/255.0), float(67.0/255.0), float(54.0/255.0)),  # Red
        COL_YELLOW:      c4d.Vector(float(255.0/255.0), float(193.0/255.0), float(7.0/255.0)),  # Yellow
        COL_DARK:        c4d.Vector(float(40.0/255.0), float(40.0/255.0), float(40.0/255.0)),   # Dark
        COL_BRIGHT:      c4d.Vector(float(180.0/255.0), float(180.0/255.0), float(180.0/255.0)),# Bright
        COL_DARKBLUE:    c4d.Vector(float(63.0/255.0), float(81.0/255.0), float(181.0/255.0)),  # Dark Blue
        COL_PURPLEHEART: c4d.Vector(float(103.0/255.0), float(58.0/255.0), float(183.0/255.0)), # Purple Heart
        COL_RANDOM:      randomColor, # Random color
        COL_CUSTOM:      customColor, # Custom color
        COL_NONE:        None         # No color
    }

    icons = {
        ICO_FOLDER: "1052837", # Folder
        ICO_OPEN:   "1052838", # Open folder
        ICO_CIRCLE: "17106",   # Circle
        ICO_STAR:   "170141",  # Star
        ICO_NULL:   "5140",    # Null
        ICO_BIN:    "12109"    # Trash can
    }

    color = colors[selColor] # Get selected color
    icon = icons[selIcon] # Get selected icon

    # Null object
    c4dver, c4dbuild = GetC4DVersion()

    null = c4d.BaseObject(c4d.Onull) # Initialize a null object
    null.SetName(name) # Set null object's name
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Display: None

    if (c4dver > 20):
        null[c4d.ID_BASELIST_ICON_FILE] = icon # Folder icon
        if color != None:
            null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Icon Color: Custom
            null[c4d.ID_BASELIST_ICON_COLOR] = color
        else:
            pass
    else:
        if color != None:
            null[c4d.NULLOBJECT_ICONCOL] = True
        else:
            pass

    if color != None:
        null[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color: On
        null[c4d.ID_BASEOBJECT_COLOR] = color

    # Protection tag
    if selProtect == True:
        protectionTag = c4d.BaseTag(5629) # Initialize a protection tag
        null.InsertTag(protectionTag) # Insert tag to the object

    if (selLayer != LAY_NONE):
        layerRoot = doc.GetLayerObjectRoot() # Get layer object root
        layer = c4d.documents.LayerObject() # Initialize a layer object
        layer.SetName(name) # Set layer's name
        if color != None:
            layer[c4d.ID_LAYER_COLOR] = color # Set layer's color
        layer.InsertUnder(layerRoot) # Insert layer to layer root
        doc.AddUndo(c4d.UNDOTYPE_NEW, layer) # Record undo for creating a new layer
        null[c4d.ID_LAYER_LINK] = layer # Set layer to the null

    # Separator tag
    if selSeparator == True:
        separatorTag = c4d.BaseTag(1022749) # Initialize a python tag
        separatorTag[c4d.TPYTHON_CODE] = separatorTagCode
        null.InsertTag(separatorTag) # Put the tag to the null
        CreateUserDataString(null, "Name", name) # Crete user data string input
        CreateUserDataCycle(null, "Style", 0, ['-', '=', '_', '~']) # Create user data cycle data
        CreateUserDataInteger(null, "Width", 40) # Create user data integer stuff
        separatorTag[c4d.ID_BASELIST_NAME] = "Separator"

    # Other stuff
    doc.AddUndo(c4d.UNDOTYPE_NEW, null) # Add undo command for creating a new object
    doc.InsertObject(null) # Insert null object to the document

    selection = doc.GetActiveObjects(0) # Get active selection
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
        c4dver, c4dbuild = GetC4DVersion()

        self.SetTitle("Create Folder Null") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, 1, 2) # Begin 'Mega1' group
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        # Inputs
        if (c4dver > 20):
            self.GroupBegin(GRP_MAIN, c4d.BFH_LEFT, 3, 1, "") # Begin 'Main' group
        else:
            self.GroupBegin(GRP_MAIN, c4d.BFH_LEFT, 2, 1, "") # Begin 'Main' group
        self.GroupBorderSpace(5, 3, 5, 3)
        #self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
        self.AddEditText(FOL_NAMEINPUT, c4d.BFH_LEFT, initw=250, inith=0)

        # Icon
        if (c4dver > 20):
            self.AddComboBox(FOL_ICONCB, c4d.BFH_LEFT, 50, 13)
            self.AddChild(FOL_ICONCB, ICO_FOLDER, " &i1052837&") # Closed folder
            self.AddChild(FOL_ICONCB, ICO_OPEN, " &i1052838&") # Open folder
            self.AddChild(FOL_ICONCB, ICO_CIRCLE, " &i17106&") # Circle
            self.AddChild(FOL_ICONCB, ICO_STAR, " &i170141&") # Start
            self.AddChild(FOL_ICONCB, ICO_NULL, " &i5140&") # Null
            self.AddChild(FOL_ICONCB, ICO_BIN, " &i12109&") # Thrash can

        # Color
        self.AddComboBox(FOL_COLORCB, c4d.BFH_LEFT, 80, 13)
        self.AddChild(FOL_COLORCB, COL_NONE, "None") # No Color
        self.AddChild(FOL_COLORCB, COL_CUSTOM, "Custom") # Custom
        self.AddChild(FOL_COLORCB, COL_RANDOM, "Random") # Random
        self.AddChild(FOL_COLORCB, COL_SEP, "") # Separator line
        self.AddChild(FOL_COLORCB, COL_BLUE, "Blue")
        self.AddChild(FOL_COLORCB, COL_DARKBLUE, "Dark Blue")
        self.AddChild(FOL_COLORCB, COL_FUCHIA, "Fuscia")
        self.AddChild(FOL_COLORCB, COL_GREEN, "Green")
        self.AddChild(FOL_COLORCB, COL_ORANGE, "Orange")
        self.AddChild(FOL_COLORCB, COL_SEANCE, "Seance")
        self.AddChild(FOL_COLORCB, COL_PURPLEHEART, "Purple")
        self.AddChild(FOL_COLORCB, COL_RED, "Red")
        self.AddChild(FOL_COLORCB, COL_YELLOW, "Yellow")
        self.AddChild(FOL_COLORCB, COL_DARK, "Dark")
        self.AddChild(FOL_COLORCB, COL_BRIGHT, "Bright")
        #
        self.GroupEnd() # End 'Main' group
        self.GroupBegin(GRP_ALT, c4d.BFH_FIT | c4d.BFH_LEFT, 4, 1, "") # Begin 'Alt' group
        #self.GroupBorderSpace(5, 0, 5, 5)
        self.GroupBegin(9000, c4d.BFH_RIGHT, 2, 1, "") # Begin 'Alt' group
        self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(5, 5, 5, 5)
        self.AddCheckbox(FOL_PROTECT, c4d.BFH_LEFT, 0, 13, "Protected")
        self.AddCheckbox(FOL_SEPARATOR, c4d.BFH_LEFT, 0, 13, "Separator")
        self.GroupEnd() # End 'Alt' group
        # Layers
        self.GroupBegin(9000, c4d.BFH_RIGHT, 2, 1, "") # Begin 'Alt' group
        self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(5, 3, 5, 3)
        self.AddStaticText(FOL_LAYERTEXT, c4d.BFH_RIGHT, 0, 13, "Layers", 0)
        self.AddComboBox(FOL_LAYERCB, c4d.BFH_RIGHT, 140, 13)
        self.AddChild(FOL_LAYERCB, LAY_NONE, "No Layer")
        self.AddChild(FOL_LAYERCB, LAY_FOLDER, "Folder Only")
        self.AddChild(FOL_LAYERCB, LAY_ADD, "Add Layer")
        self.AddChild(FOL_LAYERCB, LAY_OVER, "Overwrite Layer")
        self.AddChild(FOL_LAYERCB, LAY_AUTOTAG, "Autolayer Tag")
        self.GroupEnd() # End 'Alt' group
        self.GroupEnd() # End 'Alt' group

        # Set default options
        settings = loadSettings()
        self.SetString(FOL_NAMEINPUT, str(settings['setName']))
        self.SetInt32(FOL_COLORCB,    int(settings['setColor']))

        if (c4dver > 20):
            self.SetInt32(FOL_ICONCB,     int(settings['setIcon']))

        self.SetInt32(FOL_LAYERCB,    int(settings['setLayer']))
        self.SetBool(FOL_PROTECT,    int(settings['setProtect']))
        self.SetBool(FOL_SEPARATOR,  int(settings['setSeparator']))

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
        c4dver, c4dbuild = GetC4DVersion()
        bc = c4d.BaseContainer() # Initialize a base container

        name        = str(self.GetString(FOL_NAMEINPUT)) # Get name
        color       = int(self.GetInt32(FOL_COLORCB)) # Get color
        protect     = int(self.GetBool(FOL_PROTECT)) # Get protected
        separator   = int(self.GetBool(FOL_SEPARATOR)) # Get separator

        if (c4dver > 20):
            icon    = int(self.GetInt32(FOL_ICONCB)) # Get icon
        else:
            icon    = int(5005)

        layer       = int(self.GetInt32(FOL_LAYERCB)) # Get layer option

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            if (color == COL_CUSTOM):
                customColor = c4d.gui.ColorDialog(0, customColor)

            createFolderNull(name, color, protect, separator, icon, layer, customColor) # Run the main algorithm
            saveSettings(name, color, protect, separator, icon, layer, customColor)
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            if (color == COL_CUSTOM):
                customColor = c4d.gui.ColorDialog(0, customColor)
            createFolderNull(name, color, protect, separator, icon, layer, customColor) # Run the main algorithm
            saveSettings(name, color, protect, separator, icon, layer, customColor)
            self.Close() # Close dialog

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog