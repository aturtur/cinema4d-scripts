# Aturtur's Cinema 4D Scripts
![AR_Scripts](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/ar_scripts_cover.jpg)

My collection of Python scripts for Maxon Cinema 4D ([@aturtur](https://twitter.com/aturtur)). Almost every script is commented to make learning Python scripting in Cinema 4D faster and easier. You can find more of Cinema 4D related stuff on my [blog](https://aturtur.com/) e.g. Python Generators, Python Effectors, custom Xpresso setups and so on.

Latest version: **1.73** _(Released 24.05.2023)_

## Change Log
**Changes in 1.73**
- _24.05.2023_ Bug fix: AR_PyTagKeepOnFloor
- _06.04.2023_ New script: AR_MoGraphToNulls
- _03.04.2023_ Bug fix: AR_NodeTexToMat

**Older changes**
- _01.04.2023_ New script: AR_F@#kUpNodes (2023 April Fools' Day)
- _28.03.2023_ New script: AR_MatOverride
- _03.03.2023_ New scripts: AR_StabilizeCamera, AR_AverageLocator, AR_CycleCameras
- _27.02.2023_ Updated: AR_ViewportColor, More presets, async GeDialog instead of modal
- _18.02.2023_ Updated: AR_Folder, fixed adopt layer bug
- _10.01.2023_ New scripts: AR_CameraPlane, AR_ExportUVTex, AR_KeysSetPosX, AR_KeysSetPosY, AR_KeysSetPosZ, AR_KeysSetRotB, AR_KeysSetRotH, AR_KeysSetRotP, AR_KeysSetSclX, AR_KeysSetSclY, AR_KeysSetSclZ
- _20.11.2022_ Updated: AR_ExportMat, added progress bar
- _18.11.2022_ Updated: AR_BakeCam, AR_BakePLA, AR_BakePSR, progress bar added, parallel processing
- _18.11.2022_ Updated: AR_SelectDeepest, AR_SelectDown, AR_SelectNext, AR_SelectPrev, AR_SelectRoot, AR_SelectUp, better support for hotkeys
- _17.11.2022_ Updated: AR_ExportC4D, AR_ExportOBJ, progress bar
- _17.11.2022_ Updated: AR_Folder, fixed bug when user cancels picking a custom color
- _16.11.2022_ Updated: AR_Dot, Added option to change the color
- _15.11.2022_ Updated: AR_NodeAdd, fixed AOV port
- _10.11.2022_ Updated: AR_BakeCamera and AR_AspectRatioGuide, support for Redshift Camera object (new in C4D 2023.1.0)
- _08.11.2022_ Updated: AR_ViewportColor, dialog for presets. AR_RandomColors, option to colorize objects with a gradient
- _02.11.2022_ New script: AR_ColorizeLayersWithGradient
- _01.11.2022_ New script: AR_ExportMat  
- _24.09.2022_ Updated: AR_TglEnable, support for Insydium NeXus stuff, fixed script name
- _24.09.2022_ Updated: AR_Dot, darker icon
- _16.09.2022_ New script: AR_PyTagShowIfActiveCam
- _16.09.2022_ Updated: AR_DynaMesh, added support for material
- _16.09.2022_ Updated: AR_Folder, added support for Cinema 4D 2023
- _23.08.2022_ New script: AR_ViewportColor
- _19.08.2022_ Updated: AR_PyTagShowIfActive, added option to choose between "Selected" and " Active"
- _18.08.2022_ Updated: AR_TagsSelect, if tag selection -> search and select that tag type
- _18.08.2022_ Scripts comeback: AR_RemoveMissingTextureTags, AR_SelectSameColor
- _18.08.2022_ Updated: AR_Dot, if object selection, create dot null after every selected object
- _19.05.2022_ New script: AR_NodeTexToMat
- _06.05.2022_ Updated: AR_NodeAdd, added Change Range node
- _03.05.2022_ New script: AR_AbsRenderPaths
- _03.05.2022_ Bug fix: AR_AspectRatioGuide
- _02.05.2022_ Updated: AR_AspectRatioGuide
- _02.05.2022_ Major bug fix: AR_OpenRenderFolder
- _02.05.2022_ New scripts: AR_Dot, AR_PyTagShowGivenFrames
- _29.04.2022_ New scripts: AR_KeysAlign, AR_KeysValueAdd, AR_KeysValueSub, AR_NodeResize
- _29.04.2022_ Updated: AR_KeysMoveL, AR_KeysMoveL (saves custom step and sets it as default value), AR_BakePLA
- _26.04.2022_ New script: AR_OpenProjectFolder
- _26.04.2022_ Bug fixes: AR_TracksRemap, AR_OpenRenderFolder
- _25.04.2022_ Minor fix: AR_OpenBugReportsFolder
- _25.04.2022_ New scripts: AR_DeleteARPrefs, AR_SortABC, AR_SortRandom
- _22.04.2022_ New script: AR_PyTagShowIfCorrectCam
- _21.04.2022_ New scripts: AR_FlipIt, AR_PyTagAlignToSpline
- _20.04.2022_ New script: AR_DynaMesh (requires C4D 26)
- _15.04.2022_ **Initial version of AR_Scripts for R25**

## How to use
In this section I go through how you install AR_Scripts to  Cinema 4D. These scripts are written for Maxon Cinema 4D 2023.1.0 and Python 3.9.1. Scripts are tested using Microsoft Windows 11. All of the scripts should be compatible also with Mac OS. I'm not writing scripts anymore for older Cinema 4D versions.

_Use these scripts with your own risk!_

### Installation
Download this [repo](https://github.com/aturtur/cinema4d-scripts/archive/master.zip) and put AR_Scripts_#.##\_R25 folder to following path:

#### Windows
`C:\Users\<USER>\AppData\Roaming\MAXON\Maxon Cinema 4D RXX\library\scripts`

#### Mac OS
`/Applications/MAXON/CINEMA 4D RXX/library/scripts`

Other way to find folder for installing scripts is to opening C4D and opening preferences (Ctrl+E / Cmd+E) and pressing 'Open Preferences Folder...' -button and navigating to library > scripts.

#### Addendum 
Some of the scripts will make a txt-files in the aturtur folder under the C4D's prefs folder to save the previous settings of the script.
`C:\Users\<USER>\AppData\Roaming\MAXON\Maxon Cinema 4D RXX\prefs\aturtur`
If/when you want to uninstall AR_Scripts completely, remove that folder too.

### Using scripts
When you have installed AR_Scripts you have to reboot Cinema 4D if it is already running. On start up Cinema 4D will scan and load all of the scripts. Scripts are located under Extensions -> User Scripts -> AR_Scripts_#.##\_R25. Scripts can be used with the commander (Shift+C) too.

You run the script by clicking it. Some of the scripts have multiple functions and you can use those with key modifiers (Alt / Ctrl / Shift) and different combinations. Some of the scripts requires a certain item selection or mode to be active. If you don't know what the script does you can either open the script in the script editor and read the description or search the info of the specific script on this page.

# Script descriptions

## Animation
### ![AR_BakeCam](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_BakeCam.png) AR_BakeCam.py
**Default:** Bakes selected camera(s) to world space.  
**Shift:** Keeps render engine tags if any.  

### ![AR_BakePLA](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_BakePLA.png) AR_BakePLA.py
**Default:** Bakes object to Point Level Animation (PLA).  
To bake spline object correctly, bake them first to alembic and then use this script to bake the alembic file to PLA spline object.  
It's important that 'Intermediate Points' is set to 'Uniform'! The script does not support that the point number is changing over time.  

### ![AR_BakePSR](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_BakePSR.png) AR_BakePSR.py
**Default:** Bakes selected object(s) to PSR animation in the world space.  
**Shift:** Bakes selected object(s) to PSR animation in the local space.  

### ![AR_KeysDistribute](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysDistribute.png) AR_KeysDistribute.py
**Default:** Distributes selected keyframes evenly.  
**Shift:** Distributes selected keyframes by given step (in frames).  
Requires at least three (3) selected keyframes to correctly function. Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_KeysAlign](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysAlign.png) AR_KeysAlign.py
**Default:** Aligns selected keyframes to the closest whole frame.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_KeysMoveL](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysMoveL.png) AR_KeysMoveL.py
**Default:** Move selected keyframe(s) to the left.  
**Shift:** Set custom value as default (shared with AR_KeysMoveR).  
**Ctrl:** Move selected keyframe(s) by the set value multiplied by 2 to the left.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_KeysMoveR](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysMoveR.png) AR_KeysMoveR.py
**Default:** Move selected keyframe(s) to the right.  
**Shift:** Set custom value as default (shared with AR_KeysMoveL).  
**Ctrl:** Move selected keyframe(s) by the set value multiplied by 2 to the right.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetPosX.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetPosY.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetPosZ.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetRotH.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetRotB.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetRotP.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetSclX.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetSclY.png) ![AR_KeysSet](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysSetSclZ.png) AR_KeysSet...
**Default:** Scripts to set individually position, scale or rotation keyframe for wanted axis for selected object(s).  

