"""
AR_ExportOBJs

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExportOBJs
Version: 1.0
Description-US: Exports top level objects individually to OBJ file

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d, os
from c4d import plugins

# Functions
def main():
    fn = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Folder to export", c4d.FILESELECT_DIRECTORY)
    if not fn: return # If cancelled stop the script
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    objects = doc.GetObjects() # Get objects

    plug = plugins.FindPlugin(1030178, c4d.PLUGINTYPE_SCENESAVER)
    if plug is None:
        return
    data = {}
    if plug.Message(c4d.MSG_RETRIEVEPRIVATEDATA, data):
        if "imexporter" not in data:
            return
        objExport = data["imexporter"]
        if objExport is None:
            return

    for i, obj in enumerate(objects): # Iterate through objects
        tempDoc = c4d.documents.BaseDocument() # Initiralize a temp document
        clone = obj.GetClone() # Get clone of the original object
        tags = obj.GetTags() # Get object's tags
        for t in tags: # Loop through tags
            if isinstance(t, c4d.TextureTag): # If texture tag
                mat = t[c4d.TEXTURETAG_MATERIAL] # Get material
                tempDoc.InsertMaterial(mat) # Insert material to the temp document
        tempDoc.InsertObject(clone) # Insert clone to the temp document
        name = obj.GetName()
        path = os.path.splitext(fn)[0]+"\\"+name+".obj" # File name
        c4d.documents.SaveDocument(tempDoc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1030178) # Export OBJ-file
        tempDoc.Flush() # Flush temp doc
    c4d.StatusSetText("Export complete!") # Set status text
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()



