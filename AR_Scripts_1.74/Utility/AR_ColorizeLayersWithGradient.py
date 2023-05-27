"""
AR_ColorizeLayersWithGradient

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ColorizeLayersWithGradient
Version: 1.0.1
Description-US: Colorizes selected layers with custom gradient

Written for Maxon Cinema 4D 2023.0.1
Python version 3.9.1

Change log:
1.0.1 (02.11.2022) - Fixed a bug
1.0.0 (02.11.2022) - Initial realease
"""

# Libraries
import c4d
from c4d.gui import GeDialog
from c4d.modules import render

GRP_MEGA        = 1000
GRP_MAIN        = 1001
GRP_BTNS        = 1002
GRP_VAL         = 1003
GRP_GRD         = 1004

TINT_VAL        = 2001
TINT_GRD        = 2002

GUI_GRD         = 3001

BTN_OK          = 7001
BTN_CANCEL      = 7002

# Classes
class Dialog(GeDialog):
    def __init__(self):
        self._customGradient = None
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw

        self.SetTitle("Colorize Layers with Gradient") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupBegin(GRP_VAL, c4d.BFH_LEFT | c4d.BFH_SCALEFIT, cols=1, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupEnd()
        
        bc = c4d.BaseContainer()
        self._customGradient = self.AddCustomGui(GUI_GRD, c4d.CUSTOMGUI_GRADIENT, "Gradient", c4d.BFH_CENTER, 500, 0, bc)
        defaultGrad = c4d.Gradient()
        defaultGrad.InsertKnot(c4d.Vector(0,0,1), 1, 0, 0.5, 0)
        defaultGrad.InsertKnot(c4d.Vector(0,1,1), 1, 0.25, 0.5, 0)
        defaultGrad.InsertKnot(c4d.Vector(0,1,0), 1, 0.5, 0.5, 1)
        defaultGrad.InsertKnot(c4d.Vector(1,1,0), 1, 0.75, 0.5, 0)
        defaultGrad.InsertKnot(c4d.Vector(1,0,0), 1, 1, 0.5, 2)
        
        self._customGradient.SetGradient(defaultGrad) # Set gradient data
        
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS, c4d.BFH_CENTER)
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Ok") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()
        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bc = c4d.BaseContainer() # Initialize a base container
        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Accept' button is pressed
            grad = self._customGradient.GetGradient() # Get gradient data
            ColorizeWithGradient(grad) # Colorize objects
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            grad = self._customGradient.GetGradient() # Get gradient data
            ColorizeWithGradient(grad) # Colorize objects
            self.Close() # Close dialog
        return True # Everything is fine

# Functions
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

def ColorizeWithGradient(gradient):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    irs = render.InitRenderStruct()
    gradient.InitRender(irs)
    
    layers = CollectLayers()
    selectedLayers = []
    for l in layers:
        if l.GetBit(c4d.BIT_ACTIVE):
            selectedLayers.append(l)
            
    for i, s in enumerate(selectedLayers):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo command for changing something
        s[c4d.ID_LAYER_COLOR] = gradient.CalcGradientPixel(float(i)/float(len(selectedLayers)))
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
def main():
    dlg = Dialog() # Create dialog object
    dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog
    pass

# Execute the main function
if __name__ == '__main__':
    main()