### ![AR_KeysValueAdd](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysValueAdd.png) AR_KeysValueAdd.py
**Default:** Increases selected keyframe(s) value.  
**Shift:** Set custom value as default (shared with AR_KeysValueSub).  
**Ctrl:** Increases selected keyframe(s) value times 2.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_KeysValueSub](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_KeysValueSub.png) AR_KeysValueSub.py
**Default:** Decreases selected keyframe(s) value.  
**Shift:** Set custom value as default (shared with AR_KeysValueAdd).  
**Ctrl:** Decreases selected keyframe(s) value times 2.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_TracksRemap](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TracksRemap.png) AR_TracksRemap.py
Adds special track: Time for selected track(s) for time remapping.  
**Default:** Time track is set to absolute.  
**Shift:** time track is set to relative.  
Use in dope sheet editor, does not work in f-curve editor.  

### ![AR_TracksSequence](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TracksSequence.png) AR_TracksSequence.py
**Default:** Sequences selected animation tracks.  
**Shift:** Sequences selected animation tracks with a given gap (in frames).  
**Ctrl:** Sequencing is reversed.  
**Shift+Ctrl:** Reversed sequencing with a given gap.  
Requires at least two (2) selected tracks to correctly function. Use in dope sheet editor, does not work in f-curve editor.  

