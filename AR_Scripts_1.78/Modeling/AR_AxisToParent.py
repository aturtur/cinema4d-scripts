"""
AR_AxisToParent

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AxisToParent
Version: 1.0.0
Description-US: Sets object's axis to parent's origin (axis)

Note: Currently does not support normal tags!

Written for Maxon Cinema 4D 2024.4.1
Python version 3.11.4

Change log:
1.0.0 (04.07.2024) - Initial release
"""

# Libraries
import c4d

# Functions
def AxisToParent(obj):
    """ Puts object's axis to the world origin """
    if obj.CheckType(c4d.Opoint): # If point object
        matOld = obj.GetMg() # Store object's original matrix
        parent = obj.GetUp() # Get parent object
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj) # Record undo for changing object
        obj.SetMg(parent.GetMg()) # Set object's matrix
        
        childrenMat = [] # Initialize a list for storing children matrices
        children = obj.GetChildren() # Get children
        for child in children: # Iterate through children
            childrenMat.append(child.GetMg()) # Store child's matrix

        if obj.CheckType(c4d.Opoint): # If point object
            mat  = obj.GetMg() # Get global matrix
            cnt  = obj.GetPointCount() # Get point count

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

        # Fix children
        for i, child in enumerate(children): # Iterate through children
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, child) # Record undo for changing child
            child.SetMg(matOld * ~mat * childrenMat[i]) # Restore matrix

    else: # Otherwise
        print("Select editable object!")
    return True # All good!

def main():
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(1) # Get selected objects
    for s in selection: # Iterate through selected objects
        if s.GetUp() == None: # If no parent object
            print("Object doesn't have a parent object!")
        else:
            AxisToParent(s) # Run the main thing
    doc.EndUndo() # End recording undos
    c4d.EventAdd() # Update Cinema 4D

# Bla bla bla
if __name__=='__main__':
    main()