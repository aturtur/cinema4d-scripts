"""
AR_AddSoundFile

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_AddSoundFile
Version: 1.0
Description-US: Adds sound file starting at the current time

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

"""
# Libraries
import os
import c4d
from c4d import storage as s

def main():
    
    path = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Sound file", c4d.FILESELECT_LOAD)
    folderPath, fileName = os.path.split(path)

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document    
    time = c4d.BaseTime(doc.GetTime().Get()) # Get current time
    
    null = c4d.BaseObject(c4d.Onull) # Initialize a null
    null.SetName("Sound: "+fileName) # Set name
    null[c4d.NULLOBJECT_DISPLAY] = 14 # Set 'Display' to 'None'
    null[c4d.ID_BASELIST_ICON_FILE] = "440000255" # Set icon
    null[c4d.ID_BASELIST_ICON_COLORIZE_MODE] = 2 # Set 'Icon Color' to 'Display Color'
    null[c4d.ID_BASEOBJECT_USECOLOR] = 2 # Set 'Display Color' to 'On'
    null[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(140.0/255.0, 203.0/255.0, 1.0)
    null[c4d.ID_BASELIST_ICON_COLOR] = c4d.Vector(140.0/255.0, 203.0/255.0, 1.0)
    doc.InsertObject(null) # Insert null to the document   

    desc = c4d.DescID(c4d.DescLevel(c4d.CTsound, c4d.CTsound, 0))
    SoundTrack = c4d.CTrack(null, desc) # Initialize a sound Track
    null.InsertTrackSorted(SoundTrack) # Insert the sound track to the object
    SoundTrack[c4d.CID_SOUND_NAME] = path # Set sou
    SoundTrack[c4d.CID_SOUND_START] = time

    c4d.EventAdd()

# Execute main()
if __name__=='__main__':
    main()