## Camera
### ![AR_AspectRatioGuide](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_AspectRatioGuide.png) AR_AspectRatioGuide.py
**Default:** Creates an aspect ratio guide for selected camera(s).  
Requires at least one (1) selected camera object to correctly function.  

### ![AR_CameraPlane](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_CameraPlane.png) AR_CameraPlane.py
**Default:** Creates plane object that matches selected camera(s) field of view. Positioned to cameras focal point in Z-axis.  
Supports perspective and parallel projections.  

### ![AR_CropToIRR](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_CropToIRR.png) AR_CropToIRR.py
**Default:** Crops the canvas to Interactive Render Region.  
Changes active render settings resolution and selected/active camera's sensor size (film gate) and possibly also film offsets.  

### ![AR_ResizeCanvas](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ResizeCanvas.png) AR_ResizeCanvas.py
**Default:** Cycles through available cameras.  
**Shift:** Cycles cameras backwards.  

### ![AR_CycleCameras](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_CycleCameras.png) AR_CycleCameras.py
**Default:** Resizes the canvas without changing the perspective.  
Changes active render settings resolution and selected/active camera's sensor size or focal length and possibly also film offsets.  

### ![AR_SelectActiveCamera](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectActiveCamera.png) AR_SelectActiveCamera.py
**Default:** Selects the active camera in the object manager.  

### ![AR_StabilizeCamera](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_StabilizeCamera.png) AR_StabilizeCamera.py
**Default:** Stabilizes active camera view to selected object.  
Designed to use with AR_AverageLocator.  

## Export
### ![AR_ExportAISeq](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ExportAISeq.png) AR_ExportAISeq.py
**Default:** Exports selected spline objects to Adobe Illustrator-sequence.  
**Shift:** Export selected spline objects to separated folders (separated sequences).  
Preview range will determine the frame range that will be exported.  

### ![AR_ExportC4D](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ExportC4D.png) AR_ExportC4D.py
**Default:** Exports top level objects individually to C4D-file. Supports object selection.  

### ![AR_ExportMat](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ExportMat.png) AR_ExportMat.py
**Default:** Exports selected material(s) to own file(s).
>Note: Material names should NOT end with dot and number! Eg. "MyMaterial.1" rename that to "MyMaterial_1" or something different. Currently the script does not copy textures to the export location, use global paths!  

### ![AR_ExportOBJ](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ExportOBJ.png) AR_ExportOBJ.py
**Default:** Exports top level objects individually to OBJ-file. Supports object selection.  

### ![AR_ExportUVTex](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ExportUVTex.png) AR_ExportUVTex.py
**Default:** Exports UV texture for selected object. Remember to select polygons of the object first!  

