"""
AR_KeysAlign

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_KeysAlign
Version: 1.0.0
Description-US: Default: Align selected keyframes to nearest whole frame

Note: Use in 'Dope Sheet', doesn't work in 'F-Curve Mode'

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.0 (29.04.2022) - First version
"""

# Libraries
import c4d
import math
from c4d import gui

# Functions
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

def AlignKeys():
    tracks = GetKeys() # Get selected keys
    fps = doc.GetFps()
    for track in tracks: # Iterate through tracks
        keys = track[1]
        for i, k in enumerate(keys): # Iterate through keys
            curve = k.GetCurve() # Get the curve
            frame = k.GetTime().Get() * fps # Get frame
            if frame % 1 >= 0.5: # If frame is closer to next whole frame than previous whole frame
                frame = round(frame)
            else: # Otherwise
                frame = math.floor(frame)
            index = curve.FindKey(k.GetTime())["idx"] # Get correct index
            curve.MoveKey(c4d.BaseTime(frame/fps), index, None, True, False) # Align keyframe
def main():
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        AlignKeys() # Do the thing
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()