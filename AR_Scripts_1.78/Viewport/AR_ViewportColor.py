"""
AR_ViewportColor

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ViewportColor
Version: 1.2.0
Description-US: Changes the viewport backgound color

Note: The change is permanent

Written for Maxon Cinema 4D R26.107
Python version 3.9.1

Change log:
1.2.0 (27.02.2023) - More presets, async GeDialog instead of modal
1.1.0 (08.11.2022) - Dialog for preset selection
1.0.0 (23.08.2022) - Initial version
"""

# Libraries
import c4d, os
from c4d import storage
from c4d import gui
from c4d.gui import GeDialog

# Global variables
GRP_PRESETS     = 1000
GRP_BTN         = 1001

LBL_PRESETS     = 1002
PRESET_SEP      = 1004

CMB_PRESETS     = 2000

BTN_OK          = 7001
BTN_CANCEL      = 7002

currentPreset   = c4d.GetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND) # Get current viewport background color
presets         = [[currentPreset, "Current"], [c4d.Vector(0,0,0), ""]]

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        self.res = c4d.BaseContainer()

    # Create Dialog
    def CreateLayout(self):
        global presets

        self.SetTitle("Change Viewport Color") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_PRESETS, c4d.BFH_CENTER, 2, 1) # Begin 'Mega1' group
        self.GroupBorderSpace(10, 5, 5, 10)
        # ----------------------------------------------------------------------------------------
        # Presets
        self.AddStaticText(LBL_PRESETS, c4d.BFH_LEFT, 0, 0, "Preset")
        self.AddComboBox(CMB_PRESETS, c4d.BFH_LEFT, 0, 13)

        presetBase = 3000 # ID base for preset items
        optionsFile = CheckFiles() # Get options file
        presets = GeneratePresetArray(optionsFile) # Get presets array
        for i, preset in enumerate(presets):
            presetId = i # Current preset ID
            self.AddChild(CMB_PRESETS, presetId, presets[presetId][1]) # Fill preset    
        self.SetInt32(CMB_PRESETS, int(0)) # Set default option
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Presets' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(GRP_BTN, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        self.GroupBorderSpace(10, 0, 5, 10)
        # Buttons
        self.AddButton(BTN_OK, c4d.BFH_LEFT, name="Ok") # Add button
        self.AddButton(BTN_CANCEL, c4d.BFH_RIGHT, name="Cancel") # Add button
        self.GroupEnd() # End 'Buttons' group

        return True

    # Processing
    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global presets
        global currentPreset

        bc = c4d.BaseContainer() # Initialize a base container
        selectedPreset = self.GetInt32(CMB_PRESETS) # Get the choosen preset

        # Actions here
        if paramid == CMB_PRESETS: # If 'Preset' changed
            ChangeViewportColor(presets[selectedPreset][0])
            pass

        if paramid == BTN_CANCEL: # If 'Cancel' button is pressed
            ChangeViewportColor(currentPreset)
            self.Close() # Close dialog

        if paramid == BTN_OK: # If 'Accept' button is pressed
            ChangeViewportColor(presets[selectedPreset][0])
            self.Close() # Close dialog

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ESC, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            ChangeViewportColor(currentPreset)
            self.Close()

        c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD, c4d.KEY_ENTER, bc)
        if bc[c4d.BFM_INPUT_VALUE]:
            ChangeViewportColor(presets[selectedPreset][0])
            self.Close() # Close dialog

        return True

# Functions
def ChangeViewportColor(color):
    c4d.SetViewColor(c4d.VIEWCOLOR_C4DBACKGROUND, color)
    c4d.EventAdd() # Refresh C4D

def GeneratePresetArray(filePath):
    global presets

    f = open(filePath, "r")
    lines = f.readlines()
    for line in lines:
        split = line.split("#") # Split line
        color = hex_to_rgb(split[0].strip()) # Get color code
        name  = split[1].strip() # Get preset name
        presets.append([color, name]) # Add to presets list
    return presets

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

def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_ViewportColor.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("000000 # Black\n333333 # C4D 2023\n424242 # C4D R21\n767676 # C4D R20\n91a3a9 # Houdini\n4a545e # Maya\n5c666b # Modo") # Default value
        f.close()
    return filePath

def Prefs(id):
    return c4d.plugins.FindPlugin(id, c4d.PLUGINTYPE_PREFS)

def hex_to_rgb(value):
    lv = len(value)
    rgb = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    return c4d.Vector(float(rgb[0])/255,float(rgb[1])/255,float(rgb[2])/255)

#def main():
keyMod = GetKeyMod() # Get keymodifier
# Put 'Background Gradient' off, if it's on
if Prefs(465001625)[c4d.PREF_VIEW_DISPLAYFILTER_GRADIENT] == True:
    Prefs(465001625)[c4d.PREF_VIEW_DISPLAYFILTER_GRADIENT] = False

# Open the dialog
if keyMod == "Alt+Ctrl+Shift":
    optionsFile = CheckFiles() # Get options file
    storage.GeExecuteFile(optionsFile) # Open options file for editing
    pass
else:
    dlg = Dialog() # Create dialog object
    #dlg.Open(c4d.DLG_TYPE_MODAL_RESIZEABLE, 0, -1, -1, 0, 0) # Open dialog
    dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -1, -1, 0, 0) # Open dialog

# Execute main()
#if __name__=='__main__':
#    main()