"""
AR_MarkersToRange

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_MarkersToRange
Version: 1.1.0
Description-US: Set render range from markers

Written for Maxon Cinema 4D 2024.4.1
Python version 3.11.4

Change log:
1.1.0 (22.07.2024) - Default values, 'Close' button added, fixes 
1.0.1 (21.07.2024) - Bug fixes
1.0.0 (27.06.2024) - Initial release
"""

# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog

# Global variables
GRP_MAIN      = 1000
GRP_SECOND    = 1001
GRP_MARKERS   = 1002
GRP_RENDERSET = 1003
GRP_BUTTONS   = 1004

BTN_SET       = 2000
BTN_CLOSE     = 2001

RAD_MARKERS   = 3000
RAD_RENDERSET = 4000

# Functions
def GetNext(op):
    if op == None: return None
    if op.GetDown(): return op.GetDown()
    while not op.GetNext() and op.GetUp(): op = op.GetUp()
    return op.GetNext()

def CollectMarkers():
    markers = []
    firstMarker = c4d.documents.GetFirstMarker(doc) # Get first created marker
    currentMarker = firstMarker
    while currentMarker:
        markers.append(markerObject(currentMarker, # Add marker object to the markers list
                                    currentMarker.GetName(),
                                    currentMarker[c4d.TLMARKER_TIME],
                                    currentMarker[c4d.TLMARKER_LENGTH],
                                    currentMarker[c4d.TLMARKER_TIME].Get()))
        currentMarker = currentMarker.GetNext() # Move to the next marker
    return markers # Return markers list

def CollectRenderData():
    renderDatas = []
    firstRenderData = doc.GetFirstRenderData() # Get the first render data
    activeRenderData = doc.GetActiveRenderData() # Get the active render data
    currentRenderData = firstRenderData
    count = 0
    while currentRenderData:
        if currentRenderData == activeRenderData:
            activeSlot = count
        renderDatas.append(renderSettingsObject(currentRenderData, # Add render data object to the render datas list
                                                currentRenderData.GetName()))
        currentRenderData = GetNext(currentRenderData)
        count += 1

    return activeSlot, renderDatas

def SetRange(marker, renderData):
    doc.StartUndo() # Start recording undos
    #frame = c4d.BaseTime(1.0 / doc.GetFps())
    startTime = marker.time
    endTime   = marker.time + marker.length
    if endTime.Get() < startTime.Get():
        endTime = startTime

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData.rd) # Add undo step for render data changes
    renderData.rd[c4d.RDATA_FRAMESEQUENCE] = 0 # Manual
    renderData.rd[c4d.RDATA_FRAMEFROM]     =  startTime # Start time
    renderData.rd[c4d.RDATA_FRAMETO]       =  endTime # End frame

    doc.EndUndo() # Start recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Classes
class renderSettingsObject(object):
    def __init__(self, renderRata, name):
        self.rd   = renderRata # Render data
        self.name = name       # Name

class markerObject(object):
    def __init__(self, marker, name, time, length, sec):
        self.marker = marker # Marker
        self.name   = name   # Name
        self.time   = time   # Time
        self.sec    = sec    # Time in seconds
        self.length = length # Length

class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        global sortedMarkers
        global renderSettings

        markers = CollectMarkers() # Get markers

        sortedMarkers = sorted(markers, key=lambda x: x.sec, reverse=False) # Sort markers by time
        activeSlot, renderSettings = CollectRenderData() # Get render settings

        self.SetTitle("Markers to Ranges") # Set dialog title

        self.GroupBegin(GRP_MAIN, c4d.BFH_CENTER, 1, 1) # Start Group 1
        self.GroupBorderSpace(9, 0, 9, 9)

        self.GroupBegin(GRP_SECOND, c4d.BFH_FIT, 2, 1) # Start Group 2
        self.GroupBorderSpace(9, 0, 9, 9)

        # Markers
        self.GroupBegin(GRP_MARKERS, c4d.BFH_LEFT | c4d.BFV_TOP, 1, 1, "Markers", 150, 150) # Start Group 3
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(4, 4, 4, 4)
        self.AddRadioGroup(RAD_MARKERS, c4d.BFH_LEFT, 1, len(markers))
        for i, marker in enumerate(sortedMarkers):
            #startFrame = marker.time.GetFrame(doc.GetFps())
            startFrame = round(marker.time.Get()*doc.GetFps(), 2)
            if startFrame.is_integer():
                startFrame = int(startFrame)

            #endFrame = (marker.time.GetFrame(doc.GetFps())) + (marker.length.GetFrame(doc.GetFps()))
            endFrame = round(startFrame + (marker.length.Get()*doc.GetFps()), 2)
            if endFrame.is_integer():
                endFrame = int(endFrame)

            if endFrame < startFrame:
                endFrame = startFrame

            name = marker.name+" | "+str(startFrame)+" - "+str(endFrame)
            self.AddChild(RAD_MARKERS, i, name)
        self.GroupEnd() # End Group 3
        self.SetInt32(RAD_MARKERS, 0) # Set default markers value

        # Render settings
        self.GroupBegin(GRP_RENDERSET, c4d.BFH_RIGHT | c4d.BFV_TOP, 1, 1, "Render Settings", 150, 150) # Start Group 4
        self.GroupBorder(c4d.BORDER_GROUP_IN)
        self.GroupBorderSpace(4, 4, 4, 4)
        self.AddRadioGroup(RAD_RENDERSET, c4d.BFH_LEFT, 1, len(renderSettings))
        for i, renderSetting in enumerate(renderSettings):
            name = renderSetting.name
            self.AddChild(RAD_RENDERSET, i, name)
        self.GroupEnd() # End Group 4
        self.SetInt32(RAD_RENDERSET, activeSlot) # Set default render settings value
        self.GroupEnd() # End Group 2

        # Button
        self.GroupBegin(GRP_BUTTONS, c4d.BFH_CENTER, 2, 1) # Start Group 4
        self.AddButton(BTN_SET, c4d.BFH_LEFT, name="Set Range") # Add button 'Set Range'
        self.AddButton(BTN_CLOSE, c4d.BFH_RIGHT, name="Close") # Add button 'Close'
        self.GroupEnd() # End Group 1

        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        global sortedMarkers
        global renderSettings

        # Actions here
        if paramid == BTN_SET: # If 'Set Range' button is pressed

            selectedMarker = self.GetInt32(RAD_MARKERS)
            selectedRenderSettings = self.GetInt32(RAD_RENDERSET)

            theMarker = sortedMarkers[selectedMarker]
            theRenderSetting = renderSettings[selectedRenderSettings]

            SetRange(theMarker, theRenderSetting)

            c4d.EventAdd() # Refresh Cinema 4D

        if paramid == BTN_CLOSE: # If 'Close' button is pressed
            self.Close() # Close dialog

        return True # Everything is fine

checkMarker = c4d.documents.GetFirstMarker(doc)
if checkMarker == None: # If no markers
    c4d.gui.MessageDialog("No markers!")
else:
    dlg = Dialog() # Create dialog object
    dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 150, 150) # Open dialog