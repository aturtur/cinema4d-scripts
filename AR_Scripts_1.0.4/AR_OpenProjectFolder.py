"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenProjectFolder
Version: 1.0
Description-US: Opens folder where project is saved

Written for Maxon Cinema 4D R21.207
Python version 2.7.14
"""
# Libraries
import c4d

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    path = doc.GetDocumentPath() # Get file path of project
    if path is not "": # If path is not empty
        c4d.storage.ShowInFinder(path, False) # Open project folder

# Execute main()
if __name__=='__main__':
    main()

