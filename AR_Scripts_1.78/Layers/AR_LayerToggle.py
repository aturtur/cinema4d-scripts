"""
AR_LayerToggle

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_LayerToggle
Version: 1.1.0
Description-US: Toggle layer options

Written for Maxon Cinema 4D 2024.2.0
Python version 3.11.4

Change log:
1.1.0 (20.02.2024) - Added support for undos
1.0.0 (22.12.2023) - Initial realease
"""

# Libraries
import c4d
from c4d import utils as u
from c4d.gui import GeDialog
from c4d import storage
import os

GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002
GRP_VAL         = 1003
GRP_GRD         = 1004

CHK_SOLO        = 2000
CHK_EDITOR      = 2001
CHK_RENDER      = 2002
CHK_MANAGER     = 2003
CHK_LOCK        = 2004
CHK_ANIMATION   = 2005
CHK_GENERATORS  = 2006
CHK_DEFORMERS   = 2007
CHK_EXPRESSIONS = 2008
CHK_XREFS       = 2009

BTN_OK          = 7001
BTN_CANCEL      = 7002

defaultSettings = "0\n1\n1\n0\n0\n1\n1\n1\n1\n1"

# Classes
class Dialog(GeDialog):
    def __init__(self):
        self._customGradient = None
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document

        global settings
        settings = loadSettings()

        self.SetTitle("Layer Settings") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=250, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=250, inith=0)

        self.AddCheckbox(CHK_SOLO,          c4d.BFH_LEFT, 100, 10, "Solo") # Solo
        self.AddCheckbox(CHK_EDITOR,        c4d.BFH_LEFT, 100, 10, "Editor") # Editor
        self.AddCheckbox(CHK_RENDER,        c4d.BFH_LEFT, 100, 10, "Render") # Render
        self.AddCheckbox(CHK_MANAGER,       c4d.BFH_LEFT, 100, 10, "Object Manager") # Object Manager
        self.AddCheckbox(CHK_LOCK,          c4d.BFH_LEFT, 100, 10, "Lock") # Lock
        self.AddCheckbox(CHK_ANIMATION,     c4d.BFH_LEFT, 100, 10, "Animation") # Animation
        self.AddCheckbox(CHK_GENERATORS,    c4d.BFH_LEFT, 100, 10, "Generators") # Generators
        self.AddCheckbox(CHK_DEFORMERS,     c4d.BFH_LEFT, 100, 10, "Deformers") # Deformers
        self.AddCheckbox(CHK_EXPRESSIONS,   c4d.BFH_LEFT, 100, 10, "Expressions") # Expressions
        self.AddCheckbox(CHK_XREFS,         c4d.BFH_LEFT, 100, 10, "Xrefs") # Xrefs

        self.SetInt32(CHK_SOLO,        settings['solo'])
        self.SetInt32(CHK_EDITOR,      settings['editor'])
        self.SetInt32(CHK_RENDER,      settings['render'])
        self.SetInt32(CHK_MANAGER,     settings['manager'])
        self.SetInt32(CHK_LOCK,        settings['locked'])
        self.SetInt32(CHK_ANIMATION,   settings['animation'])
        self.SetInt32(CHK_GENERATORS,  settings['generators'])
        self.SetInt32(CHK_DEFORMERS,   settings['deformers'])
        self.SetInt32(CHK_EXPRESSIONS, settings['expressions'])
        self.SetInt32(CHK_XREFS,       settings['xfers'])

        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS,  c4d.BFH_CENTER)
        self.AddButton(BTN_OK,     c4d.BFH_LEFT,  name="Ok") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()
        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global settings

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bc = c4d.BaseContainer() # Initialize a base container

        settings = [str(int(self.GetInt32(CHK_SOLO))),
            str(int(self.GetInt32(CHK_EDITOR))),
            str(int(self.GetInt32(CHK_RENDER))),
            str(int(self.GetInt32(CHK_MANAGER))),
            str(int(self.GetInt32(CHK_LOCK))),
            str(int(self.GetInt32(CHK_ANIMATION))),
            str(int(self.GetInt32(CHK_GENERATORS))),
            str(int(self.GetInt32(CHK_DEFORMERS))),
            str(int(self.GetInt32(CHK_EXPRESSIONS))),
            str(int(self.GetInt32(CHK_XREFS)))
        ]

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            saveSettings(settings) # Save settings
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            saveSettings(settings) # Save settings
            self.Close() # Close dialog
        return True # Everything is fine

# Functions
def loadSettings():
    optionsFile = CheckFiles()
    f = open(optionsFile) # Open the file for reading
    optionsArray = [] # Initialize an array for options
    for line in f: # Iterate through every row
        line = line.rstrip('\n') # Strip newline stuff
        optionsArray.append(line)
    f.close() # Close the file
    options = {
        'solo':        int(optionsArray[0]),
        'editor':      int(optionsArray[1]),
        'render':      int(optionsArray[2]),
        'manager':     int(optionsArray[3]),
        'locked':        int(optionsArray[4]),
        'animation':   int(optionsArray[5]),
        'generators':  int(optionsArray[6]),
        'deformers':   int(optionsArray[7]),
        'expressions': int(optionsArray[8]),
        'xfers':       int(optionsArray[9])
    }
    return options

