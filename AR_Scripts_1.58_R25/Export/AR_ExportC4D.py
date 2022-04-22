"""
AR_ExportC4D

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExportC4D
Version: 1.0.1
Description-US: Exports top level objects individually to C4D file. Supports object selection.

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (17.10.2020) - Updated for R25, added support for selected objects
"""

# Libraries
import c4d
import os

# Functions
def GetFolderSeparator():
    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
        return "\\"
    else: # If operating system is Mac or Linux
        return "/"

def ExportObject(obj, fn):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    tempDoc = c4d.documents.IsolateObjects(doc, [obj]) # Isolate object to temp doc
    name = obj.GetName() # Get object's name
    separator = GetFolderSeparator() # Get folder separator
    path = os.path.splitext(fn)[0]+separator+name+".c4d" # File name
    c4d.documents.SaveDocument(tempDoc, path, c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST, c4d.FORMAT_C4DEXPORT) # Export C4D-file
    tempDoc.Flush() # Flush temp doc

def main():
    fn = c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Folder to export", c4d.FILESELECT_DIRECTORY)
    if not fn: return # If cancelled stop the script
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    objects = doc.GetObjects() # Get objects
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get selected objects

    if len(selected) == 0: # If there's no selected objects
        for i, obj in enumerate(objects): # Iterate through objects
            ExportObject(obj, fn) # Export object
    else: # If there's selected objects
        for obj in selected: # Iterate through selected objects
            ExportObject(obj, fn) # Export object

    c4d.StatusSetText("Export complete!") # Set status text
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()