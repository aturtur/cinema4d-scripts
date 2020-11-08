"""
AR_CreateFolderNull

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateFolderNull
Version: 1.0.1
Description-US: Creates a folder null for easier organizing.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.1 (07.11.2020) - Added support for Esc and Enter keys
"""
# Libraries
import c4d
from c4d.gui import GeDialog

# Global variables
hierarchy = {} # Initialize hierarchy dictionary
level = 0 # Initialize level variable (how deep object is in hierarchy)

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

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
    global hieararchy # Access to global dictionary (hierarchy)
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
    global hieararchy # Access to global dictionary (hierarchy)
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
                                print addRest, l+targetLevel
                                if c >= l + targetLevel: # If level match
                                    collection.append(i) # Add object to collection
                            else:
                                print addRest, l+targetLevel
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

def createFolderNull(name, selColor, selIcon):
    global hieararchy # Access to global dictionary (hierarchy)
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    keyMod = GetKeyMod() # Get key modifier
    doc.StartUndo() # Start recording undos
      
    # Choose color and icon
    colors = {
        4001: c4d.Vector(float(3.0/255.0), float(169.0/255.0), float(244.0/255.0)),  # Blue
        4002: c4d.Vector(float(233.0/255.0), float(30.0/255.0), float(99.0/255.0)),  # Fuchia
        4003: c4d.Vector(float(76.0/255.0), float(175.0/255.0), float(80.0/255.0)),  # Green
        4004: c4d.Vector(float(255.0/255.0), float(152.0/255.0), float(1.0/255.0)),  # Orange
        4005: c4d.Vector(float(156.0/255.0), float(39.0/255.0), float(176.0/255.0)), # Seance
        4006: c4d.Vector(float(244.0/255.0), float(67.0/255.0), float(54.0/255.0)),  # Red
        4007: c4d.Vector(float(255.0/255.0), float(193.0/255.0), float(7.0/255.0)),  # Yellow
        4008: c4d.Vector(float(40.0/255.0), float(40.0/255.0), float(40.0/255.0)),   # Dark
        4009: c4d.Vector(float(180.0/255.0), float(180.0/255.0), float(180.0/255.0)),# Bright
        4010: c4d.Vector(float(63.0/255.0), float(81.0/255.0), float(181.0/255.0)),  # Dark Blue
        4011: c4d.Vector(float(103.0/255.0), float(58.0/255.0), float(183.0/255.0))  # Purple Heart
    }

    icons = {
        5001: "1052837", # Folder
        5002: "1052838", # Open folder
        5003: "17106", # Circle
        5004: "170141", # Star
        5005: "5140", # Null
        5006: "12109" # Trash can
    }

    color = colors[selColor] # Get selected color
    icon = icons[selIcon] # Get selected icon
    
    # Null object
    null = c4d.BaseObject(c4d.Onull) # Initialize a null object
    null.SetName(name) # Set null object's name
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Display: None
    null[c4d.ID_BASELIST_ICON_FILE] = icon # Folder icon
    null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 1 # Icon Color: Custom
    null[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color: On
    null[c4d.ID_BASEOBJECT_COLOR] = color
    null[c4d.ID_BASELIST_ICON_COLOR] = color
    
    # Protection tag
    protectionTag = c4d.BaseTag(5629) # Initialize a protection tag
    null.InsertTag(protectionTag) # Insert tag to the object
    
    # Layer
    layerRoot = doc.GetLayerObjectRoot() # Get layer object root
    layer = c4d.documents.LayerObject() # Initialize a layer object
    layer.SetName(name) # Set layer's name
    layer[c4d.ID_LAYER_COLOR] = color # Set layer's color
    layer.InsertUnder(layerRoot) # Insert layer to layer root
    doc.AddUndo(c4d.UNDOTYPE_NEW, layer) # Record undo for creating a new layer
    null[c4d.ID_LAYER_LINK] = layer # Set layer to the null
    
    # Other stuff
    doc.AddUndo(c4d.UNDOTYPE_NEW, null) # Add undo command for creating a new object
    doc.InsertObject(null) # Insert null object to the document

    #if keyMod == "None":
    selection = doc.GetActiveObjects(0) # Get active selection
    if len(selection) != 0: # If there are selected objects
        null.InsertBefore(selection[0]) # Move null
        hierarchy = BuildHierarchy() # Build hierarchy
        for s in selection: # Iterate through selected objects
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for changing object
            mat = s.GetMg() # Get global matrix
            s.InsertUnder(null) # Move under the null object
            s.SetMg(mat) # Set global matrix
            s.DelBit(c4d.BIT_ACTIVE) # Deselect object
            if keyMod == "Shift": # If shift-key is pressed down
                objectLayer = s.GetLayerObject(doc) # Get object's layer
                if objectLayer == None: # If object does not already have a layer
                    s[c4d.ID_LAYER_LINK] = layer # Set layer to the object

                children = FindChildren(s, 0, True) # Get children
                for child in children: # Iterate through children
                    objectLayer = child.GetLayerObject(doc) # Get object's layer
                    if objectLayer == None: # If object does not already have a layer
                        child[c4d.ID_LAYER_LINK] = layer # Set layer to the object

            if keyMod == "Ctrl": # If control-key is pressed down
                s[c4d.ID_LAYER_LINK] = layer # Set layer to the object
                children = FindChildren(s, 0, True)
                for child in children:
                    child[c4d.ID_LAYER_LINK] = layer # Set layer to the object

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
        self.SetTitle("Create Folder Null") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1000, c4d.BFH_CENTER, 2, 1) # Begin 'Mega1' group
        # ----------------------------------------------------------------------------------------
        # Inputs
        self.GroupBegin(1002, c4d.BFH_RIGHT, 4, 1, "") # Begin 'Main' group
        self.GroupBorder(c4d.BORDER_NONE)
        self.GroupBorderNoTitle(c4d.BORDER_NONE)
        self.GroupBorderSpace(5, 5, 5, 5)
        self.AddStaticText(3000, c4d.BFH_LEFT, 0, 0, "Name", 0)
        self.AddEditText(3001, c4d.BFH_LEFT, initw=250, inith=0)

        self.AddComboBox(3006, c4d.BFH_LEFT, 50, 13)
        self.AddChild(3006, 5001, " &i1052837&") # Closed folder
        self.AddChild(3006, 5002, " &i1052838&") # Open folder
        self.AddChild(3006, 5003, " &i17106&") # Circle
        self.AddChild(3006, 5004, " &i170141&") # Start
        self.AddChild(3006, 5005, " &i5140&") # Null
        self.AddChild(3006, 5006, " &i12109&") # Thrash can

        self.AddComboBox(3003, c4d.BFH_LEFT, 80, 13)
        self.AddChild(3003, 4001, "Blue")
        self.AddChild(3003, 4010, "Dark Blue")
        self.AddChild(3003, 4002, "Fuscia")
        self.AddChild(3003, 4003, "Green")
        self.AddChild(3003, 4004, "Orange")
        self.AddChild(3003, 4005, "Seance")
        self.AddChild(3003, 4011, "Purple")
        self.AddChild(3003, 4006, "Red")
        self.AddChild(3003, 4007, "Yellow")
        self.AddChild(3003, 4008, "Dark")
        self.AddChild(3003, 4009, "Bright")

        self.SetString(3001, "Null") # Default
        self.SetInt32(3003, 4001) # Default color
        self.SetInt32(3006, 5001) # Default icon

        self.GroupEnd() # End 'Resolution' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Mega1' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1005, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(3004, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(3005, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End 'Buttons' group

        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        bc = c4d.BaseContainer() # Initialize a base container

        # Actions here
        if paramid == 3005: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == 3004: # If 'Accept' button is pressed
            name  = str(self.GetString(3001)) # Get name
            color = int(self.GetInt32(3003)) # Get color
            icon = int(self.GetInt32(3006)) # Get icon
            createFolderNull(name, color, icon) # Run the main algorithm
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            name  = str(self.GetString(3001)) # Get name
            color = int(self.GetInt32(3003)) # Get color
            icon = int(self.GetInt32(3006)) # Get icon
            createFolderNull(name, color, icon) # Run the main algorithm
            self.Close() # Close dialog

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -2, -2, 100, 50) # Open dialog