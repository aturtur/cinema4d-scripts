"""
AR_ZoomHelper

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ZoomHelper
Version: 1.0.0
Description-US: Creates a helper camera from active camera and activates 'Film Magnify' tool

Written for Maxon Cinema 4D 2024.4.1
Python version 3.11.4

Change log:
1.0.0 (09.07.2024) - Initial realease

"""

# Libraries
import c4d

# Functions
def SetActiveCamera(cam):
    bd = doc.GetActiveBaseDraw() # Get active base draw
    bd.SetSceneCamera(cam) # Set active camera
    return True

def GetActiveCamera():
    bd = doc.GetActiveBaseDraw() # Get active base draw
    cam = bd.GetSceneCamera(doc) # Get scene camera
    return cam

def CopyCameraData(sourceCam, targetCam):
    if sourceCam.GetType() == 5103: # If standard camera
        targetCam[c4d.CAMERA_PROJECTION]          = sourceCam[c4d.CAMERA_PROJECTION]                          # Projection Type
        targetCam[c4d.CAMERA_FOCUS]               = sourceCam[c4d.CAMERA_FOCUS]                               # Focal Length
        targetCam[c4d.CAMERAOBJECT_APERTURE]      = sourceCam[c4d.CAMERAOBJECT_APERTURE]                      # Sensor Size
        targetCam[c4d.CAMERAOBJECT_FILM_OFFSET_X] = sourceCam[c4d.CAMERAOBJECT_FILM_OFFSET_X]                 # Film Offset X
        targetCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = sourceCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]                 # Film Offset Y

    elif sourceCam.GetType() == 1057516: # If RS camera
        targetCam[c4d.CAMERA_PROJECTION]          = sourceCam[c4d.RSCAMERAOBJECT_PROJECTION]                  # Projection Type
        targetCam[c4d.CAMERA_FOCUS]               = sourceCam[c4d.RSCAMERAOBJECT_FOCAL_LENGTH]                # Focal Length
        targetCam[c4d.CAMERAOBJECT_APERTURE]      = sourceCam[c4d.RSCAMERAOBJECT_SENSOR_SIZE,c4d.VECTOR2D_X]  # Sensor Size
        targetCam[c4d.CAMERAOBJECT_FILM_OFFSET_X] = sourceCam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT,c4d.VECTOR2D_X] # Film Offset X
        targetCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = sourceCam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT,c4d.VECTOR2D_Y] # Film Offset Y
    return True

def main():
    bd = doc.GetActiveBaseDraw() # Get active base draw
    doc.StartUndo() # Start recording undos
    helperCam = c4d.BaseObject(5103) # Standard camera
    editorCamera = bd.GetEditorCamera() # Get default camera
    activeCam = GetActiveCamera() # Get active cam

    helperCam.SetName(activeCam.GetName()+"_helper") # Set name
    CopyCameraData(activeCam, helperCam) # Copy settings

    if activeCam == editorCamera: # If active camera is same as default camera
        helperCam.SetMg(activeCam.GetMg()) # Set matrix
        doc.InsertObject(helperCam) # Insert helper camera into the document
    else: # Otherwise
        helperCam.InsertUnder(activeCam) # Insert helper camera under the active camera
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, helperCam) # Add undo step for inserting new object

    SetActiveCamera(helperCam) # Set active camera
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    
    # Pick Film Magnify tool
    c4d.CallCommand(1016008) # Film Magnify
    
    pass

# Execute main
if __name__ == '__main__':
    main()