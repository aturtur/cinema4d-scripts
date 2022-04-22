"""
AR_RandomColors

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RandomColors
Version: 1.0.1
Description-US: Sets random display color to selected object(s).

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

To do:
    Ctrl: Colors from selected palette

Change log:
1.0.1 (29.03.2022) - Support for R25
"""

# Libraries
import c4d
import random

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

def RandomValue():
    r = random.random() # Random float
    return r # Return random float value

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
            elif keyMod == "Ctrl":
                obj[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Set 'Display Color' to 'Off'
                color = CycleColors(i)
                obj[c4d.ID_BASEOBJECT_COLOR] = color
            elif keyMod == "Alt":
                obj[c4d.ID_BASEOBJECT_USECOLOR] = 0 # Set 'Display Color' to 'Off'
                obj[c4d.ID_BASEOBJECT_COLOR] = doc[c4d.DOCUMENT_DEFAULTMATERIAL_COLOR] # Set color to documents default object color
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()