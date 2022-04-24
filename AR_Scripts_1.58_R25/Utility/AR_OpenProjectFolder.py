"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenProjectFolder
Version: 1.0
Description-US: Opens folder where project is saved

Written for Maxon Cinema 4D R25+
Python version 3.9.1

R26 Update: Toms Seglins (tomsvfx)
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    path = doc.GetDocumentPath() # Get file path of project
    if path != "": # If path is not empty
        c4d.storage.ShowInFinder(path, True) # Open project folder

# Execute main()
if __name__=='__main__':
    main()
