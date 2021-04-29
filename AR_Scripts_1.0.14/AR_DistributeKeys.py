"""
AR_DistributeKeys

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_DistributeKeys
Version: 1.0
Description-US: DEFAULT: Distributes selected keyframes evenly. SHIFT: Give step (in frames) to distribute.
Note: Select whole tracks, not only keyframes!

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""

# Libraries
import c4d
from c4d import gui

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

def DistributeKeys(keyMod, step):
    tracks = GetKeys() # Get selected keys
    for track in tracks:
        keys = track[1]
        for i, k in enumerate(keys): # Iterate through tracks
            curve = k.GetCurve() # Get the curve
            firstKeyTime = keys[0].GetTime().Get()
            lastKeyTime = keys[-1].GetTime().Get()
            if i != 0: # If not first run
                if keyMod == "None":
                    time = firstKeyTime + (lastKeyTime - firstKeyTime) / (len(keys)-1) * (i) # Distribution algorithm
                elif keyMod == "Shift":
                    time = firstKeyTime + float(step)/doc.GetFps() * (i) # Distribution algorithm
                index = curve.FindKey(k.GetTime())["idx"] # Get correct index
                curve.MoveKey(c4d.BaseTime(time), index, None, True, False) # Move keyframe        
def main():
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        keyMod = GetKeyMod() # Get keymodifier
        inp = 0
        if keyMod == "Shift":
            inp = int(gui.InputDialog('Step')) # Store user given value
        DistributeKeys(keyMod, inp) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()