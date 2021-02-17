"""
AR_SequenceTracks

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SequenceTracks
Version: 1.0
Description-US: DEFAULT: Sequences selected animation tracks. SHIFT: Set gap.
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

def MoveKeys(curve, shift=1):
    shift = c4d.BaseTime((1.0/doc.GetFps())*shift) # Get one frame in BaseTime
    keyCount = curve.GetKeyCount() # Get count of keyframes
    for i in range(0, keyCount): # Iterate through keyframe indicies
        oldTime = curve.GetKey(i).GetTime() # Get keyframe's current time
        newTime = oldTime + shift
        curve.MoveKey(newTime, i, None, True, False) # Move keyframe

def SequenceTracks(keyMod):
    tracks = GetTracks() # Get selected tracks
    prevTrack = tracks[0] # Get the first selected track
    prevOut = prevTrack.GetCurve().GetEndTime() # Get out time

    if keyMod == "None":
        gap = c4d.BaseTime(1.0/doc.GetFps())
    elif keyMod == "Shift":
        inp = gui.InputDialog('Gap') # Store user given value
        gap = c4d.BaseTime(1.0/doc.GetFps()*float(inp)) # Gap
    elif keyMod == "Ctrl":
        tracks.reverse()
        gap = c4d.BaseTime(1.0/doc.GetFps())
    elif keyMod == "Ctrl+Shift":
        tracks.reverse()
        inp = gui.InputDialog('Gap') # Store user given value
        gap = c4d.BaseTime(1.0/doc.GetFps()*float(inp)) # Gap

    for i in range(1, len(tracks)): # Iterate through tracks
        curve = tracks[i].GetCurve() # Get current curve
        startTime = curve.GetStartTime()
        endTime = curve.GetEndTime()
        sub = prevOut - (startTime-gap) # Get time subtraction
        if sub.Get() < 0: # If subtraction is negative
            sub = (startTime-gap) - prevOut # New subtraction
            for i in range(0, sub.GetFrame(doc.GetFps())):
                MoveKeys(curve, -1) # Move keys one frame to the left
        else: # Otherwise
            for i in range(0, sub.GetFrame(doc.GetFps())):
                MoveKeys(curve, 1) # Move keys one frame to the right
        prevOut = curve.GetEndTime() # Get new out time
        
def main():
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        keyMod = GetKeyMod() # Get keymodifier
        SequenceTracks(keyMod) # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()