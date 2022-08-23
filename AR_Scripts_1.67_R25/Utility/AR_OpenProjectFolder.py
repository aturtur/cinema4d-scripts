"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenProjectFolder
Version: 1.0.2
Description-US: Opens the folder wher the project file is saved.

Written for Maxon Cinema 4D R26.013
Python version 3.9.1

Change log:
1.0.2 (18.05.2022) - Bug fix
1.0.1 (26.04.2022) - Update
"""

# Libraries
import c4d
from c4d import storage

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    path = doc.GetDocumentPath() # Get file path of project
    if path != "": # If path is not empty
        storage.ShowInFinder(path, True) # Open project folder

# Execute main()
if __name__=='__main__':
    main()