"""
AR_TracksRemap

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TracksRemap
Version: 1.0.1
Description-US: Adds Time track for selected tracks for time remapping


Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (26.04.2022) - Bug fix
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

def SequenceTimeRemap(keyMod):
    tracks = GetTracks() # Get selected tracks
    null = c4d.BaseObject(c4d.Onull) # Init a null object
    null.SetName("Time Remap") # Set null's name
    doc.InsertObject(null, checknames=True) # Insert the null object to document
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null) # Record undo for adding a new object
    desc = c4d.DescID(c4d.DescLevel(c4d.CTtime, c4d.CTtime, 0))
    timeTrack = c4d.CTrack(null, desc) # Initialize a Time Track
    null.InsertTrackSorted(timeTrack) # Insert the time track to the object

    fps = doc.GetFps() # Get document's FPS

    minStartTime = tracks[0].GetCurve().GetStartTime().GetFrame(fps) # Init min start time variable
    maxEndTime = tracks[0].GetCurve().GetEndTime().GetFrame(fps) # Init max start time variable

    for i in range(0, len(tracks)): # Iterate through tracks
        curve = tracks[i].GetCurve() # Get current curve

        startTime = curve.GetStartTime().GetFrame(fps)
        endTime = curve.GetEndTime().GetFrame(fps)

        if startTime < minStartTime:
            minStartTime = minStartTime
        if endTime > maxEndTime:
            maxEndTime = endTime

    curve = timeTrack.GetCurve() # Get Curve of the CTrack
    #currentTime = c4d.BaseTime(frame, fps) # Get current time
    firstKey = curve.AddKey(c4d.BaseTime(minStartTime/fps))["key"]
    timeTrack.FillKey(doc, null, firstKey)
    firstKey.SetValue(curve, 0)

    lastKey = curve.AddKey(c4d.BaseTime(maxEndTime/fps))["key"]
    timeTrack.FillKey(doc, null, lastKey)
    lastKey.SetValue(curve, 1)

    for i in range(0, len(tracks)): # Iterate through tracks
        tracks[i][c4d.ID_CTRACK_TIME] = timeTrack
        if keyMod == "None":
            tracks[i][c4d.ID_CTRACK_TIME_RELATIVE] = False
        elif keyMod == "Shift":
            tracks[i][c4d.ID_CTRACK_TIME_RELATIVE] = True

def main():
    doc.StartUndo() # Start recording undos
    #try: # Try to execute following script
    keyMod = GetKeyMod() # Get keymodifier
    SequenceTimeRemap(keyMod) # Do the thing
    #except: # If something went wrong
    #    pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
# Execute main()
if __name__=='__main__':
    main()



#[c4d.ID_CTRACK_TIME]