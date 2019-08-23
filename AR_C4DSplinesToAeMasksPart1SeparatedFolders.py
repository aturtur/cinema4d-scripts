"""
AR_C4DSplinesToAeMasksPart1SeparatedFolders

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_C4DSplinesToAeMasksPart1SeparatedFolders
Description-US: Exports selected spline objects to AI-sequence in separated folders. Preview range will determine which frames will be exported. The script will create a new folder for each selected object so be extra carefully with object names and selections!
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d, os
from c4d import plugins

# Functions
def main():
    # ---------------------------------------------------------------------------------------------------
    # Setup and export AI-sequence with Sketch and Toon
    fn = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select Save Path", flags=c4d.FILESELECT_DIRECTORY) # Select path to save        
    if not fn: return # If cancelled stop the script
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    renderData = doc.GetActiveRenderData() # Get document render data
    currVideoPost = renderData.GetFirstVideoPost() # Get first render effect
    sntFound = False # Initialize variable for storing info is 'Sketch and Toon' effect enabled already
    while currVideoPost is not None: # Loop through render effects
        if currVideoPost.GetType() == 1011015: # If 'Sketch and Toon' effect found
            sntFound = True # Set variable to true
        currVideoPost = currVideoPost.GetNext() # Get next render effect on list
    if sntFound == False: # If 'Sketch and Toon' effect is not enabled already
        sketchEffect = c4d.documents.BaseVideoPost(1011015) # Initialize 'Sketch and Toon' effect
        renderData.InsertVideoPostLast(sketchEffect) # Add 'Sketch and Toon' effect to render settings
    sketchMat = c4d.BaseMaterial(1011014) # Initialize 'Sketch Material'
    doc.InsertMaterial(sketchMat) # Insert material to document
    sketchTags = [] # Initialize list for 'Sketch Style' tags
    # ---------------------------------------------------------------------------------------------------
    # Export plug-in settings
    plug = plugins.FindPlugin(1012074, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return
    data = {}
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
        if "imexporter" not in data:
            return
        aiExport = data["imexporter"]
        if aiExport is None:
            return
        # Change Illustrator export settings
        aiExport[c4d.TUAIEXPORT_OUTPUTSIZE] = 0 # Output: Render
        aiExport[c4d.TUAIEXPORT_ZSORT] = 0
        aiExport[c4d.TUAIEXPORT_SCALE] = 1 # Scale: 100%
        aiExport[c4d.TUAIEXPORT_EXPORTLINES] = 1 # Export lines
        aiExport[c4d.TUAIEXPORT_LINEOPACITY] = 0 # Disable line opacity
        aiExport[c4d.TUAIEXPORT_LINETHICKNESS] = 0 # Disable line thickness
        aiExport[c4d.TUAIEXPORT_LINEPATTERNS] = 0 # Disable line patterns
        aiExport[c4d.TUAIEXPORT_LINECONNECTIONS] = 1 # Enable line connections
        aiExport[c4d.TUAIEXPORT_EXPORTSURFACE] = 0 # Disable surface export
        aiExport[c4d.TUAIEXPORT_ANIMATION] = 1 # Export animation
        aiExport[c4d.TUAIEXPORT_ANIMTYPE] = 0 # Output As: Files
        aiExport[c4d.TUAIEXPORT_FRAMES] = 2 # Frames: Manual
        aiExport[c4d.TUAIEXPORT_FRAME_START] = doc.GetLoopMinTime() # Animation first frame
        aiExport[c4d.TUAIEXPORT_FRAME_END] = doc.GetLoopMaxTime() # Animation last frame
        aiExport[c4d.TUAIEXPORT_FRAME_RATE] = doc.GetFps() # Frame rate
    # ---------------------------------------------------------------------------------------------------
    # Handle selected objects
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get selected objects
    for i in xrange(0, len(selection)): # Loop through selected objects
        #sketchTags.append(c4d.BaseTag(1011012)) # Insert 'Sketch Style' tag to sketchTags list
        sketchTag = c4d.BaseTag(1011012) # Initialize a sketch tag
        sketchTag[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat # Put sketch material to sketch tag
        sketchTag[c4d.OUTLINEMAT_LINE_SPLINES] = 1 # Enable splines
        sketchTag[c4d.OUTLINEMAT_LINE_FOLD] = 0 # Disable fold
        sketchTag[c4d.OUTLINEMAT_LINE_CREASE] = 0 # Disable crease
        sketchTag[c4d.OUTLINEMAT_LINE_BORDER] = 0 # Disable border
        selection[i].InsertTag(sketchTag) # Insert sketch tag to selected object
        # ---------------------------------------------------------------------------------------------------
        folderPath = os.path.splitext(fn)[0] # Folder path
        objectName = selection[i].GetName() # Get object name
        os.mkdir(folderPath+"\\"+objectName) # Create new folders
        fullFilePath = folderPath+"\\"+objectName+"\\"+objectName+".ai" # Full file path
        c4d.documents.SaveDocument(doc, fullFilePath, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1012074) # Export AI-file
        sketchTag.Remove() # Delete sketch tag
    # ---------------------------------------------------------------------------------------------------
    # Remove unnecessary stuff
    #for st in sketchTags: # Loop through sketchTags
        #st.Remove() # Remove 'Sketch Style' tag
    sketchMat.Remove() # Remove 'Sketch Material'
    if sntFound == False: # If there was not 'Sketch and Toon' render effect already
        sketchEffect.Remove() # Remove 'Sketch and Toon' render effect
    # ---------------------------------------------------------------------------------------------------
    c4d.StatusClear() # Clear status bar
    c4d.StatusSetText("Export complete!") # Set status text
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()