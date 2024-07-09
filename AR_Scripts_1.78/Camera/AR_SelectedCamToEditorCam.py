"""
AR_SelectedCamToEditorCam

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_SelectedCamToEditorCam
Version: 1.0.0
Description-US: Copies settings from selected camera to editor camera

Written for Maxon Cinema 4D 2024.3.2
Python version 3.11.4

Change log:
1.0.0 (10.01.2024) - Initial realease
"""

# Libraries
import c4d

# Functions
def main():

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    bd = doc.GetActiveBaseDraw() # Get active base draw
    
    editorCam = bd.GetEditorCamera() # Get editor camera
    selectedCam = doc.GetActiveObject() # Get active object

    cameraTypes = [5103, 1057516]
    if selectedCam.GetType() in cameraTypes:

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, selectedCam) # Add undo step for changing camera

        # Position, Rotation and Scale
        selectedCam.SetMg(editorCam.GetMg()) # Set matrix

        if selectedCam.GetType() == 5103: # If standard camera
            selectedCam[c4d.CAMERA_PROJECTION]                          = editorCam[c4d.CAMERA_PROJECTION]          # Projection Type
            selectedCam[c4d.CAMERA_FOCUS]                               = editorCam[c4d.CAMERA_FOCUS]               # Focal Length
            selectedCam[c4d.CAMERAOBJECT_APERTURE]                      = editorCam[c4d.CAMERAOBJECT_APERTURE]      # Sensor Size
            selectedCam[c4d.CAMERAOBJECT_FILM_OFFSET_X]                 = editorCam[c4d.CAMERAOBJECT_FILM_OFFSET_X] # Film Offset X
            selectedCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]                 = editorCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y] # Film Offset Y

        elif selectedCam.GetType() == 1057516: # If RS camera
            selectedCam[c4d.RSCAMERAOBJECT_PROJECTION]                  = editorCam[c4d.CAMERA_PROJECTION]          # Projection Type
            selectedCam[c4d.RSCAMERAOBJECT_FOCAL_LENGTH]                = editorCam[c4d.CAMERA_FOCUS]               # Focal Length
            selectedCam[c4d.RSCAMERAOBJECT_SENSOR_SIZE,c4d.VECTOR2D_X]  = editorCam[c4d.CAMERAOBJECT_APERTURE]      # Sensor Size
            selectedCam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT,c4d.VECTOR2D_X] = editorCam[c4d.CAMERAOBJECT_FILM_OFFSET_X] # Film Offset X
            selectedCam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT,c4d.VECTOR2D_Y] = editorCam[c4d.CAMERAOBJECT_FILM_OFFSET_Y] # Film Offset Y

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__ == '__main__':
    main()