## Import
### ![AR_ImportfSpy](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportfSpy.png) AR_ImportfSpy.py
**Default:** Creates a camera from fSpy JSON-file and Background object from a Image-file.  

### ![AR_ImportImageFolder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportImageFolder.png) AR_ImportImageFolder.py
**Default:** Imports an image folder into materials.  
**Shift:** Generates also plane objects for each material with correct proportion of the image.  

### ![AR_ImportOBJFolder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportOBJFolder.png) AR_ImportOBJFolder.py
**Default:** Merges OBJ-files from selected folder into the active document.  

### ![AR_ImportPixeur](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportPixeur.png) AR_ImportPixeur.py
**Default:** Creates materials from Pixeur color palette file.  

### ![AR_ImportPSD](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportPSD.png) AR_ImportPSD.py
**Default:** Imports PSD-file's layers into separate materials.  
**Shift:** Generates also plane-objects for each layer.  

### ![AR_ImportSound](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ImportSound.png) AR_ImportSound.py
**Default:** Imports sound-file and places it to the current time.  

## Materials
### ![AR_MatConsolidateTags](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MatConsolidateTags.png) AR_MatConsolidateTags.py
**Default:** Consolidates different polygon selections together that uses same materials.  
>Note: Messes up material projections! Select object(s) and run the script.  

### ![AR_MatOverride](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MatOverride.png) AR_MatOverride.py
**Default:** Overrides selected materials with the top of the list selected material.  

### ![AR_MatOverride](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MatMerge.png) AR_MatMerge.py
**Default:** Merges materials that has the same name.  
Case sensitive. Supports Cinema 4D's naming conventions. The first material in the material manager overrides the other ones (with the same name).  

### ![AR_MatOwn](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MatOverride.png) AR_MatOverride.py
**Default:** Overrides selected materials with the top of the list selected material.  

### ![AR_MatToObject](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MatToObject.png) AR_MatToObject.py
**Default:** Puts material to object if they have a same name.  

## Modeling
### ![AR_AxisToOrigin](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_AxisToOrigin.png) AR_AxisToOrigin.py
**Default:** Sets object's axis to world origin.  
Currently does not support objects with exposed normal tags.  

### ![AR_BooleSplit](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_BooleSplit.png) AR_BooleSplit.py
**Default:** Splits selected objects in half.  

### ![AR_DropToFloor](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_DropToFloor.png) AR_DropToFloor.py
**Default:** Places the object on the floor.  

### ![AR_DynaMesh](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_DynaMesh.png) AR_DynaMesh.py
**Default:** Remeshes selected object with ZRemesher.  
**Shift:** Dialog to set different options. Options will be saved.  
>Note: Requires Cinema 4D S26 or newer!

### ![AR_FlipIt](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_FlipIt.png) AR_FlipIt.py
**Default:** Flips selected object(s) (multiplies specific axis by -1).  
**Shift:** Dialog to set different options, like space, which axis to flip and make a copy of the original object. Options will be saved.  

### ![AR_Guide](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Guide.png) AR_Guide.py
**Default:** Creates a guide object from two selected objects, points or edge.  

### ![AR_NullsControl](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NullsControl.png) AR_NullsControl.py
**Default:** Creates null(s) from selected point(s) that can control the original geometry.  

### ![AR_NullsSticky](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NullsSticky.png) AR_NullsSticky.py
**Default:** If point selection: Creates null(s) with constraint tag(s) (clamp) from selected point(s).  
**Default:** If object selection: Creates null(s) with constraint tag(s) (PSR) from selected object(s).  

### ![AR_ObjectReplace](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ObjectReplace.png) AR_ObjectReplace.py
**Default:** Replaces objects with instance of the first selected object.  
**Shift:** Replace objects with instances of the last selected object.  
**Ctrl:** Replace objects with copies of the first selected object.  
**Shift+Ctrl:** Replace objects with copies of the last selected object.  

### ![AR_ObjectToSpline](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ObjectToSpline.png) AR_ObjectToSpline.py
**Default:** Converts selected object(s) to splines.  
**Shift:** Keep the original object(s).  

### ![AR_PlaceNull](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PlaceNull.png) AR_PlaceNull.py
Creates null to current axis matrix.  
**Default:** Selects the new null object and deselects the old selection.  
**Shift:** Does not change the current selection.  

