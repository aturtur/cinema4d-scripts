"""
AR_AxisToOrigin

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AxisToOrigin
Version: 1.0.0
Description-US: Sets object's axis to world origin.

Note: Currently does not support normal tags!

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

To do:
- Normal tag support

https://forums.cgsociety.org/t/script-help-zero-axis/1707180/6
https://plugincafe.maxon.net/topic/11359/handling-direction-of-the-normal-tag

"""

# Libraries
import c4d
from c4d.modules import snap

# Functions
def AxisToOrigin(obj):
    """ Puts object's axis to the world origin """
    if obj.CheckType(c4d.Opoint): # If point object
        matOld = obj.GetMg() # Store object's original matrix
        workplane = snap.GetWorkplaneObject(doc) # Get workplane
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Record undo for changing object
        obj.SetMg(workplane.GetMg()) # Set object's matrix

        if obj.CheckType(c4d.Opoint): # If point object
            mat  = obj.GetMg() # Get global matrix
            cnt  = obj.GetPointCount() # Get point count
            
            # WIP (Normal tag handling)
            #nt   = None
            #tags = obj.GetTags() # Get object's tags
            #for t in tags: # Iterate through tags
            #    if t.CheckType(c4d.Tnormal): # If normal tag
            #        nt = t # Store normal tag

            for i in range(cnt): # Iterate through points
                pos = obj.GetPoint(i) # Get point position
                posGlobal = matOld * pos # Calculate global point position
                obj.SetPoint(i, ~mat * posGlobal) # Set new point position

                # Fix tangents
                if (obj.CheckType(c4d.Ospline) and obj[c4d.SPLINEOBJECT_TYPE] == c4d.SPLINEOBJECT_TYPE_BEZIER): # If spline object and bezier type
                        posNew = obj.GetPoint(i) # Get new position
                        tan = obj.GetTangent(i) # Get tangent
                        tan_l = tan['vl'] + pos # Left tangent
                        tan_r = tan['vr'] + pos # Right tangent
                        tan_l_glo = matOld * tan_l
                        tan_r_glo = matOld * tan_r
                        tan_l_new = ~mat * tan_l_glo - posNew
                        tan_r_new = ~mat * tan_r_glo - posNew
                        obj.SetTangent(i, tan_l_new, tan_r_new) # Set new tangent

        obj.Message(c4d.MSG_UPDATE)
    else: # Otherwise
        print("Select editable object!")
    return True # All good!

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(1) # Get selected objects
    for s in selection: # Iterate through selected objects
        AxisToOrigin(s) # Run the main thing
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Update Cinema 4D

# Bla bla bla
if __name__=='__main__':
    main()