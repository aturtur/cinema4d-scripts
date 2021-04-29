"""
AR_EaseCopy

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_EaseCopy
Version: 1.0
Description-US: Copies easing of selected keyframes. If you use F-Curve editor hold SHIFT when running the script.

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
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
    keys = []
    for track in IterateTracks():
        curve = track.GetCurve()
        if curve is None:
            continue

        for i, key_id in enumerate(range(curve.GetKeyCount())):
            key = curve.GetKey(key_id)
            if keyMod == "None":
              if key.GetNBit(c4d.NBIT_TL1_SELECT):
                  keys.append({'id': key_id,
                             'value': key.GetValue(),
                             'time': key.GetTime().Get(),
                             'lefttime': key.GetTimeLeft().Get(),
                             'righttime': key.GetTimeRight().Get(),
                             'leftvalue': key.GetValueLeft(),
                             'rightvalue': key.GetValueRight(),
                             'autotan': key.GetNBit(c4d.NBIT_CKEY_AUTO),
                             'slope': key.GetAutomaticTangentMode(),
                             'clamp': key.GetNBit(c4d.NBIT_CKEY_CLAMP),
                             'overshoot': key.GetNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT),
                             'weighted': key.GetNBit(c4d.NBIT_CKEY_WEIGHTEDTANGENT),
                             'locktanangles': key.GetNBit(c4d.NBIT_CKEY_LOCK_O),
                             'locktanlengths': key.GetNBit(c4d.NBIT_CKEY_LOCK_L),
                             'keepvisangle': key.GetNBit(c4d.NBIT_CKEY_KEEPVISUALANGLE)
                  })
            if keyMod == "Shift":
              if key.GetNBit(c4d.NBIT_TL1_SELECT2):
                  keys.append({'id': key_id,
                             'value': key.GetValue(),
                             'time': key.GetTime().Get(),
                             'lefttime': key.GetTimeLeft().Get(),
                             'righttime': key.GetTimeRight().Get(),
                             'leftvalue': key.GetValueLeft(),
                             'rightvalue': key.GetValueRight(),
                             'autotan': key.GetNBit(c4d.NBIT_CKEY_AUTO),
                             'slope': key.GetAutomaticTangentMode(),
                             'clamp': key.GetNBit(c4d.NBIT_CKEY_CLAMP),
                             'overshoot': key.GetNBit(c4d.NBIT_CKEY_REMOVEOVERSHOOT),
                             'weighted': key.GetNBit(c4d.NBIT_CKEY_WEIGHTEDTANGENT),
                             'locktanangles': key.GetNBit(c4d.NBIT_CKEY_LOCK_O),
                             'locktanlengths': key.GetNBit(c4d.NBIT_CKEY_LOCK_L),
                             'keepvisangle': key.GetNBit(c4d.NBIT_CKEY_KEEPVISUALANGLE)
                  })

    return keys

def main():
    keyMod = GetKeyMod() # Get keymodifier
    keys = GetKeys(keyMod) # Collect keyframe data
    path, fn = os.path.split(__file__) # Get path of the script
    file = os.path.join(path, 'AR_EaseData.txt') # data file path
    with open(file, 'w') as csvfile:
        csv_columns = ['id',
                       'value',
                       'time',
                       'lefttime',
                       'righttime',
                       'leftvalue',
                       'rightvalue',
                       'autotan',
                       'slope',
                       'clamp',
                       'overshoot',
                       'weighted',
                       'locktanangles',
                       'locktanlengths',
                       'keepvisangle']
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in keys:
            writer.writerow(data)

# Execute main()
if __name__=='__main__':
    main()