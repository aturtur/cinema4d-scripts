"""
AR_KeysSetPosX

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_KeysSetPosY
Version: 1.0.0
Description-US: Sets Position Y keyframe for selected object(s) to current time with current value

Written for Maxon Cinema 4D 2023.1.3
Python version 3.9.1

Change log:
1.0.0 (10.01.2023) - Initial realease
"""

# Libraries
import c4d

# Functions
def SetKeyframe(obj, param, value):
    track = obj.FindCTrack(param) # Find CTrack
    if track == None: # If there's no CTrack
        track = c4d.CTrack(obj, param) # Init CTrack
        obj.InsertTrackSorted(track) # And insert it to the object
        
    curve = track.GetCurve() # Get curve
    fps = doc.GetFps() # Get Frame Rate
    frame = doc.GetTime().GetFrame(fps) # Get current frame
    currentTime = c4d.BaseTime(frame, fps) # Get current time
    key = curve.AddKey(currentTime)["key"] # Init key
    track.FillKey(doc, obj, key) # Set key
    
    # Set key interpolation
    if doc[c4d.TLWORLD_INTER] == 1: # If animation interpolation is set to 'Spline'
        key.SetInterpolation(curve, c4d.CINTERPOLATION_SPLINE)
        key.ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_SET)
        key.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, c4d.NBITCONTROL_SET)
        key.ChangeNBit(c4d.NBIT_CKEY_CLAMP, c4d.NBITCONTROL_SET)

def main():
    doc.StartUndo() # Start recording undos
    
    p = c4d.ID_BASEOBJECT_REL_POSITION # Position
    a = c4d.VECTOR_Y                   # Y-axis
    
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Iterate through selection
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, s) # Add undo for inserting key    
        SetKeyframe(s, [p, a], s[p,a]) # Set keyframe

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    pass

# Execute main
if __name__ == '__main__':
    main()