"""
AR_RandomColors

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RandomColors
Version: 1.1.0
Description-US: Sets random display color to selected object(s)

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.1.0 (08.11.2022) - Added feature to use custom gradient
1.0.1 (29.03.2022) - Support for R25
1.0.0 (10.04.2021) - Initial release
"""

# Libraries
import c4d
import random
from c4d.gui import GeDialog
from c4d.modules import render

# Global variables
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

        self.SetTitle("Colorize with Gradient") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupBegin(GRP_VAL, c4d.BFH_LEFT | c4d.BFH_SCALEFIT, cols=1, rows=1, groupflags=1, initw=500, inith=0)
        self.GroupEnd()
        
        bc = c4d.BaseContainer()
        self._customGradient = self.AddCustomGui(GUI_GRD, c4d.CUSTOMGUI_GRADIENT, "Gradient", c4d.BFH_CENTER, 500, 0, bc)
        
        # Default gradient
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
def ColorizeWithGradient(gradient):
    irs = render.InitRenderStruct()
    gradient.InitRender(irs)
    selection = doc.GetActiveObjects(1) # Get object selection
    random.shuffle(selection)
    for i, obj in enumerate(selection): # Iterate through selected objects
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj) # Record undo
        obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color = On
        #color = c4d.Vector(RandomValue(), RandomValue(), RandomValue()) # Get random color

        obj[c4d.ID_BASEOBJECT_COLOR] = gradient.CalcGradientPixel(float(i)/float(len(selection)))
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D


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

def RandomValue():
    r = random.random() # Random float
    return r # Return random float value

"""
def CycleColors(i):
    colors = [c4d.Vector(244.0/255.0, 67.0/255.0, 54.0/255.0),
              c4d.Vector(233.0/255.0, 30.0/255.0, 99.0/255.0),
              c4d.Vector(156.0/255.0, 39.0/255.0, 176.0/255.0),
              c4d.Vector(103.0/255.0, 58.0/255.0, 183.0/255.0),
              c4d.Vector(63.0/255.0, 81.0/255.0, 181.0/255.0),
              c4d.Vector(33.0/255.0, 150.0/255.0, 243.0/255.0),
              c4d.Vector(3.0/255.0, 169.0/255.0, 244.0/255.0),
              c4d.Vector(1.0/255.0, 188.0/255.0, 212.0/255.0),
              c4d.Vector(1.0/255.0, 150.0/255.0, 136.0/255.0),
              c4d.Vector(76.0/255.0, 175.0/255.0, 80.0/255.0),
              c4d.Vector(139.0/255.0, 195.0/255.0, 74.0/255.0),
              c4d.Vector(205.0/255.0, 220.0/255.0, 57.0/255.0),
              c4d.Vector(255.0/255.0, 235.0/255.0, 59.0/255.0),
              c4d.Vector(255.0/255.0, 197.0/255.0, 7.0/255.0),
              c4d.Vector(255.0/255.0, 152.0/255.0, 1.0/255.0),
              c4d.Vector(255.0/255.0, 87.0/255.0, 34.0/255.0)]
    return colors[i % len(colors)]
"""

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    try: # Try to execute following script
        selection = doc.GetActiveObjects(1) # Get object selection
        for i, obj in enumerate(selection): # Iterate through selected objects
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_NOCHILDREN, obj) # Record undo
            if keyMod == "None":
                obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color = On
                color = c4d.Vector(RandomValue(), RandomValue(), RandomValue()) # Get random color
                obj[c4d.ID_BASEOBJECT_COLOR] = color # Random color
            elif keyMod == "Shift":
                obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Display Color = On
                color = c4d.Vector(RandomValue()) # Random grey
                obj[c4d.ID_BASEOBJECT_COLOR] = color # Set random color
            #elif keyMod == "Ctrl":
            #    obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Set 'Display Color' to 'Off'
            #    color = CycleColors(i)
            #    obj[c4d.ID_BASEOBJECT_COLOR] = color
            elif keyMod == "Alt":
                obj[c4d.ID_BASEOBJECT_USECOLOR] = 0 # Set 'Display Color' to 'Off'
                obj[c4d.ID_BASEOBJECT_COLOR] = doc[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR] # Set color to documents default object color

        if keyMod == "Ctrl":
            dlg = Dialog() # Create dialog object
            dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog
            pass

    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()