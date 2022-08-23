"""
AR_KeysValueAdd

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_KeysValueAdd
Version: 1.0.0
Description-US: Default: Increases selected keyframe(s) value. Shift: Set the value. Ctrl: Increase is multiplied by 2.

Note: Use in 'Dope Sheet', doesn't work in 'F-Curve Mode'

Written for Maxon Cinema 4D R26.014
Python version 3.9.1

Change log:
1.0.0 (29.04.2022) - First version
"""

# Libraries
import c4d
import os
import sys
from c4d import storage
from c4d import gui

# Functions
def CheckFiles():
    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get C4D's preference folder path
    folder = os.path.join(folder, "aturtur") # Aturtur folder
    if not os.path.exists(folder): # If folder doesn't exist
        os.makedirs(folder) # Create folder
    fileName = "AR_KeysValue.txt" # File name
    filePath = os.path.join(folder, fileName) # File path
    if not os.path.isfile(filePath): # If file doesn't exist
        f = open(filePath,"w+")
        f.write("1.0") # Default settings
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

def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def IterateHierarchy():
    op = doc.GetFirstObject()
    while op is not None:
        yield op
        op = GetNextObject(op)

def IterateTracks():
    for op in IterateHierarchy():
        ctracks = op.GetCTracks()
        for track in op.GetCTracks():
            yield track

def GetTracks():
    tracks = []
    for track in IterateTracks():
        if track.GetNBit(c4d.NBIT_TL1_SELECT): # If track is selected in timeline
            tracks.append(track)
    return tracks

def GetKeys():
    tracks = []
    for track in IterateTracks():
        curve = track.GetCurve()
        if curve is None:
            continue
        keys = []
        for key_id in range(curve.GetKeyCount()):
            key = curve.GetKey(key_id)
            if key.GetNBit(c4d.NBIT_TL1_SELECT): # If key is selected in timeline
                keys.append(key)
        tracks.append([curve, keys])
    return tracks

def LoadValue():
    optionsFile = CheckFiles() # Get options file
    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile) # Open the file for reading
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"))
    value = float(f.readline()) # Get value from the file
    return value

def SaveValue(value):
    optionsFile = CheckFiles() # Get options file
    if (sys.version_info >= (3, 0)): # If Python 3 version (R23)
        f = open(optionsFile, 'w') # Open the file for writing
    else: # If Python 2 version (R21)
        f = open(optionsFile.decode("utf-8"), 'w') # Open the file for writing
    f.write(str(value)) # Write current value to file
    f.close() # Close file

def ChangeValue(keyMod, value):
    tracks = GetKeys() # Get selected keys
    fps = doc.GetFps()
    for track in tracks: # Iterate through tracks
        keys = track[1]
        for i, k in enumerate(keys): # Iterate through keys
            curve = k.GetCurve() # Get the curve
            oldValue = k.GetValue()
            if keyMod == "None":
                k.SetValue(curve, oldValue+value)
            elif keyMod == "Ctrl":
                k.SetValue(curve, oldValue+(value*2))

def main():
    doc.StartUndo() # Start recording undos
    #try: # Try to execute following script
    keyMod = GetKeyMod() # Get keymodifier
    value = LoadValue()
    if keyMod == "Shift":
        value = float(gui.InputDialog('Value', str(value))) # Store user given value
        SaveValue(value)
    ChangeValue(keyMod, value) # Do the thing
    #except: # If something went wrong
    #    pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()