### ![AR_PointCloud](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PointCloud.png) AR_PointCloud.py
**Default:** Creates a point cloud (polygon object with only points) from selected objects' positions.  

### ![AR_PolySplit](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PolySplit.png) AR_PolySplit.py
**Default:** Splits the object into pieces by polygon selection tag(s).  

### ![AR_Swap](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Swap.png) AR_Swap.py
**Default:** Swaps selected objects between each other (transformation).  
**Shift:** Generates a dialog where you can pick specifically what properties to swap.  
**Ctrl:** Swaps selected objects only in the object manager.  
Requires just two (2) selected objects.  

### ![AR_VertexMapCreate](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_VertexMapCreate.png) AR_VertexMapCreate.py
**Default:** Creates a vertex map tag for selected object(s).  
**Shift:** Creates also linear falloff field to control the vertex map.  

### ![AR_VertexMapInvert](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_VertexMapInvert.png) AR_VertexMapInvert.py
**Default:** Inverts selected Vertex Map tag's data.  

## MoGraph
### ![AR_FindEffectors](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_FindEffectors.png) AR_FindEffectors.py
**Default:** Selects MoGraph Effector(s) that use(s) selected Field object. Selects MoGraph Effector(s) that are used in selected Generator object.  
Does not support subfields or tags!  

### ![AR_FindGenerators](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_FindGenerators.png) AR_FindGenerators.py
**Default:** Selects MoGraph generator(s) that use(s) selected effector. Prints info also to console.  


### ![AR_MoGraphToNulls](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MoGraphToNulls.png) AR_MoGraphToNulls.py
**Default:** Creates MoGraph to nulls setup.  
**Shift:** User input for custom index.   

### ![AR_MoSelection](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MoSelection.png) AR_MoSelection.py
**Default:** Creates MoGraph selection for every clone.  
**Shift:** Shared tag for given IDs.  
**Ctrl:** Individual tags for given IDs.  

### ![AR_MoSelectionMerge](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MoSelectionMerge.png) AR_MoSelectionMerge.py
**Default:** Merges selected MoGraph Selection Tags into one tag.  
>Note: If you have nested MoGraph Generators, disable parent generators before running this script.  

## Node Tools
### ![AR_F@#kUpNodes](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_FkUpNodes.png) AR_F@#kUpNodes.py
**Default:** Messes position of selected nodes (2023 April Fools' Day).  
>Works only with Redshift. Make sure the Redshift material is selected when using the script!  

### ![AR_NodeAdd](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeAdd.png) AR_NodeAdd.py
**Default:** Adds node between selected nodes.  
>Works only with Redshift. Make sure the Redshift material is selected when using the script!  

### ![AR_NodeAlignH](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeAlignH.png) AR_NodeAlignH.py
Aligns selected graph nodes horizontally.  
**Default:** The leftmost node rules. Pivot is in the middle.  
**Shift:** The leftmost node rules. Pivot is in the top.  
**Ctrl:** The leftmost node rules. Pivot is in the bottom.  
**Alt:** The rightmost node rules. Pivot is in the middle.  
**Alt+Shift:** The rightmost node rules. Pivot is in the top.  
**Alt+Ctrl:** The rightmost node rules. Pivot is in the bottom.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeAlignV](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeAlignV.png) AR_NodeAlignV.py
Aligns selected graph nodes vertically.  
**Default:** The topmost node rules. Pivot is in the middle.  
**Shift:** The topmost node rules. Pivot is in the left.  
**Ctrl:** The topmost node rules. Pivot is in the right.  
**Alt:** The lowest node rules. Pivot is in the middle.  
**Alt+Shift:** The lowest node rules. Pivot is in the left.  
**Alt+Ctrl:** The lowest node rules. Pivot is in the right.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeCon](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeCon.png) AR_NodeCon.py
**Default:** Connects two selected nodes, if possible. Starting from the top.  
**Shift:** Custom input to connect OUT and IN port.  
**Ctrl:** Connects two selected nodes, if possible. Starting from the bottom.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeDiscon](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeDiscon.png) AR_NodeDiscon.py
**Default:** Disconnect all connection(s) of selected node or connection(s) between selected nodes.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeDstrbH](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeDstrbH.png) AR_NodeDstrbH.py
**Default:** Distributes selected nodes horizontally.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeDstrbV](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeDstrbV.png) AR_NodeDstrbV.py
**Default:** Distributes selected nodes vertically.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeLineUpH](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeLineUpH.png) AR_NodeLineUpH.py
**Default:** Lines up selected graph nodes horizontally.  
**Shift:** Lines up selected graph nodes horizontally with a custom gap.  
**Alt:** Reversed direction.  
**Shift+Alt:** Reversed direction with a custom gap.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeLineUpV](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeLineUpV.png) AR_NodeLineUpV.py
**Default:** Lines up selected graph nodes vertically.  
**Shift:** Lines up selected graph nodes vartically with a custom gap.  
**Alt:** Reversed direction.  
**Shift+Alt:** Reversed direction with a custom gap.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeResize](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeResize.png) AR_NodeResize.py
**Default:** Resizes selected nodes by given width and height values.  
Supports Xpresso and Redshift.  
>Notice: Make sure the Xpresso tag or the Redshift material is selected when using the script!  

