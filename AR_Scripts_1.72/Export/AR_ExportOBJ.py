"""
AR_ExportOBJ

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExportOBJ
Version: 1.2.0
Description-US: Exports top level objects individually to OBJ file. Supports object selection

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.2.0 (17.11.2022) - Progress bar
1.1.0 (17.10.2020) - Updated for R25, added support for selected objects
"""

# Libraries
import c4d
import os
from c4d import plugins
from c4d import utils as u

# Functions
def ExportObject(obj, fn):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    tempDoc = c4d.documents.IsolateObjects(doc, [obj]) # Isolate object to temp doc
    name = obj.GetName() # Get object's name
    separator = os.sep # Get folder separator
    path = os.path.splitext(fn)[0]+separator+name+".obj" # File name
    c4d.documents.SaveDocument(tempDoc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, 1030178) # Export OBJ-file
    tempDoc.Flush() # Flush temp doc

def main():
    fn = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Folder to export", c4d.FILESELECT_DIRECTORY)
    if not fn: return # If cancelled stop the script
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    objects = doc.GetObjects() # Get objects
    selected = doc.GetActiveObjects(0) # Get selected objects

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

    if len(selected) == 0: # If there's no selected objects
        for i, obj in enumerate(objects): # Iterate through objects
            progress = u.RangeMap(i, 0, len(objects), 0, 100, True)
            c4d.StatusSetText("Exporting %s of %s" % (i,len(objects)))
            c4d.StatusSetBar(progress)
            c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_STATICBREAK)
            ExportObject(obj, fn) # Export object
            c4d.GeSyncMessage(c4d.EVMSG_UPDATEBASEDRAW)
    else: # If there's selected objects
        for i, obj in enumerate(selected): # Iterate through selected objects
            progress = u.RangeMap(i, 0, len(selected), 0, 100, True)
            c4d.StatusSetText("Exporting %s of %s" % (i,len(selected)))
            c4d.StatusSetBar(progress)
            c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_STATICBREAK)
            ExportObject(obj, fn) # Export object
            c4d.GeSyncMessage(c4d.EVMSG_UPDATEBASEDRAW)
    c4d.StatusClear() # Clear status
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()