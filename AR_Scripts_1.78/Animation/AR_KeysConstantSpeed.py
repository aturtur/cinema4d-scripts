"""
AR_KeysConstantSpeed

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_KeysConstantSpeed
Version: 1.0.1
Description-US: Default: Modifies two selected keyframes' tangents so they are aligned. Shift: Break tangents.

Note: Use in 'Dope Sheet', doesn't work in 'F-Curve Mode'

Written for Maxon Cinema 4D R2024.1.0
Python version 3.11.4

Change log:
1.0.1 (17.01.2024) - Added some error checking
1.0.0 (08.12.2023) - First version
"""

# Libraries
import c4d
import os
import sys
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

def ConstantSpeed(keyMod):
    tracks = GetKeys() # Get selected keys
    for track in tracks: # Iterate through tracks

        keys = track[1]
        if len(keys) == 0:
            return False

        # Get keyframes
        keyA   = keys[0] # First keyframe
        keyB   = keys[1] # Second keyframe

        # Get and set keyframe A data
        curveA = keyA.GetCurve() # Get keyframe's curve

        keyA.SetInterpolation(curveA, c4d.CINTERPOLATION_SPLINE) # Set interpolation to spline
        keyA.ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_CLEAR) # Untick auto tangents
        keyA.ChangeNBit(c4d.NBIT_CKEY_CLAMP, c4d.NBITCONTROL_CLEAR) # Untick clamp tangents
        keyA.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_SET) # Lock key tangents length
        keyA.ChangeNBit(c4d.NBIT_CKEY_WEIGHTEDTANGENT, c4d.NBITCONTROL_CLEAR) # Untick weighted tangent
        keyA.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, c4d.NBITCONTROL_CLEAR) # Untick Remove overshoot
        keyA.ChangeNBit(c4d.NBIT_CKEY_AUTOWEIGHT, c4d.NBITCONTROL_CLEAR) # Untick Auto weight
    
        valueA = keyA.GetValue() # Get keyframe's value
        timeA  = keyA.GetTime().Get() # Get keyframe's time
        timeALeft = keyA.GetTimeLeft().Get() # Gets the time component of the left tangent of the key
        timeARight = keyA.GetTimeRight().Get() # Gets the time component of the right tangent of the key

        # Get and set keyframe B data
        curveB = keyB.GetCurve() # Get keyframe's curve

        keyB.SetInterpolation(curveB, c4d.CINTERPOLATION_SPLINE) # Set interpolation to spline
        keyB.ChangeNBit(c4d.NBIT_CKEY_AUTO, c4d.NBITCONTROL_CLEAR) # Untick auto tangents
        keyB.ChangeNBit(c4d.NBIT_CKEY_CLAMP, c4d.NBITCONTROL_CLEAR) # Untick clamp tangents
        keyB.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_SET) # Lock key tangents length
        keyB.ChangeNBit(c4d.NBIT_CKEY_WEIGHTEDTANGENT, c4d.NBITCONTROL_CLEAR) # Untick weighted tangent
        keyB.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, c4d.NBITCONTROL_CLEAR) # Untick Remove overshoot
        keyB.ChangeNBit(c4d.NBIT_CKEY_AUTOWEIGHT, c4d.NBITCONTROL_CLEAR) # Untick Auto weight

        valueB = keyB.GetValue() # Get keyframe's value
        timeB  = keyB.GetTime().Get() # Get keyframe's time
        timeBLeft = keyB.GetTimeLeft().Get() # Gets the time component of the left tangent of the key
        timeBRight = keyB.GetTimeRight().Get() # Gets the time component of the right tangent of the key

        # More stuff
        k = (valueB - valueA) / (timeB - timeA) # Calculate slope

        if keyMod == "Shift": # If shift pressed
            keyA.ChangeNBit(c4d.NBIT_CKEY_BREAK, c4d.NBITCONTROL_SET) # Break tangents for first keyframe
            keyB.ChangeNBit(c4d.NBIT_CKEY_BREAK, c4d.NBITCONTROL_SET) # Break tangents for second keyframe
        else:
            keyA.SetValueLeft(curveA, k * timeALeft) # Set left value for first keyframe
            keyB.SetValueRight(curveA, k * timeBRight) # Set right value for second keyframe

        keyA.SetValueRight(curveA, k * timeARight) # Set right value for first keyframe
        keyB.SetValueLeft(curveA, k * timeBLeft) # Set left value for second keyframe

        keyA.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_CLEAR) # Untick key tangents length
        keyB.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, c4d.NBITCONTROL_CLEAR) # Untick key tangents length

def main():
    doc.StartUndo() # Start recording undos
    #try: # Try to execute following script
    keyMod = GetKeyMod() # Get keymodifier
    ConstantSpeed(keyMod) # Do the thing
    #except: # If something went wrong
    #    pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D

# Execute main()
if __name__=='__main__':
    main()