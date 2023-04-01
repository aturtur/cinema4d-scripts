"""
AR_BakeCam

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_BakeCam
Version: 1.2.0
Description-US: Bakes selected camera(s) to the world space

Written for Maxon Cinema 4D 2023.1.0
Python version 3.9.1

Change log:
1.2.0 (18.11.2022) - Parallel processing, bakes multiple cameras in one go. Progress bar
1.1.0 (10.11.2022) - Support for Redshift camera (new in C4D 2023.1.0)
1.0.2 (10.10.2021) - Updated to R25
1.0.1 (27.10.2020) - Fixed setTime bug
1.0.0 (21.08.2019) - Initial release
"""

# Libraries
import c4d
from c4d import utils as u

# Global variables
suffix = "_baked"

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

def DummyStandardCamera(obj, doc):
    dummyCamera = c4d.BaseObject(5103) # Initialize a standard C4D camera object
    dummyCamera.SetName("Dummy "+obj.GetName()) # Set name
    doc.InsertObject(dummyCamera) # Insert dummyCamera to document
    MoveToLast(dummyCamera, doc) # Move new camera in the object hierarchy
    pythontag = c4d.BaseTag(c4d.Tpython) # Initialize python tag
    dummyCamera.InsertTag(pythontag) # Insert python tag to object
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 449) # Set priority value to last possible value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false
    pythontag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set priority data
    pythontag[c4d.TPYTHON_FRAME] = True # Set frame dependet to true
    link1 = CreateUserDataLink(pythontag, "Object", obj) # Create user data link
    pythontag[c4d.TPYTHON_CODE] = ( "import c4d\n"
                                    "def main():\n"
                                    "\tcam = op[c4d.ID_USERDATA,1]\n"
                                    "\tmat = cam.GetMg()\n"
                                    "\tobj = op.GetObject()\n"
                                    "\tobj.SetMg(mat)\n"
                                    " \n"
                                    "\t# Basic\n"
                                    "\tobj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_USECOLOR] = cam[c4d.ID_BASEOBJECT_USECOLOR]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_COLOR] = cam[c4d.ID_BASEOBJECT_COLOR]\n"
                                    " \n"
                                    "\t# Object\n"
                                    "\tobj[c4d.CAMERA_PROJECTION] = cam[c4d.CAMERA_PROJECTION]\n"
                                    "\tobj[c4d.CAMERA_FOCUS] = cam[c4d.CAMERA_FOCUS]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE] = cam[c4d.CAMERAOBJECT_APERTURE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FOV] = cam[c4d.CAMERAOBJECT_FOV]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FOV_VERTICAL] = cam[c4d.CAMERAOBJECT_FOV_VERTICAL]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FILM_OFFSET_X] = cam[c4d.CAMERAOBJECT_FILM_OFFSET_X]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = cam[c4d.CAMERAOBJECT_FILM_OFFSET_Y]\n"
                                    "\tobj[c4d.CAMERAOBJECT_TARGETDISTANCE] = cam[c4d.CAMERAOBJECT_TARGETDISTANCE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_TARGETOBJECT] = cam[c4d.CAMERAOBJECT_TARGETOBJECT]\n"
                                    "\tobj[c4d.CAMERAOBJECT_WHITE_BALANCE_TEMPERATURE] = cam[c4d.CAMERAOBJECT_WHITE_BALANCE_TEMPERATURE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_WHITE_BALANCE_LIGHTS_ONLY] = cam[c4d.CAMERAOBJECT_WHITE_BALANCE_LIGHTS_ONLY]\n"
                                    "\tobj[c4d.CAMERAOBJECT_AFX] = cam[c4d.CAMERAOBJECT_AFX]\n"
                                    " \n"
                                    "\t# Physical\n"
                                    "\tobj[c4d.CAMERAOBJECT_MOVIECAMERA] = cam[c4d.CAMERAOBJECT_MOVIECAMERA]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FNUMBER_VALUE] = cam[c4d.CAMERAOBJECT_FNUMBER_VALUE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_EXPOSURE] = cam[c4d.CAMERAOBJECT_EXPOSURE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_ISO_VALUE] = cam[c4d.CAMERAOBJECT_ISO_VALUE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_GAIN_VALUE] = cam[c4d.CAMERAOBJECT_GAIN_VALUE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SHUTTER_SPEED_VALUE] = cam[c4d.CAMERAOBJECT_SHUTTER_SPEED_VALUE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SHUTTER_ANGLE] = cam[c4d.CAMERAOBJECT_SHUTTER_ANGLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SHUTTER_OFFSET] = cam[c4d.CAMERAOBJECT_SHUTTER_OFFSET]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SHUTTER_EFFICIENCY] = cam[c4d.CAMERAOBJECT_SHUTTER_EFFICIENCY]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LENS_DISTORTION_QUAD] = cam[c4d.CAMERAOBJECT_LENS_DISTORTION_QUAD]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LENS_DISTORTION_CUBIC] = cam[c4d.CAMERAOBJECT_LENS_DISTORTION_CUBIC]\n"
                                    "\tobj[c4d.CAMERAOBJECT_VIGNETTING_INTENSITY] = cam[c4d.CAMERAOBJECT_VIGNETTING_INTENSITY]\n"
                                    "\tobj[c4d.CAMERAOBJECT_VIGNETTING_OFFSET] = cam[c4d.CAMERAOBJECT_VIGNETTING_OFFSET]\n"
                                    "\tobj[c4d.CAMERAOBJECT_CHROMATIC_ABERRATION_STRENGTH] = cam[c4d.CAMERAOBJECT_CHROMATIC_ABERRATION_STRENGTH]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_SHAPE] = cam[c4d.CAMERAOBJECT_APERTURE_SHAPE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_BLADES] = cam[c4d.CAMERAOBJECT_APERTURE_BLADES]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_ANGLE] = cam[c4d.CAMERAOBJECT_APERTURE_ANGLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_BIAS] = cam[c4d.CAMERAOBJECT_APERTURE_BIAS]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_ANISOTROPY] = cam[c4d.CAMERAOBJECT_APERTURE_ANISOTROPY]\n"
                                    "\tobj[c4d.CAMERAOBJECT_APERTURE_SHADER] = cam[c4d.CAMERAOBJECT_APERTURE_SHADER]\n"
                                    " \n"
                                    "\t# Details\n"
                                    "\tobj[c4d.CAMERAOBJECT_NEAR_CLIPPING_ENABLE] = cam[c4d.CAMERAOBJECT_NEAR_CLIPPING_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_NEAR_CLIPPING] = cam[c4d.CAMERAOBJECT_NEAR_CLIPPING]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FAR_CLIPPING_ENABLE] = cam[c4d.CAMERAOBJECT_FAR_CLIPPING_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FAR_CLIPPING] = cam[c4d.CAMERAOBJECT_FAR_CLIPPING]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SHOW] = cam[c4d.CAMERAOBJECT_SHOW]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FRONTBLUR] = cam[c4d.CAMERAOBJECT_FRONTBLUR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FRONTSTART] = cam[c4d.CAMERAOBJECT_FRONTSTART]\n"
                                    "\tobj[c4d.CAMERAOBJECT_FRONTEND] = cam[c4d.CAMERAOBJECT_FRONTEND]\n"
                                    "\tobj[c4d.CAMERAOBJECT_REARBLUR] = cam[c4d.CAMERAOBJECT_REARBLUR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_REARSTART] = cam[c4d.CAMERAOBJECT_REARSTART]\n"
                                    "\tobj[c4d.CAMERAOBJECT_REAREND] = cam[c4d.CAMERAOBJECT_REAREND]\n"
                                    " \n"
                                    "\t# Composition\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_ENABLE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_CELLS] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_CELLS]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GRID_COLOR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_MIRROR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_MIRROR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_DIAGONAL_COLOR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_MODE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_MODE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_MIRROR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_MIRROR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_FLIP] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_FLIP]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_TRIANGLES_COLOR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_I] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_I]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_TOP] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_TOP]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_RIGHT] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_RIGHT]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_BOTTOM] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_BOTTOM]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_LEFT] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_LEFT]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSECTION_COLOR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_MIRROR_H] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_MIRROR_H]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_MIRROR_V] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_MIRROR_V]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_FLIP] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_FLIP]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_ALIGN_V] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_ALIGN_V]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_GOLDENSPIRAL_COLOR]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_SCALE] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_SCALE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_COLOR] = cam[c4d.CAMERAOBJECT_LAYOUTHELP_DRAW_CROSSHAIR_COLOR]\n"
                                    " \n"
                                    "\t# Stereoscopic\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_MODE] = cam[c4d.CAMERAOBJECT_STEREO_MODE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_EYESEPARATION] = cam[c4d.CAMERAOBJECT_STEREO_EYESEPARATION]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_PLACEMENT] = cam[c4d.CAMERAOBJECT_STEREO_PLACEMENT]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_SHOW_ALL] = cam[c4d.CAMERAOBJECT_STEREO_SHOW_ALL]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_ZERO_PARALLAX] = cam[c4d.CAMERAOBJECT_STEREO_ZERO_PARALLAX]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_AUTO_PLANES] = cam[c4d.CAMERAOBJECT_STEREO_AUTO_PLANES]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_NEAR_PLANE] = cam[c4d.CAMERAOBJECT_STEREO_NEAR_PLANE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_FAR_PLANE] = cam[c4d.CAMERAOBJECT_STEREO_FAR_PLANE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_STEREO_SHOW_FLOATING_FRAME] = cam[c4d.CAMERAOBJECT_STEREO_SHOW_FLOATING_FRAME]\n"
                                    " \n"
                                    "\t# Stereoscopic (w Spherical)\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_LAYOUT] = cam[c4d.CAMERAOBJECT_SPC_STEREO_LAYOUT]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_EYESEPARATION] = cam[c4d.CAMERAOBJECT_SPC_STEREO_EYESEPARATION]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_NECK_DIST] = cam[c4d.CAMERAOBJECT_SPC_STEREO_NECK_DIST]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_FOCAL] = cam[c4d.CAMERAOBJECT_SPC_STEREO_FOCAL]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_MODE] = cam[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_MODE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_ANGLE] = cam[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_ANGLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_EXP] = cam[c4d.CAMERAOBJECT_SPC_STEREO_N_POLE_EXP]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_MODE] = cam[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_MODE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_ANGLE] = cam[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_ANGLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_EXP] = cam[c4d.CAMERAOBJECT_SPC_STEREO_S_POLE_EXP]\n"
                                    " \n"
                                    "\t# Spherical\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_ENABLE] = cam[c4d.CAMERAOBJECT_SPC_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_GIZMO] = cam[c4d.CAMERAOBJECT_SPC_GIZMO]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_PROJECTION_MAPPING] = cam[c4d.CAMERAOBJECT_SPC_PROJECTION_MAPPING]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_FIT_FRAME] = cam[c4d.CAMERAOBJECT_SPC_FIT_FRAME]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_FULL_RANGE_ENABLE] = cam[c4d.CAMERAOBJECT_SPC_FULL_RANGE_ENABLE]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_LONG_MIN] = cam[c4d.CAMERAOBJECT_SPC_LONG_MIN]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_LONG_MAX] = cam[c4d.CAMERAOBJECT_SPC_LONG_MAX]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_LAT_MIN] = cam[c4d.CAMERAOBJECT_SPC_LAT_MIN]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_LAT_MAX] = cam[c4d.CAMERAOBJECT_SPC_LAT_MAX]\n"
                                    "\tobj[c4d.CAMERAOBJECT_SPC_DOME_LAT] = cam[c4d.CAMERAOBJECT_SPC_DOME_LAT]") # Python tag script
    return dummyCamera

