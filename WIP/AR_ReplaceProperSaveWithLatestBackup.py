"""
AR_ReplaceProperSaveWithLatestBackup

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ReplaceProperSaveWithLatestBackup
Description-US: Replaces the last proper save with the last found backup file. Backup files should be located in the backup folder, which is located under the folder of the c4d project file.
Version: 1.0

WARNING! This copies files over other files. Be cautious!
"""

# Libraries
import c4d
import glob
import os
import datetime
import shutil
from c4d import gui

# Functions
def GetModDate(filename):
    t = os.path.getmtime(filename) # Get the file's modified date data
    return datetime.datetime.fromtimestamp(t) # Modify and return the date

def main():
    recentDocs = c4d.documents.GetRecentDocumentsList() # Get list of the recent documents
    latestDoc = recentDocs[0]                           # Get the latest c4d document
    latestDoc = str(latestDoc).replace('file:///','')  # Get document's path
    latestDocName = latestDoc[latestDoc.rfind('/'):][1:] # Get document's name
    latestDoc = latestDoc.replace('/', '\\')           # Modify file path separators
    latestDocDir = os.path.dirname(latestDoc)          # Get the document's director path
    backupPath = os.path.join(latestDocDir, "backup")  # Get ppath of backup files
    backupPath = backupPath+"\*"                       # Modifying the folder path for the glob operation
    backupFiles = glob.glob(backupPath)                # * means all if need specific format then *.csv
    if len(backupFiles) == 0:                          # If no backup files found
        print ("No backup files found")                # Print some stuff
        return False                                    # Return false
    else:                                               # Otherwise
        latestBackup = max(backupFiles, key=os.path.getctime) # Get the latest backup file
        lastDot = latestBackup.rfind('.')                     # Get the file extension
        extension = latestBackup[lastDot:][:5]                # Format the extension
        if extension == ".c4d@":                              # Check the extension
            properFileDate = GetModDate(latestDoc)            # Get modify date of the proper file
            backupFileDate = GetModDate(latestBackup)         # Get modify date of the backup file
            backupFileName = latestBackup[latestBackup.rfind("\\"):][1:] # Get backup file's name
            if properFileDate < backupFileDate:         # If backup file is newer than the proper save 
                qbox = gui.QuestionDialog("Backup file found:\n"+backupFileName+"\nReplace the proper save ("+latestDocName+") with the backup file?")
                if qbox == True:
                    shutil.copyfile(r''+latestBackup+'', r''+latestDoc+'') # Replace the latest document with the latest backup
                    c4d.documents.LoadFile(latestDoc) # Open the file
            else:
                qbox = gui.QuestionDialog("Latest found backup file:\n"+backupFileName+"\nis older than the proper save.\nOverwrite "+latestDocName+" anyway?")
                if qbox == True:
                    shutil.copyfile(r''+latestBackup+'', r''+latestDoc+'') # Replace the latest document with the latest backup
                    c4d.documents.LoadFile(latestDoc) # Open the file
        else:                                                 # Otherwise
            print ("Incorrect file selected for the backup") # Print some stuff
    
    
    c4d.EventAdd()                                      # Update the Cinema 4D

# Execute main()
if __name__=='__main__':
    main()