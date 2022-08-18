"""
AR_TglGrid

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TglGrid
Version: 1.0.1
Description-US: Toggle grid visibility in viewport

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (07.10.2021) - Updated for R25, added keymodifier (shift) to toggle all viewports
"""

# Libraries
import c4d

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

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    keyMod = GetKeyMod() # Get keymodifier

    if keyMod == "None":
        bd = doc.GetActiveBaseDraw() # Get active basedraw
        bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] = not bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] # Toggle grid

    elif keyMod == "Shift":
        bdc = doc.GetBaseDrawCount() # Get count of basedraws
        for x in range(0, bdc): # Iterate through basedraws
            bd = doc.GetBaseDraw(x)
            bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] = not bd[c4d.BASEDRAW_DISPLAYFILTER_GRID] # Toggle grid in all viewports

# Execute main()
if __name__=='__main__':
    main()
    c4d.EventAdd()