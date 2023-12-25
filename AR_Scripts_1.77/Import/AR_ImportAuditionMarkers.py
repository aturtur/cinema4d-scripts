"""
AR_ImportAuditionMarkers

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportAuditionMarkers
Version: 1.0.0
Description-US: Imports Adobe Audition markers CSV file and creates markers from those

Written for Maxon Cinema 4D 2023.2.2
Python version 3.10.8

Change log:
1.0.0 (31.08.2023) - Initial realease
"""

# Libraries
import c4d
import random
from c4d import storage as s

# Functions
def RandomColor():
    red   = random.random()
    green = random.random()
    blue  = random.random()
    
    return c4d.Vector(red, green, blue)

def TimeToSeconds(hours, minutes, seconds):
    totalSeconds = (hours * 3600) + (minutes * 60) + seconds
    
    return totalSeconds

def TimeToBaseTime(time):
    # 1:09:59.842
    split = time.split(":") # Split time

    hours   = 0
    minutes = 0
    seconds = 0

    if len(split) == 3:
        hours   = float(split[0]) # Hours
        minutes = float(split[1]) # Minutes
        seconds = float(split[2]) # Seconds

    elif len(split) == 2: # Minutes, seconds
        minutes = float(split[0]) # Minutes
        seconds = float(split[1]) # Seconds

    fps = doc.GetFps()
    totalSeconds = TimeToSeconds(hours, minutes, seconds) * fps

    return c4d.BaseTime(totalSeconds, fps)

def main():

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select Audition CSV file',c4d.FILESELECT_LOAD,'') # File dialog
    if fn is None: return # If no file, exit
    f = open(fn) # Open file
    for i, line in enumerate(f): # Loop trhough lines in Pixeur color palette file
        if i != 0: # Skip first line
            line     = line.split("\t") # Split line to list
            name     = line[0] # Marker name
            start    = line[1] # Start time
            duration = line[2] # Duration

            time   = TimeToBaseTime(start) # Get time in correct format
            length = TimeToBaseTime(duration) # Get length in correct format

            marker = c4d.documents.AddMarker(doc, None, time, name) # Add marker
            marker[c4d.TLMARKER_LENGTH] = length # Set length
            marker[c4d.TLMARKER_COLOR] = RandomColor() # Set color

            doc.AddUndo(c4d.UNDOTYPE_NEW, marker) # Add undo command for inserting a marker
            
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main
if __name__ == '__main__':
    main()