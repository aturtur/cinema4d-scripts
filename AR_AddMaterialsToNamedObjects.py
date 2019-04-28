"""
AR_AddMaterialsToNamedObjects

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AddMaterialsToNamedObjects
Description-US: Add materials to objects that have exactly same name as the material
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# User variable
useFound = True
# True - Add materials only once to objects with same name
# False - Add materials to objects with same name no matter what

# Functions
def GetNextObject(op):
    if op==None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()
 
def IterateHierarchy(op, materials):
    global useFound # Get access to global variable
    if op is None:
        return 
    while op:
        found = False # Initialize found variable to false
        for m in materials: # Loop through materials
            if m.GetName() == op.GetName(): # If object's name matches with material's name
                tags = op.GetTags() # Get object's tags
                for t in tags: # Loop through tags
                    if t.GetType() == 5616: # If tag is texture tag
                        if t[c4d.TEXTURETAG_MATERIAL] == m: # If object already has texture tag with this material
                            found = True # Set foun variable to true
                if found != True and useFound == True: # If texture tag with same material not found
                    t = c4d.BaseTag(5616) # Initialize texture tag
                    t[c4d.TEXTURETAG_MATERIAL] = m # Set material to tag
                    op.InsertTag(t) # Insert texture tag to object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
                elif useFound == False:
                    t = c4d.BaseTag(5616) # Initialize texture tag
                    t[c4d.TEXTURETAG_MATERIAL] = m # Set material to tag
                    op.InsertTag(t) # Insert texture tag to object
                    doc.AddUndo(c4d.UNDOTYPE_NEW, t) # Add undo command for inserting new tag
        op = GetNextObject(op) 

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    try: # Try to execute following script
        materials = doc.GetMaterials() # Get materials
        start_object = doc.GetFirstObject()
        IterateHierarchy(start_object, materials)    
    except: # If something went wrong
        pass # Do nothing
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
  
# Execute main()
if __name__=='__main__':
    main()