def DummyRedshiftCamera(obj, doc):
    dummyCamera = c4d.BaseObject(1057516) # Initialize a Redshift camera object
    dummyCamera.SetName("Dummy "+obj.GetName()) # Set name
    doc.InsertObject(dummyCamera) # Insert dummyCamera to document
    MoveToLast(dummyCamera, doc) # Move new camera in the object hierarchy
    pythontag = c4d.BaseTag(c4d.Tpython) # Initialize python tag
    dummyCamera.InsertTag(pythontag) # Insert python tag to object
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 449) # Set priority value to last possible value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false
    pythontag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set priority data
    pythontag[c4d.TPYTHON_FRAME] = True # Set frame dependet to true
    link1 = CreateUserDataLink(pythontag, "Object", obj) # Create user data link
    pythontag[c4d.TPYTHON_CODE] = ( "import c4d\n"
                                    "def main():\n"
                                    "\tcam = op[c4d.ID_USERDATA,1]\n"
                                    "\tmat = cam.GetMg()\n"
                                    "\tobj = op.GetObject()\n"
                                    "\tobj.SetMg(mat)\n"
                                    " \n"
                                    "\t# Basic\n"
                                    "\tobj[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = cam[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = cam[c4d.ID_BASEOBJECT_VISIBILITY_RENDER]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_USECOLOR] = cam[c4d.ID_BASEOBJECT_USECOLOR]\n"
                                    "\tobj[c4d.ID_BASEOBJECT_COLOR] = cam[c4d.ID_BASEOBJECT_COLOR]\n"
                                    " \n"
                                    "\t# Object\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_PROJECTION] = cam[c4d.RSCAMERAOBJECT_PROJECTION]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FOCAL_LENGTH] = cam[c4d.RSCAMERAOBJECT_FOCAL_LENGTH]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FOV] = cam[c4d.RSCAMERAOBJECT_FOV]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SENSOR_SHIFT] = cam[c4d.RSCAMERAOBJECT_SENSOR_SHIFT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SENSOR_SIZE_PRESET] = cam[c4d.RSCAMERAOBJECT_SENSOR_SIZE_PRESET]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SENSOR_SIZE] = cam[c4d.RSCAMERAOBJECT_SENSOR_SIZE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SENSOR_SIZE_LOCK_RATIO] = cam[c4d.RSCAMERAOBJECT_SENSOR_SIZE_LOCK_RATIO]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SENSOR_SIZE_FIT_MODE] = cam[c4d.RSCAMERAOBJECT_SENSOR_SIZE_FIT_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_NEAR_CLIPPING_ENABLE] = cam[c4d.RSCAMERAOBJECT_NEAR_CLIPPING_ENABLE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_NEAR_CLIPPING] = cam[c4d.RSCAMERAOBJECT_NEAR_CLIPPING]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FAR_CLIPPING_ENABLE] = cam[c4d.RSCAMERAOBJECT_FAR_CLIPPING_ENABLE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FAR_CLIPPING] = cam[c4d.RSCAMERAOBJECT_FAR_CLIPPING]\n"
                                    " \n"
                                    "\t# Optical\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_EXPOSURE_TYPE] = cam[c4d.RSCAMERAOBJECT_EXPOSURE_TYPE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_EXPOSURE] = cam[c4d.RSCAMERAOBJECT_EXPOSURE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_ISO] = cam[c4d.RSCAMERAOBJECT_ISO]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_WHITE_POINT] = cam[c4d.RSCAMERAOBJECT_WHITE_POINT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_VIGNETTING] = cam[c4d.RSCAMERAOBJECT_VIGNETTING]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE] = cam[c4d.RSCAMERAOBJECT_FOCUS_DISTANCE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TARGETOBJECT] = cam[c4d.RSCAMERAOBJECT_TARGETOBJECT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FOCUS_OFFSET] = cam[c4d.RSCAMERAOBJECT_FOCUS_OFFSET]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FNUMBER_VALUE] = cam[c4d.RSCAMERAOBJECT_FNUMBER_VALUE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BOKEH_ENABLED] = cam[c4d.RSCAMERAOBJECT_BOKEH_ENABLED]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_SHAPE] = cam[c4d.RSCAMERAOBJECT_APERTURE_SHAPE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_ASPECT] = cam[c4d.RSCAMERAOBJECT_APERTURE_ASPECT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_SPHERICAL_ABBERATION] = cam[c4d.RSCAMERAOBJECT_APERTURE_SPHERICAL_ABBERATION]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_BLADES] = cam[c4d.RSCAMERAOBJECT_APERTURE_BLADES]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_ANGLE] = cam[c4d.RSCAMERAOBJECT_APERTURE_ANGLE]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_APERTURE_IMAGE] = cam[c4d.RSCAMERAOBJECT_APERTURE_IMAGE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_APERTURE_BOKEH_NORMALIZATION] = cam[c4d.RSCAMERAOBJECT_APERTURE_BOKEH_NORMALIZATION]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SHUTTER_TYPE] = cam[c4d.RSCAMERAOBJECT_SHUTTER_TYPE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SHUTTER_TIME_RATIO] = cam[c4d.RSCAMERAOBJECT_SHUTTER_TIME_RATIO]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_MOTION_BLUR_MODE] = cam[c4d.RSCAMERAOBJECT_MOTION_BLUR_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SELF_BLUR_ENABLED] = cam[c4d.RSCAMERAOBJECT_SELF_BLUR_ENABLED]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SHUTTER_OFFSET_FRAMES] = cam[c4d.RSCAMERAOBJECT_SHUTTER_OFFSET_FRAMES]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_SHUTTER_EFFICIENCY] = cam[c4d.RSCAMERAOBJECT_SHUTTER_EFFICIENCY]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_LENS_DISTORTION_ENABLED] = cam[c4d.RSCAMERAOBJECT_LENS_DISTORTION_ENABLED]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_LENS_DISTORTION_IMAGE] = cam[c4d.RSCAMERAOBJECT_LENS_DISTORTION_IMAGE]\n"
                                    " \n"
                                    "\t# Color Correction\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_ENABLED] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_ENABLED]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_HIGHLIGHTS] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_HIGHLIGHTS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_DESATURATE_HIGHLIGHTS] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_DESATURATE_HIGHLIGHTS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_BLACKS] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_BLACKS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_BLACKS_THRESHOLD] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_BLACKS_THRESHOLD]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_TONE_MAPPING_SATURATION] = cam[c4d.RSCAMERAOBJECT_TONE_MAPPING_SATURATION]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_LUT_MODE] = cam[c4d.RSCAMERAOBJECT_LUT_MODE]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_LUT_FILENAME] = cam[c4d.RSCAMERAOBJECT_LUT_FILENAME]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_LUT_LIST] = cam[c4d.RSCAMERAOBJECT_LUT_LIST]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_LUT_INTENSITY] = cam[c4d.RSCAMERAOBJECT_LUT_INTENSITY]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_MODE] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_MODE]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CONTRAST] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CONTRAST]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_RGB] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_RGB]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_RED] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_RED]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_GREEN] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_GREEN]\n"
                                    "\t#obj[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_BLUE] = cam[c4d.RSCAMERAOBJECT_COLOR_CONTROLS_CURVE_BLUE]\n"
                                    " \n"
                                    "\t# Lens Effects\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_MODE] = cam[c4d.RSCAMERAOBJECT_BLOOM_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_INTENSITY] = cam[c4d.RSCAMERAOBJECT_BLOOM_INTENSITY]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_THRESHOLD] = cam[c4d.RSCAMERAOBJECT_BLOOM_THRESHOLD]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_SOFTNESS] = cam[c4d.RSCAMERAOBJECT_BLOOM_SOFTNESS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT_1] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT_1]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT_2] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT_2]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT_3] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT_3]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT_4] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT_4]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_BLOOM_TINT_5] = cam[c4d.RSCAMERAOBJECT_BLOOM_TINT_5]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_MODE] = cam[c4d.RSCAMERAOBJECT_FLARE_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_INTENSITY] = cam[c4d.RSCAMERAOBJECT_FLARE_INTENSITY]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_THRESHOLD] = cam[c4d.RSCAMERAOBJECT_FLARE_THRESHOLD]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_SOFTNESS] = cam[c4d.RSCAMERAOBJECT_FLARE_SOFTNESS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_CHROMATIC] = cam[c4d.RSCAMERAOBJECT_FLARE_CHROMATIC]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_SIZE] = cam[c4d.RSCAMERAOBJECT_FLARE_SIZE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_HALO] = cam[c4d.RSCAMERAOBJECT_FLARE_HALO]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_1] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_1]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_2] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_2]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_3] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_3]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_4] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_4]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_5] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_5]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_FLARE_TINT_6] = cam[c4d.RSCAMERAOBJECT_FLARE_TINT_6]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_MODE] = cam[c4d.RSCAMERAOBJECT_STREAK_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_INTENSITY] = cam[c4d.RSCAMERAOBJECT_STREAK_INTENSITY]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_THRESHOLD] = cam[c4d.RSCAMERAOBJECT_STREAK_THRESHOLD]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_TAIL] = cam[c4d.RSCAMERAOBJECT_STREAK_TAIL]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_SOFTNESS] = cam[c4d.RSCAMERAOBJECT_STREAK_SOFTNESS]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_NUMBER] = cam[c4d.RSCAMERAOBJECT_STREAK_NUMBER]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_STREAK_ANGLE] = cam[c4d.RSCAMERAOBJECT_STREAK_ANGLE]\n"
                                    " \n"
                                    "\t# Display\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_MODE] = cam[c4d.RSCAMERAOBJECT_DISPLAY_MODE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE] = cam[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE_COLOR] = cam[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE_COLOR]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE_OPACITY] = cam[c4d.RSCAMERAOBJECT_DISPLAY_FOCUS_PLANE_OPACITY]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_SHOW_NEAR_CLIP_PLANE] = cam[c4d.RSCAMERAOBJECT_DISPLAY_SHOW_NEAR_CLIP_PLANE]\n"
                                    "\tobj[c4d.RSCAMERAOBJECT_DISPLAY_SHOW_FAR_CLIP_PLANE] = cam[c4d.RSCAMERAOBJECT_DISPLAY_SHOW_FAR_CLIP_PLANE]") # Python tag script
    return dummyCamera