### ![AR_NodeTexPSR](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeTexPSR.png) AR_NodeTexPSR.py
**Default:** Creates individual scale, offset and rotate control nodes for Redshift texture and triplanar nodes.  
**Shift:** Add only scale controller.  
**Ctrl:** Add only offset controller.  
**Alt:** Add only rotation controller.  
Works only with Redshift.  
>Notice: Make sure the Redshift material is selected when using the script!  

### ![AR_NodeTexToMat](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_NodeTexToMat.png) AR_NodeTexToMat.py
**Default:** Creates material node from selected texture nodes or connects selected texture nodes to selected materials.  
**Shift:** Change settings.  
Works only with Redshift.  
>Notice: Make sure the Redshift material is selected when using the script!  

## Object Manager
### ![AR_CopyToChild](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_CopyToChild.png) AR_CopyToChild.py
Creates a copy from object to the rest of the selected objects.  
**Default:** Copy the first selected object.  
**Shift:** Copy the last selected object.  
**Ctrl:** Instance the first selected object.  
**Shift+Ctrl:** Instance the last selected object.  

### ![AR_FindSource](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_FindSource.png) AR_FindSource.py
**Default:** Selects the source object.  
Supports Instance, Connect, MoInstance, MoSpline, Cloner and Matrix objects.  

### ![AR_MergeSelectionTags](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_MergeSelectionTags.png) AR_MergeSelectionTags.py
**Default:** Merges selection tags.  
Supports object and tag selections.  

### ![AR_RandomColors](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_RandomColors.png) AR_RandomColors.py
**Default:** Gives a random display color to selected object(s).  
**Shift:** Gives a random grayscale display color to selected object(s).  
**Ctrl:** Colorize objects randomly based on a custom gradient.   
**Alt:** Reset color.  

### ![AR_RemoveEmptySelectionTags](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_RemoveEmptySelectionTags.png) AR_RemoveEmptySelectionTags.py
**Default:** Removes empty selection tags from selected object(s) or from all objects if no selection.  

### ![AR_RemoveMissingTextureTags](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_RemoveMissingTextureTags.png) AR_RemoveMissingTextureTags.py
**Default:** Removes missing texture tags. If selection, removes only from selected objects.  

### ![AR_SelectByVisibility](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectByVisibility.png) AR_SelectByVisibility.py
**Default:** Selects objects by visibility.  

### ![AR_SelectChildren](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectChildren.png) AR_SelectChildren.py
**Default:** Select children of selected object(s).  
**Shift:** Keeps original selection.  
**Ctrl:** Select children from custom level.  
**Alt:** Select siblings from given level (ignore their children).  

### ![AR_SelectCousins](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectCousins.png) AR_SelectCousins.py
**Default:** Selects the object's cousins.  
**Ctrl:** Selects the object's cousins and deselects the original selection.  

### ![AR_SelectDeepest](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectDeepest.png) AR_SelectDeepest.py
**Default:** Select children of selected object(s) that are the most deep in hierarchy.  
**Shift:** Keep the original selection.  

### ![AR_SelectDown](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectDown.png) AR_SelectDown.py
**Default:** Goes down one hierarchy level.  
**Shift:** Keeps the old selection.  

### ![AR_SelectNext](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectNext.png) AR_SelectNext.py
**Default:** Selects the next object.  
**Shift:** Keeps the old selection.  

### ![AR_SelectNth](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectNth.png) AR_SelectNth.py
**Default:** Selects every even object.  
**Shift:** Selects every odd object.  
**Ctrl:** Selects every nth object.  
**Alt:** Selects every nth object inverted.  
**Shift+Ctrl:** Keep random n.  

