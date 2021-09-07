"""
AR_EasePaste

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_EasePaste
Version: 1.0.1
Description-US: Pastes copied easing to selected keyframes. If you use F-Curve editor hold SHIFT when running the script.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

Change log:
1.0.1 (09.10.2020) - Major bug fix
"""
# Libraries
import c4d
import os
import csv

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

def GetKeys(keyMod):
    tracks = []
    for track in IterateTracks():
        curve = track.GetCurve()
        if curve is None:
            continue
        keys = []
        for key_id in range(curve.GetKeyCount()):
            key = curve.GetKey(key_id)
            if keyMod == "None":
                if key.GetNBit(c4d.NBIT_TL1_SELECT): # If key is selected in timeline
                    keys.append(key)
            if keyMod == "Shift":
                if key.GetNBit(c4d.NBIT_TL1_SELECT2): # If key is selected in fcurve graph
                    keys.append(key)
        tracks.append([curve, keys])
    return tracks

def CheckBit(bit):
    if int(bit) == 1:
        return c4d.NBITCONTROL_SET
    elif int(bit) == 0:
        return c4d.NBITCONTROL_CLEAR

def SetKeys(keyData, keyMod):
    tracks = GetKeys(keyMod) # Get selected keys
    for track in tracks:
        keys = track[1]
        for i, k in enumerate(keys): # Iterate through tracks
            diff = 1.0
            if i < len(keyData)-1: # Not the last key
                valueDiffRef = float(keyData[i]['value']) - float(keyData[i+1]['value'])
                valueDiffOrig = k.GetValue() - k.GetNext().GetValue()
                if valueDiffRef != 0:
                    if valueDiffOrig != 0:
                        diff = valueDiffOrig / valueDiffRef # Fixed
            if i == len(keyData)-1: # The last key
                valueDiffRef = float(keyData[i-1]['value']) - float(keyData[i]['value'])
                valueDiffOrig = k.GetPred().GetValue() - k.GetValue()
                if valueDiffRef != 0:
                    if valueDiffOrig != 0:
                        diff = valueDiffOrig / valueDiffRef # Fixed
                        print "end diff " + str(diff)

            leftValue = float(keyData[i]['leftvalue']) * diff
            rightValue = float(keyData[i]['rightvalue']) * diff
            leftTime = c4d.BaseTime(float(keyData[i]['lefttime']))
            rightTime = c4d.BaseTime(float(keyData[i]['righttime']))
            
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, k) # Record undo
            curve = k.GetCurve()
            k.SetInterpolation(curve, c4d.CINTERPOLATION_SPLINE)
            k.ChangeNBit(c4d.NBIT_CKEY_AUTO, CheckBit(keyData[i]['autotan'])) # Auto Tangents
            k.SetAutomaticTangentMode(curve, int(keyData[i]['slope'])) # Slope
            k.ChangeNBit(c4d.NBIT_CKEY_CLAMP, CheckBit(keyData[i]['clamp'])) # Clamp
            k.ChangeNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT, CheckBit(keyData[i]['overshoot'])) # Remove Overshooting
            k.ChangeNBit(c4d.NBIT_CKEY_WEIGHTEDTANGENT, CheckBit(keyData[i]['weighted'])) # Weighted Tangent
            k.ChangeNBit(c4d.NBIT_CKEY_LOCK_O, CheckBit(keyData[i]['locktanangles'])) # Lock Tangent Angles
            k.ChangeNBit(c4d.NBIT_CKEY_LOCK_L, CheckBit(keyData[i]['locktanlengths'])) # Lock Tangent Lengths
            k.ChangeNBit(c4d.NBIT_CKEY_KEEPVISUALANGLE, CheckBit(keyData[i]['keepvisangle'])) # Keep Visual Angle
            k.SetValueLeft(curve, leftValue)
            k.SetValueRight(curve, rightValue)
            k.SetTimeLeft(curve, leftTime)
            k.SetTimeRight(curve, rightTime)

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    path, fn = os.path.split(__file__) # Get path of the script
    file = os.path.join(path, 'AR_EaseData.txt') # data file path
    keyData = []
    with open(file, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keyData.append(row)

    SetKeys(keyData, keyMod)
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D


# Execute main()
if __name__=='__main__':
    main()