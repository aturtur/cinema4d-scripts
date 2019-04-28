"""
AR_OpenProjectFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenProjectFolder
Description-US: Opens folder where project is saved
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d
import subprocess

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active document
    path = doc.GetDocumentPath() # Get file path of project
    if path is not "": # If path is not empty
        subprocess.Popen(r'explorer "'+path+'"') # Open project folder

# Execute main()
if __name__=='__main__':
    main()