### ![AR_SelectPrev](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectPrev.png) AR_SelectPrev.py
**Default:** Selects the previous object.  
**Shift:** Keeps the old selection.  

### ![AR_SelectRoot](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectRoot.png) AR_SelectRoot.py
**Default:** Selects the root object of the object.  
**Shift:** Keeps the old selection.  

### ![AR_SelectSameColor](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectSameColor.png) SelectSameColor.py
**Default:** Selects objects that has same display color as the selected object.  

### ![AR_SelectSiblings](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectSiblings.png) AR_SelectSiblings.py
**Default:** Selects the object's siblings.  
**Ctrl:** Selects the object's siblings and deselects the original selection.  

### ![AR_SelectUp](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SelectUp.png) AR_SelectUp.py
**Default:** Selects the parent object.  
**Shift:** Keeps the old selection.  

### ![AR_SortABC](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SortABC.png) AR_SortABC.py
**Default:** Sorts selected objects order alphabetically (descending) in the object manager.  
**Shift:** Sorts selected objects order alphabetically (ascending) in the object manager.  
Note: Objects has to be in the same level in the object manager.  

### ![AR_SortRandom](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_SortRandom.png) AR_SortRandom.py
**Default:** Randomizes selected objects order in the object manager.  
Note: Objects has to be in the same level in the object manager.  

### ![AR_TagsClone](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TagsClone.png) AR_TagsClone.py
**Default:** Clone selected tag(s) to selected object(s).  

### ![AR_TagsCloneHierarchy](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TagsCloneHierarchy.png) AR_TagsCloneHierarchy.py
**Default:** Clones specific tags from first selected hierarchy to second selected hierarchy.  
Hierarcies has to be indetical!  

### ![AR_TagsDelete](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TagsDelete.png) AR_TagsDelete.py
**Default:** Removes selected tag type from selected objects. If no object selection. Selected tag type will be removed from all objects.  

### ![AR_TagsSelect](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TagsSelect.png) AR_TagsSelect.py
**Default:** Selects tag(s) of selected object(s). If only tags selected, selects that type of tags from other objects. You can also restrict the tag search with object selection.  

### ![AR_TagsShift](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TagsShift.png) AR_TagsShift.py
Shifts selected tag(s).  
**Default:** Shifts selected tag(s) to the right.  
**Shift:** Shifts selected tag(s) to the left.  

## Python Tags
### ![AR_PyTagAlignToSpline](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagAlignToSpline.png) AR_PyTagAlignToSpline.py
**Default:** Adds a custom python tag for selected object(s) that works like C4D's Align To Spline tag but this one works also with deformed spline.  

### ![AR_PyTagKeepOnFloor](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagKeepOnFloor.png) AR_PyTagKeepOnFloor.py
**Default:** Adds a custom python tag for selected object(s) that keeps the object on the floor.  

### ![AR_PyTagShowGivenFrames](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagShowGivenFrames.png) AR_PyTagShowGivenFrames.py
**Default:** Adds a custom python tag for selected object(s) that toggles object's visibility by given frames.  
There's some variables you can use: **start** and **end** for global start and end frames, **prevstart** and **prevend** for preview range start end end frames.  
Set frame range with dash (-) and separate different frames and ranges with a comma (,).  

### ![AR_PyTagShowIfActive](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagShowIfActive.png) AR_PyTagShowIfActive.py
**Default:** Adds a custom python tag for selected object(s) that shows the object only if it is active.  

### ![AR_PyTagShowIfActiveCam](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagShowIfCorrectCam.png) AR_PyTagShowIfActiveCam.py
**Default:** Adds a custom python tag for selected object(s) that shows and hides camera if it is active or not.  

### ![AR_PyTagShowIfCorrectCam](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagShowIfCorrectCam.png) AR_PyTagShowIfCorrectCam.py
**Default:** Adds a custom python tag for selected object(s) that shows and hides object based on assigned camera.  

### ![AR_PyTagShowWhenAnimated](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PyTagShowWhenAnimated.png) AR_PyTagShowWhenAnimated.py
**Default:** Adds a custom python tag for selected object(s) that shows the object only when it is animated.  

## Tracking
### ![AR_AverageLocator](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_AverageLocator.png) AR_AverageLocator.py
**Default:** Creates a null object which position is average of selected objects/points.  