def saveSettings(settings):
    optionsFile = CheckFiles() #
    f = open(optionsFile, 'w') # Open the file for writing
    settings = "\n".join(settings) # Create a string from an array
    f.write(settings) # Write settings to the file
    f.close() # Close the file
    return True # Everything is fine

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_LayersSettings.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write(defaultSettings) # Default settings
        f.close()
    return filePath

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

def GetNextItem(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectLayers():
    def IterateLayers(op):
        layerList = [] # Initialize an array for collecting layers
        if op is None: # If there is no layer
            return # This is over
        while op: # While there is an item
            layerList.append(op) # Add layer to layer list
            op = GetNextItem(op) # Get next layer
        return layerList # Return layers

    doc = c4d.documents.GetActiveDocument() # Get active document
    layerRoot = doc.GetLayerObjectRoot() # Get layer object root
    layers = layerRoot.GetChildren() # Get layers
    if layers == []: # Check if there is no any layer
        return None # Return none
    else: # If there is any layer
        startLayer = layers[0] # Get start layer for iterating through all layers
        return IterateLayers(startLayer) # Return collection of all layers

def LayerToggle(settings):

    doc = c4d.documents.GetActiveDocument() # Get the active Cinema 4D document
    doc.StartUndo() # Start recording undos

    layers = CollectLayers() # Collect layers
    selectedLayers = [l for l in layers if l.GetBit(c4d.BIT_ACTIVE)] # Filter for selected layers

    if len(selectedLayers) == 0: # If no layers are selected
        for s in layers: # Iterate through all layers
            
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo step
            
            if settings['solo'] == 1:
                s[c4d.ID_LAYER_SOLO] = not s[c4d.ID_LAYER_SOLO]
            if settings['editor'] == 1:
                s[c4d.ID_LAYER_VIEW] = not s[c4d.ID_LAYER_VIEW]
            if settings['render'] == 1:
                s[c4d.ID_LAYER_RENDER] = not s[c4d.ID_LAYER_RENDER]
            if settings['manager'] == 1:
                s[c4d.ID_LAYER_MANAGER] = not s[c4d.ID_LAYER_MANAGER]
            if settings['animation'] == 1:
                s[c4d.ID_LAYER_ANIMATION] = not s[c4d.ID_LAYER_ANIMATION]
            if settings['generators'] == 1:
                s[c4d.ID_LAYER_GENERATORS] = not s[c4d.ID_LAYER_GENERATORS]
            if settings['deformers'] == 1:
                s[c4d.ID_LAYER_DEFORMERS] = not s[c4d.ID_LAYER_DEFORMERS]
            if settings['expressions'] == 1:
                s[c4d.ID_LAYER_EXPRESSIONS] = not s[c4d.ID_LAYER_EXPRESSIONS]
            if settings['locked'] == 1:
                s[c4d.ID_LAYER_LOCKED] = not s[c4d.ID_LAYER_LOCKED]
            if settings['xfers'] == 1:
                s[c4d.ID_LAYER_XREF] = not s[c4d.ID_LAYER_XREF]

    for i, s in enumerate(selectedLayers): # For selected layers
        
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo step
        
        if settings['solo'] == 1:
            s[c4d.ID_LAYER_SOLO] = not s[c4d.ID_LAYER_SOLO]
        if settings['editor'] == 1:
            s[c4d.ID_LAYER_VIEW] = not s[c4d.ID_LAYER_VIEW]
        if settings['render'] == 1:
            s[c4d.ID_LAYER_RENDER] = not s[c4d.ID_LAYER_RENDER]
        if settings['manager'] == 1:
            s[c4d.ID_LAYER_MANAGER] = not s[c4d.ID_LAYER_MANAGER]
        if settings['animation'] == 1:
            s[c4d.ID_LAYER_ANIMATION] = not s[c4d.ID_LAYER_ANIMATION]
        if settings['generators'] == 1:
            s[c4d.ID_LAYER_GENERATORS] = not s[c4d.ID_LAYER_GENERATORS]
        if settings['deformers'] == 1:
            s[c4d.ID_LAYER_DEFORMERS] = not s[c4d.ID_LAYER_DEFORMERS]
        if settings['expressions'] == 1:
            s[c4d.ID_LAYER_EXPRESSIONS] = not s[c4d.ID_LAYER_EXPRESSIONS]
        if settings['locked'] == 1:
            s[c4d.ID_LAYER_LOCKED] = not s[c4d.ID_LAYER_LOCKED]
        if settings['xfers'] == 1:
            s[c4d.ID_LAYER_XREF] = not s[c4d.ID_LAYER_XREF]

    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Update Cinema 4D

def main():
    keyMod = GetKeyMod() # Get key modifier
    if keyMod == "None": # If no key modifier
        settings = loadSettings() # Load settings
        LayerToggle(settings)
    elif keyMod == "Alt+Ctrl+Shift": # If key modifier ALT + CTRL + SHIFT
        dlg = Dialog() # Create dialog object
        dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog

# Execute the main function
if __name__ == '__main__':
    main()