def MoveToLast(obj, doc):
    items = doc.GetObjects() # Get top level items from the document
    last = items[-1] # The Last item in the hierarchy
    obj.InsertAfter(last) # Move object after the last item

def MoveToFirst(obj, doc):
    items = doc.GetObjects() # Get top level items from the document
    first = items[0] # The first item in the hierarchy
    obj.InsertBefore(first) # Move object before the first item

def CopyRendererTags(source, target):
    tags = source.GetTags() # Get objects tags
    # 1036760 Redshift Camera Tag
    # 1029524 Octane Camera Tag
    # 1029989 Arnold Parameter Tag
    rendererTags = [1029524, 1036760, 1029989] # Third party renderer tags
    for t in reversed(tags): # Iterate through tags
        if t.GetType() in rendererTags: # If tag is renderer tag
            d = t.GetClone() # Duplicate the tag
            target.InsertTag(d) # Copy tag

def CleanKeys(cameras):
    """ Removes unnecessary keyframes """
    for i, cam in enumerate(cameras): # Loop through baked cameras (cam[2])
        theCam = cam[2] # baked camera
        ctracks = theCam.GetCTracks() # Get baked camera's CTracks

        #
        progress = u.RangeMap(i, 0, len(cameras), 0, 100, True)
        c4d.StatusSetText("Cleaning keys")
        c4d.StatusSetBar(progress)
        #

        for ctrack in ctracks: # Iterate through CTracks
            curve = ctrack.GetCurve() # Get Curve (keyframe holder)
            keyCount = curve.GetKeyCount() # Get Keyframe count
            keysToDelete = [] # Initialize an array for kayframes that can be deleted
            for key in range(0, keyCount): # Iterate through keyframes
                keyValue = curve.GetKey(key).GetValue() # Get keyframe value
                if (key != 0) and (key != keyCount-1): # If not first or last keyframe
                    prevKey = curve.GetKey(key-1).GetValue() # Get previous keyframes value
                    nextKey = curve.GetKey(key+1).GetValue() # Get next keyframes value
                    if keyValue == prevKey and keyValue == nextKey: # If current keyframe has same value with previous and next keyframe
                        keysToDelete.append(key) # Add this keyframe to deleted keys
            for d in reversed(keysToDelete): # Iterate through keystoDelete array
                curve.DelKey(d) # Delete keyframe
        # Remove unused tracks
        ctracks = theCam.GetCTracks() # Get object's CTracks again
        for ctrack in ctracks:
            curve = ctrack.GetCurve()
            keyCount = curve.GetKeyCount()
            if keyCount == 2: # If CTrack has only two keyframes
                if curve.GetKey(0).GetValue() == curve.GetKey(1).GetValue(): # ...and if they has same value
                    ctrack.Remove() # ...CTrack can be removed
        c4d.GeSyncMessage(c4d.EVMSG_UPDATEBASEDRAW)