### ![AR_Extract2DTracks](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Extract2DTracks.png) AR_Extract2DTracks.py
Extracts 2D tracks from selected motion tracker to null objects.  
**Default:** Extracts only manual tracks.  
**Shift:** Extracts only auto tracks.  

## Utility
### ![AR_AbsRenderPaths](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_AbsRenderPaths.png) AR_AbsRenderPaths.py
**Default:** Converts relative render paths to absolute paths.  
For example: Cinema 4D's native Render Queue does not work with relative render paths, so this scripts helps to convert render paths.  

### ![AR_ColorizeLayersWithGradient](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ColorizeLayersWithGradient.png) AR_ColorizeLayersWithGradient.py
**Default:** Colorizes selected layers with custom gradient.  

### ![AR_DeleteARPrefs](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_DeleteARPrefs.png) AR_DeleteARPrefs.py
**Default:** Deletes aturtur folder inside prefs folder, where some of scripts saves user's custom settings.  
**Shift:** Opens the folder location.  

### ![AR_Dot](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Dot.png) AR_Dot.py
**Default:** Creates a dark null that has no name.  

### ![AR_Folder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Folder.png) AR_Folder.py
**Default:** Creates a folder null that keeps your project nice and tidy.  

### ![AR_OpenBugReportsFolder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_OpenBugReportsFolder.png) AR_OpenBugReportsFolder.py
**Default:** Opens the bug reports folder.  

### ![AR_OpenProjectFolder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_OpenProjectFolder.png) AR_OpenProjectFolder.py
**Default:** Opens the folder where the project file is saved.  

### ![AR_OpenRenderFolder](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_OpenRenderFolder.png) AR_OpenRenderFolder.py
**Default:** Opens the folder where the project is rendered.  
>The folder must exist already! Does not support all of the tokens!  

### ![AR_PrintType](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_PrintType.png) AR_PrintType.py
**Default:** Prints info about selected objects, tags, materials, Xpresso nodes and Redshift nodes.  

### ![AR_TglEnable](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TglEnable.png) AR_TglEnable.py
**Default:** Toggle selected generator object (enable / disable).  
**Shift:** Toggle next found parent generator object from the default list.  
**Ctrl:** Toggle the root generator object.  
**Alt:** Toggle all parent generators from common list.  
**Alt+Shift:** Force disable.  
**Alt+Ctrl:** Force enable.  
**Shift+Ctrl:** Toggle from custom list.  
**Alt+Ctrl+Shift:** Open textfile to modify custom. You can use hashtag '#' separating comments. Put each generator to separate line!  
>Highly recommended to assign this script to a keyboard shortcut!  

## Viewport
### ![AR_ReferenceViewport](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ReferenceViewport.png) AR_ReferenceViewport.py
**Default:** Creates a viewport for animation reference.  
**Shift:** Create only background.  
**Ctrl:** Delete existing setup.  
The script requires and enables 'Full Animation Redraw' in Preferences/View.  

### ![AR_Safeframes](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_Safeframes.png) AR_Safeframes.py
**Default:** Toggle opacity of safeframes in viewport.  
**Shift:** Set a custom value and color.  
>Note: The color pickers in modal dialogs are currently broken in C4D R25, hopefully Maxon will fix this bug someday...  

### ![AR_TglGrid](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_TglGrid.png) AR_TglGrid.py
**Default:** Toggle ground grid visibility in the active viewport.  
**Shift:** Toggle in all viewports.  

### ![AR_ViewportColor](https://raw.githubusercontent.com/aturtur/cinema4d-scripts/master/img/AR_ViewportColor.png) AR_ViewportColor.py
**Default:** Opens a dialog where you can select a preset to change viewport color.
**Alt+Ctrl+Shift:** Open textfile to modify custom. Use hashtag '#' separating preset name. Put each color code to separate line!  

## Modules
### ar_shelf_tool.py
More information here: [Shelf tool script for Cinema 4D](https://aturtur.com/shelf-tool-script-for-cinema-4d/)
Version: 1.0.4
Latest update: Alt+Ctrl+Shift keymodifier opens the asset document (for modification purpose)

## Support the project
If you find these scripts useful, consider to supporting the project and keeping it up and running: [Tip jar](https://paypal.me/aturtur).

If you have any script ideas, you can DM me at [Twitter](https://twitter.com/aturtur).