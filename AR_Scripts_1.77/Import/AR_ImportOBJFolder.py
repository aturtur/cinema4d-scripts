"""
AR_ImportOBJFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportOBJFolder
Version: 1.0.1
Description-US: Merges OBJ-files from selected folder to the document

Written for Maxon Cinema 4D R25.010
Python version 3.9.1

Change log:
1.0.1 (28.04.2022) - Updated for R25
"""

# Libraries
import c4d, os
from c4d import storage as s

# Functions
def GetFolderSeparator():
    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
        return "\\"
    else: # If operating system is Mac or Linux
        return "/"

def main():
    extensions = ["obj"] # File extensions that will be imported
    separator = GetFolderSeparator() # Get path separator
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select folder to import',c4d.FILESELECT_DIRECTORY,'') # Load folder
    if not folder: return # If there is no folder, stop the script
    files = os.listdir(folder) # Get files
    for f in files: # Loop through files
        ext = f.rsplit(".",1) # Get file extension
        if ext[1] in extensions: # If extension matches
            c4d.documents.MergeDocument(doc, folder+separator+f, c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS) # Merge file to current project
    c4d.EventAdd() # Update Cinema 4D
if __name__=='__main__':
    main()