"""
AR_NodeResize

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_NodeResize
Version: 1.0.1
Description-US: Resize selected nodes, supports Xpresso and Redshift

Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.1 (19.10.2023) - Update for Cinema 4D 2024
1.0.0 (29.04.2022) - First version
"""

# Libraries
import c4d
import sys
try:
    import redshift
except:
    pass
from operator import attrgetter
from c4d import utils as u
from c4d import gui
from c4d.gui import GeDialog

# Variables
GRP_MEGA = 1000
GRP_MAIN = 1001
GRP_VAL  = 1002
GRP_BTNS = 1003

TXT_WIDTH = 3001
TXT_HEIGHT = 3002

EDIT_WIDTH = 4001
EDIT_HEIGHT = 4002

BTN_OK   = 2001
BTN_ADD   = 2003
BTN_CANCEL = 2002

options = [0,0,0]

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        global options

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw

        self.SetTitle("Resize Node") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MEGA, c4d.BFH_CENTER, cols=1, rows=1, groupflags=1, initw=300, inith=0)
        self.GroupBorderSpace(5, 5, 5, 5)
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, cols=2, rows=1, groupflags=1, initw=300, inith=0)

        self.AddStaticText(TXT_WIDTH, c4d.BFH_LEFT, name="Width")
        self.AddEditNumberArrows(EDIT_WIDTH, c4d.BFH_LEFT, initw=80, inith=13)
        self.SetFloat(EDIT_WIDTH, 65.0, min=0, max=sys.float_info.max, step=1.0)

        self.AddStaticText(TXT_WIDTH, c4d.BFH_LEFT, name="Height")
        self.AddEditNumberArrows(EDIT_HEIGHT, c4d.BFH_LEFT, initw=80, inith=13)
        self.SetFloat(EDIT_HEIGHT, 35.0, min=0, max=sys.float_info.max, step=1.0)

        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        # Buttons
        self.GroupBegin(GRP_BTNS, c4d.BFH_CENTER)
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Set") # Add button
        self.AddButton(BTN_ADD, c4d.BFH_LEFT, name="Add") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd()
        # ----------------------------------------------------------------------------------------
        self.GroupEnd()
        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global options

        doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
        bd = doc.GetActiveBaseDraw() # Get active basedraw
        bc = c4d.BaseContainer() # Initialize a base container

        # Actions here
        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == BTN_OK: # If 'Set' button is pressed
            options = [self.GetInt32(EDIT_WIDTH), self.GetInt32(EDIT_HEIGHT), 0]
            self.Close() # Close dialog
        if paramid == BTN_ADD: # If 'Add' button is pressed
            options = [self.GetInt32(EDIT_WIDTH), self.GetInt32(EDIT_HEIGHT), 1]
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            options = [self.GetInt32(EDIT_WIDTH), self.GetInt32(EDIT_HEIGHT), 0]
            self.Close() # Close dialog
        return True # Everything is fine

class nodeObject(object):
    def __init__(self, obj, px, py, sx, sy):
        self.node = obj # Node object
        self.px = px # X position
        self.py = py # Y position
        self.sx = sx # X scale
        self.sy = sy # Y scale

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
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

def ResizeNodes(nodeMaster, keyMod):
    global options

    dlg = Dialog() # Create dialog object
    dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 0, 0) # Open dialog

    nodes = [] # Initialize a list
    root = nodeMaster.GetRoot() # Get node master root
    for node in root.GetChildren(): # Iterate through nodes
        if node.GetBit(c4d.BIT_ACTIVE): # If node is selected
            bc  = node.GetDataInstance() # Get copy of base container
            bsc = bc.GetContainer(c4d.ID_SHAPECONTAINER) # Get copy of shape container
            bcd = bsc.GetContainer(c4d.ID_OPERATORCONTAINER) # Get copy of operator container
            px  = bcd.GetReal(100) # Get x position
            py  = bcd.GetReal(101) # Get y position
            sx  = bcd.GetReal(108) # Get x scale
            sy  = bcd.GetReal(109) # Get y scale
            nodes.append(nodeObject(node, px, py, sx, sy)) # Create nodeObject and add it to the list

    nodeMaster.AddUndo() # Add undo for changing nodes

    for i in range(0, len(nodes)): # Iterate through collected nodes
        node=  nodes[i].node # Get node
        bc  = node.GetDataInstance() # Get base container
        bsc = bc.GetContainerInstance(c4d.ID_SHAPECONTAINER) # Get shape container
        bcd = bsc.GetContainerInstance(c4d.ID_OPERATORCONTAINER) # Get operator container

        xSize = options[0]
        ySize = options[1]

        if options[0] != 0.0 or options[1] != 0.0:
            if options[2] == 0:
                bcd.SetReal(108, xSize) # Set x scale
                bcd.SetReal(109, ySize) # Set y scale
            else:
                bcd.SetReal(108, nodes[i].sx + xSize) # Add to x scale
                bcd.SetReal(109, nodes[i].sy + ySize) # Add to y scale

def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = GetKeyMod() # Get keymodifier
    doc.StartUndo() # Start recording undos
    materials = doc.GetMaterials() # Get materials
    selection = doc.GetSelection() # Get active selection
    #try: # Try to execute following script



    for s in selection: # Iterate through selection
        if type(s).__name__ == "XPressoTag": # If operator is xpresso tag
            xpnm = s.GetNodeMaster() # Get node master
            ResizeNodes(xpnm, keyMod) # Run the main function
    for m in materials: # Iterate through materials
        if m.GetBit(c4d.BIT_ACTIVE): # If material is selected
            rsnm = redshift.GetRSMaterialNodeMaster(m) # Get Redshift material node master
            ResizeNodes(rsnm, keyMod) # Run the main function
#except: # Otherwise
        #pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()