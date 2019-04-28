# Libraries
import c4d, os
from c4d import plugins

# Functions
def main():
    # ---------------------------------------------------------------------------------------------------
    # Step 1 - Setup and export AI-sequence with Sketch and Toon
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    fn = c4d.storage.SaveDialog(c4d.FILESELECTTYPE_ANYTHING, "Select Save Path") # Select path to save
    if not fn: return # If cancelled stop the script
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
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0) # Get selected objects
    for i in xrange(0, len(selection)): # Loop through selected objects
        sketchTags.append(c4d.BaseTag(1011012)) # Insert 'Sketch Style' tag to sketchTags list
        sketchTags[i][c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V] = sketchMat # Put sketch material to sketch tag
        sketchTags[i][c4d.OUTLINEMAT_LINE_SPLINES] = 1 # Enable splines
        sketchTags[i][c4d.OUTLINEMAT_LINE_FOLD] = 0 # Disable fold
        sketchTags[i][c4d.OUTLINEMAT_LINE_CREASE] = 0 # Disable crease
        sketchTags[i][c4d.OUTLINEMAT_LINE_BORDER] = 0 # Disable border
        selection[i].InsertTag(sketchTags[i]) # Insert sketch tag to selected object
    # ---------------------------------------------------------------------------------------------------
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
        name = os.path.splitext(fn)[0]+".ai" # File name
    c4d.documents.SaveDocument(doc, name, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1012074) # Export AI-file
    # ---------------------------------------------------------------------------------------------------
    # Step 2 - Remove unnecessary stuff
    for st in sketchTags: # Loop through sketchTags
        st.Remove() # Remove 'Sketch Style' tag
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