def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None):
    """ Create user data link """
    if obj is None: return False # If there is no object stop the function
    if shortname is None: shortname = name # Short name is name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK) # Initialize user data
    bc[c4d.DESC_NAME] = name # Set user data name
    bc[c4d.DESC_SHORT_NAME] = shortname # Set userdata short name
    bc[c4d.DESC_DEFAULT] = link # Set default value
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF # Disable animation option
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None: # If there is parent group
        bc[c4d.DESC_PARENTGROUP] = parentGroup # Set parent group
    element = obj.AddUserData(bc) # Add user data
    obj[element] = link # Set user data value
    return element # Return user data field

def SetCurrentFrame(frame, doc):
    """ Changes editor's current frame to  """
    doc.SetTime(c4d.BaseTime(frame,doc.GetFps())) # Set current time to given frame
    doc.ExecutePasses(None, True, True, True, 0) # Animate the current frame of the document
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) # Send a synchronous event message that time has changed
    return

def RemoveTags(obj):
    """ Removes tags of the object  """
    tags = obj.GetTags() # Get tags
    for t in tags: # Iterate through tags
        t.Remove() # Remove tag

def GetDataVault(camType):
    if camType == 5103: # If standard C4D camera
        dataVault = [ [903, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [903, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [903, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Position
                      [904, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Rotation
                      [905, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Scale

                      # Basic
                      [901, c4d.DTYPE_LONG], # Visible in Editor
                      [902, c4d.DTYPE_LONG], # Visible in Renderer
                      [907, c4d.DTYPE_LONG], # User Color
                      [908, c4d.DTYPE_REAL, 1000, c4d.DTYPE_COLOR], [908, c4d.DTYPE_REAL, 1001, c4d.DTYPE_COLOR], [908, c4d.DTYPE_REAL, 1002, c4d.DTYPE_COLOR], # Display Color

                      # Object
                      [1001, c4d.DTYPE_LONG], # Projection
                      [500, c4d.DTYPE_REAL], # Focal Length
                      [1006, c4d.DTYPE_REAL], # Sensor Size
                      [1008, c4d.DTYPE_REAL], # Field of View (Horizontal)
                      [4600, c4d.DTYPE_REAL], # Field of View (Vertical)
                      [1000, c4d.DTYPE_REAL], # Zoom
                      [1118, c4d.DTYPE_REAL], # Film Offset X
                      [1119, c4d.DTYPE_REAL], # Film Offset Y
                      [1010, c4d.DTYPE_REAL], # Focus Distance
                      #[1009, c4d.DTYPE_BOOL], #Use Target Object
                      #[1130], # Focus Object
                      [1311, c4d.DTYPE_REAL], # White Balance
                      [1312, c4d.DTYPE_BOOL], # Affect Lights Only
                      [1344, c4d.DTYPE_BOOL], # Export to Compositing

                      # Physical
                      #[1343, c4d.DTYPE_BOOL], # Movie Camera
                      [1201, c4d.DTYPE_REAL], # F-Stop
                      [1220, c4d.DTYPE_BOOL], # Exposure
                      [1231, c4d.DTYPE_REAL], # ISO
                      [1241, c4d.DTYPE_REAL], # Gain (dB)
                      [1211, c4d.DTYPE_REAL], # Shutter Speed (s)
                      [1212, c4d.DTYPE_REAL], # Shutter Angle
                      [1213, c4d.DTYPE_REAL], # Shutter Offset
                      [1214, c4d.DTYPE_REAL], # Shutter Effiency
                      [1331, c4d.DTYPE_REAL], # Lens Distortion - Quadratic
                      [1333, c4d.DTYPE_REAL], # Lens Distortion - Cubic
                      [1321, c4d.DTYPE_REAL], # Vignetting Intensity
                      [1322, c4d.DTYPE_REAL], # Vignetting Offset
                      [1341, c4d.DTYPE_REAL], # Chromatic Aberration
                      [1300, c4d.DTYPE_BOOL], # Diaphragm Shape
                      [1301, c4d.DTYPE_LONG], # Blades
                      [1302, c4d.DTYPE_REAL], # Angle
                      [1303, c4d.DTYPE_REAL], # Bias
                      [1306, c4d.DTYPE_REAL], # Anistropy

                      # Details
                      [1123, c4d.DTYPE_BOOL], # Enable Near Clipping
                      [1122, c4d.DTYPE_REAL], # Near Clipping
                      [1129, c4d.DTYPE_BOOL], # Enable Far Clipping
                      [1128, c4d.DTYPE_REAL], # Far Clipping
                      [1007, c4d.DTYPE_BOOL], # Show Cone
                      [1111, c4d.DTYPE_BOOL], # DOF Map Front Blur
                      [1112, c4d.DTYPE_REAL], # Front Blur Start
                      [1113, c4d.DTYPE_REAL], # Front Blur End
                      [1114, c4d.DTYPE_BOOL], # DOF Map Rear Blur
                      [1115, c4d.DTYPE_REAL], # Rear Blur Start
                      [1116, c4d.DTYPE_REAL], # Rear Blur End

                      # Stereoscopic
                      #[4200, c4d.DTYPE_LONG], # Mode
                      #[4201, c4d.DTYPE_REAL], # Eye Separation
                      #[4202, c4d.DTYPE_LONG], # Placement
                      #[4207, c4d.DTYPE_BOOL], # Show All Cameras
                      #[4205, c4d.DTYPE_REAL], # Zero Parallax
                      #[4208, c4d.DTYPE_LONG], # Auto Planes
                      #[4204, c4d.DTYPE_REAL], # Near Plane
                      #[4206, c4d.DTYPE_REAL], # Far Plane
                      #[4209, c4d.DTYPE_BOOL], # Show Floating Frame

                      # Spherical
                      [1160, c4d.DTYPE_BOOL], # Enable
                      [1003, c4d.DTYPE_LONG], # FOV Helper
                      [1004, c4d.DTYPE_LONG], # Mapping
                      [1162, c4d.DTYPE_BOOL], # Fit Frame
                      [1161, c4d.DTYPE_BOOL], # Use Full Range
                      [1170, c4d.DTYPE_REAL], # Long Min
                      [1171, c4d.DTYPE_REAL], # Long Max
                      [1172, c4d.DTYPE_REAL], # Lat Min
                      [1173, c4d.DTYPE_REAL], # Lat Max
                      [1180, c4d.DTYPE_REAL] # Latitude
                    ]

    elif camType == 1057516: # If Redshift camera
        dataVault = [ [903, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], # Position X
                      [903, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], # Position Y
                      [903, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Position Z (etc...)
                      [904, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Rotation
                      [905, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Scale

                      # Basic
                      [901, c4d.DTYPE_LONG], # Visible in Editor
                      [902, c4d.DTYPE_LONG], # Visible in Renderer
                      [907, c4d.DTYPE_LONG], # User Color
                      [908, c4d.DTYPE_REAL, 1000, c4d.DTYPE_COLOR], [908, c4d.DTYPE_REAL, 1001, c4d.DTYPE_COLOR], [908, c4d.DTYPE_REAL, 1002, c4d.DTYPE_COLOR], # Display Color

                      # Object
                      ##[1001, c4d.DTYPE_LONG], # Projection (Cannot be animated)
                      [500, c4d.DTYPE_REAL], # Focal Length
                      ##[4601, c4d.DTYPE_VECTOR], # FOV (Not necessary)
                      [7012, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], # Sensor Shift.X
                      [7012, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], # Sensor Shift.Y
                      ##[7001, c4d.DTYPE_LONG], # Sensor Size Preset
                      [7002, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], # Sensor Size.X
                      [7002, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], # Sensor Size.Y
                      [7004, c4d.DTYPE_BOOL], # Sensor Size Lock Ratio
                      #[7005, c4d.DTYPE_LONG], # Sensor Size Fit (Cannot be animated)
                      [1123, c4d.DTYPE_BOOL], # Near Clip Plane
                      [1122, c4d.DTYPE_REAL], # (Near) Depth
                      [1129, c4d.DTYPE_BOOL], # Affect Lights Only
                      [1128, c4d.DTYPE_REAL], # (Far) Depth

                      # Optical
                      [7016, c4d.DTYPE_LONG], # Exposure Type
                      [1220, c4d.DTYPE_REAL], # Exposure
                      [1231, c4d.DTYPE_REAL], # ISO
                      [7019, c4d.DTYPE_REAL, 1000, c4d.DTYPE_COLOR], # White Point.R
                      [7019, c4d.DTYPE_REAL, 1001, c4d.DTYPE_COLOR], # White Point.G
                      [7019, c4d.DTYPE_REAL, 1002, c4d.DTYPE_COLOR], # White Point.B
                      [1321, c4d.DTYPE_REAL], # Vignetting
                      [1010, c4d.DTYPE_REAL], # Focus Distance
                      ##[1130, c4d.DTYPE_], # Object (Link)
                      #[7901, c4d.DTYPE_REAL], # Offset
                      [1201, c4d.DTYPE_REAL], # Aperture (Fnumber value)
                      [8002, c4d.DTYPE_BOOL], # Bokeh
                      [1300, c4d.DTYPE_LONG], # Diaphragm (Aperture Shape)
                      [1306, c4d.DTYPE_REAL], # Aspect
                      [1303, c4d.DTYPE_REAL], # Spherical Aberration
                      [1301, c4d.DTYPE_LONG], # Blades
                      [1302, c4d.DTYPE_REAL], # Angle
                      ##[8003, c4d.DTYPE_], # Image (RSFile)
                      [8001, c4d.DTYPE_LONG], # Normalization
                      [7017, c4d.DTYPE_LONG], # Shutter Type
                      [8101, c4d.DTYPE_REAL], # Shutter Time
                      [8103, c4d.DTYPE_LONG], # Motion Blur Mode
                      [8104, c4d.DTYPE_BOOL], # Camera Motion
                      [8105, c4d.DTYPE_REAL], # Shutter Offset
                      [1214, c4d.DTYPE_REAL], # Efficiency
                      [8202, c4d.DTYPE_BOOL] # Distortion
                      #[8201, c4d.DTYPE_], # Lens Distortion Image
                      # Color Correction...
                      # Lens Effects...
                      # Display...
                    ]
    return dataVault

def Bake(cameras):
    """ Bake function """

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    fps = doc.GetFps() # Get Frame Rate
    startFrame = doc.GetLoopMinTime().GetFrame(fps) # Get first frame of Preview Range
    endFrame = doc.GetLoopMaxTime().GetFrame(fps) # Get last frame of Preview Range

    for i in range(startFrame, endFrame+1): # Iterate through Preview Range

        #
        progress = u.RangeMap(i, 0, endFrame+1, 0, 100, True)
        c4d.StatusSetText("Baking frame %s of %s" % (i,endFrame+1))
        c4d.StatusSetBar(progress)
        #c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_STATICBREAK) # Updates the viewport during the script runs -> slows down potential baking speed a lot!
        #

        SetCurrentFrame(i, doc) # Set current frame
        frame = doc.GetTime().GetFrame(fps) # Get current frame

        for cam in cameras: # Iterate through cameras

            source = cam[1] # Dummy camera
            target = cam[2] # Bake camera
            dataVault = cam[3] # Data vault

            for data in dataVault: # Iterate through data vault
                if len(data) == 2: # Float
                    desc = c4d.DescID(c4d.DescLevel(data[0], data[1],0))
                    value = source[data[0]] # Dummy camera is the source

                if len(data) == 4: # Vector
                    desc = c4d.DescID(c4d.DescLevel(data[0], data[3],0), c4d.DescLevel(data[2], data[1],0))
                    value = source[data[0],data[2]]

                track = target.FindCTrack(desc) # Try to find CTrack
                if not track: # If CTrack does not exists
                    track = c4d.CTrack(target, desc) # Initialize CTrack
                    target.InsertTrackSorted(track) # Insert CTrack to the bake camera

                curve = track.GetCurve() # Get Curve of the CTrack
                currentTime = c4d.BaseTime(frame, fps) # Get current time
                key = curve.AddKey(currentTime)["key"]
                track.FillKey(doc, target, key)

                if data[1] == c4d.DTYPE_REAL: # Float
                    key.SetValue(curve, value)
                else: # If boolean or integer
                    key.SetValue(curve, value)
                    key.SetGeData(curve, value) # Keyframe value needs to be set with SetGeData

def main():
    """ The first function to run """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    keymod = GetKeyMod() # Get keymodifier
    selected = doc.GetActiveObjects(0) # Get selected objects
    cameras = [] # Collect cameras to an array
    doc.StartUndo() # Start recording undos
    # Collect cameras and do preparation operations
    for s in selected: # Iterate through objects
        if (s.GetType() == 5103) or (s.GetType() == 1057516): # If object is a camera object (standard C4D camera or Redshift camera)
            if s.GetType() == 5103: # If standard C4D camera
                dummyCam = DummyStandardCamera(s, doc) # Dummy camera
                dataVault = GetDataVault(5103) # Get corresponding data vault
            elif s.GetType() == 1057516: # If RS camera
                dummyCam = DummyRedshiftCamera(s, doc) # Dummy camera
                dataVault = GetDataVault(1057516) # Get corresponding data vault
            bakeCam = dummyCam.GetClone() # Bake camera
            name = s.GetName() # Get camera's name
            bakeCam.SetName(name+suffix) # Set baked camera's name
            doc.InsertObject(bakeCam) # Insert camera to document
            doc.AddUndo(c4d.UNDOTYPE_NEW, bakeCam) # Add undo command for creating a new object
            MoveToLast(bakeCam, doc) # Move object to last
            RemoveTags(bakeCam) # Remove tags of the object
            cameras.append([s, dummyCam, bakeCam, dataVault]) # Original camera, dummy camera, camera to bake

    doc.ExecutePasses(None, True, True, True, 0) # Animate the current frame of the document
    Bake(cameras) # Bake the camera (standard C4D camera)
    CleanKeys(cameras) # Clean keyframes

    # Remove dummy cameras
    for i in range(0, len(cameras)):
        cameras[i][1].Remove() # Delete Dummy camera(s)

    # Sort baked cameras
    for i in reversed(range(0, len(cameras))):
        MoveToFirst(cameras[i][2], doc) # Move camera to top of the hierarchy list

    #if keymod == "Shift":
    #    CopyRendererTags(s, bakeCam) # Copies renderer tags from source camera to bake camera

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D
    c4d.StatusClear() # Clear status

# Execute main()
if __name__=='__main__':
    main()