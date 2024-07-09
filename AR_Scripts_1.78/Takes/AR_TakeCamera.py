"""
AR_TakeCamera

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_TakeCamera
Version: 1.0.0
Description-US: Creates take from selected camera(s) or if no selection for each camera.

Written for Maxon Cinema 4D 2024.1.0
Python version 3.11.4

Change log:
1.0.0 (24.11.2023) - Initial realease
"""

# Libraries
import c4d

# Global variables
camTypes = [5103, 1057516]

# Functions
def GetNextObject(op):
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()
    return op.GetNext()

def CollectCameras(op):
    cameras = []
    if op is None:
        return
    while op:
        if op.GetType() in camTypes:
            cameras.append(op)
        op = GetNextObject(op)
    return cameras

def CreateTake(name, cam):
    takeData  = doc.GetTakeData() # Get take data
    mainTake  = takeData.GetMainTake() # Get main take
    childTake = mainTake.GetDown() # Get first child take
        
    newTake = takeData.AddTake("", mainTake, childTake) # Add take
    newTake.SetName(name) # Set name
    newTake.SetCamera(takeData, cam) # Set camera
    
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, newTake) # Add undo for creating a take

def main():
    doc.StartUndo() # Start recording undos

    selection = doc.GetActiveObjects(1) # Get selected objects
    
    if len(selection) == 0: # If no selection
        cameras = CollectCameras(doc.GetFirstObject()) # Collect all cameras
        if cameras != None: # If there's any camera(s)
            for camera in reversed(cameras): # Iterate through cameras
                CreateTake(camera.GetName(), camera) # Create take
    else:
        for s in reversed(selection): # Iterate through selection
            if s.GetType() in camTypes:
                CreateTake(s.GetName(), s) # Create take
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
    pass

# Execute main
if __name__ == '__main__':
    main()