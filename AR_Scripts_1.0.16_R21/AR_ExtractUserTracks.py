"""
AR_ExtractUserTracks

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ExtractUserTracks
Version: 1.0
Description-US: Extracts 2D user tracks from selected motion tracker to null objects

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

"""
# Libraries
import c4d

# Functions
def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None): # Create user data link
    if obj is None: return False # If there is no object stop the function
    if shortname is None: shortname = name # Short name is name
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_BASELISTLINK) # Initialize user data
    bc[c4d.DESC_NAME] = name # Set user data name
    bc[c4d.DESC_SHORT_NAME] = shortname # Set userdata short name
    bc[c4d.DESC_DEFAULT] = link # Set default value
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_OFF # Disable animation option
    bc[c4d.DESC_SHADERLINKFLAG] = True
    if parentGroup is not None: # If there is parent group
        bc[c4d.DESC_PARENTGROUP] = parentGroup # Set parent group
    element = obj.AddUserData(bc) # Add user data
    obj[element] = link # Set user data value
    return element # Return user data field

def CreateUserDataFloat(obj, name, val=0, parentGroup=None, unit=c4d.DESC_UNIT_REAL):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_REAL)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_STEP] = 2
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def CreateUserDataInt(obj, name, val=0, parentGroup=None, unit=c4d.DESC_UNIT_INT):
    if obj is None: return False
    bc = c4d.GetCustomDatatypeDefault(c4d.DTYPE_LONG)
    bc[c4d.DESC_NAME] = name
    bc[c4d.DESC_SHORT_NAME] = name
    bc[c4d.DESC_DEFAULT] = val
    bc[c4d.DESC_ANIMATE] = c4d.DESC_ANIMATE_ON
    bc[c4d.DESC_UNIT] = unit
    bc[c4d.DESC_STEP] = 1
    if parentGroup is not None:
        bc[c4d.DESC_PARENTGROUP] = parentGroup
  
    element = obj.AddUserData(bc)
    obj[element] = val
    return element

def GetUserTracks(tracks, tracksType):
    """ Function to get a list of User Tracks """
    userTracks = []
    for index in range(len(tracksType)):
        if tracksType[index] == 1:
            userTracks.append(tracks.GetTrackByIndex(index = index))
    return userTracks

def Create2DTracks(mt):
    """ Function to create 2D track nulls from Motion Tracker object """
    tracks = mt.Get2dTrackData() # Get 2D trackers
    count = tracks.GetTrackCount() # Count of trackers
    tracksStatus = tracks.GetTrackIndices(userTracks = True, autoTracks = False)
    tracksType = tracksStatus.GetAll(count)
    userTracks = GetUserTracks(tracks, tracksType) # Get user trackers
    utCount = len(userTracks) # Count of user trackers

    code = "import c4d\n\
def GetUserTracks(tracks, tracksType):\n\
    userTracks = []\n\
    for index in range(len(tracksType)):\n\
        if tracksType[index] == 1:\n\
            userTracks.append(tracks.GetTrackByIndex(index = index))\n\
    return userTracks\n\
def GetClosestActive(index, booleanList):\n\
    minusIndex = index\n\
    plusIndex = index\n\
    while booleanList[minusIndex] == False and minusFrame > firstFrame:\n\
        minusFrame -= 1\n\
    while booleanList[plusFrame] == False and plusFrame < lastFrame:\n\
        plusFrame += 1\n\
    if booleanList[plusFrame] == True and booleanList[minusIndex] == True:\n\
       if (plusFrame - frame) < (frame - minusIndex):\n\
           frame = plusFrame\n\
       else:\n\
            frame = minusIndex\n\
    elif booleanList[minusIndex] == True:\n\
        frame = minusIndex\n\
    elif booleanList[plusFrame] == True:\n\
        frame = plusFrame\n\
def main():\n\
    Count = 0\n\
    CameraSpacePosition = c4d.Vector(0.0, 0.0, 0.0)\n\
    isActive = False\n\
    mt = op[c4d.ID_USERDATA,1]\n\
    index = op[c4d.ID_USERDATA,2]\n\
    cameraDistance = op[c4d.ID_USERDATA,3]\n\
    obj = op.GetObject()\n\
    time = doc.GetTime()\n\
    fps = doc.GetFps()\n\
    frame = time.GetFrame(fps)\n\
    ft = mt.GetFootageData()\n\
    if ft != None:\n\
        firstFrame = ft.GetFirstFrameNumber()\n\
        lastFrame = ft.GetLastFrameNumber()\n\
    else:\n\
        firstFrame = doc.GetMinTime().GetFrame(fps)\n\
        lastFrame = doc.GetMaxTime().GetFrame(fps)\n\
    cam = mt.GetDown()\n\
    fl = cam[c4d.CAMERA_FOCUS]\n\
    sw = cam[c4d.CAMERAOBJECT_APERTURE]\n\
    camMatrix = cam.GetMg()\n\
    tracks = mt.Get2dTrackData()\n\
    count = tracks.GetTrackCount()\n\
    ft = mt.GetFootageData()\n\
    tracksStatus = tracks.GetTrackIndices(userTracks = True, autoTracks = False)\n\
    tracksType = tracksStatus.GetAll(count)\n\
    userTracks = GetUserTracks(tracks, tracksType)\n\
    utCount = len(userTracks)\n\
    track = userTracks[index]\n\
    activeFrames = track.GetFramesWithTrackData().GetAll(lastFrame + 1)\n\
    if activeFrames[frame] == True:\n\
        isActive = True\n\
    else:\n\
        minusFrame = frame\n\
        plusFrame = frame\n\
        while activeFrames[minusFrame] == False and minusFrame > firstFrame:\n\
            minusFrame -= 1\n\
        while activeFrames[plusFrame] == False and plusFrame < lastFrame:\n\
            plusFrame += 1\n\
        if activeFrames[plusFrame] == True and activeFrames[minusFrame] == True:\n\
           if (plusFrame - frame) < (frame - minusFrame):\n\
               frame = plusFrame\n\
           else:\n\
                frame = minusFrame\n\
        elif activeFrames[minusFrame] == True:\n\
            frame = minusFrame\n\
        elif activeFrames[plusFrame] == True:\n\
            frame = plusFrame\n\
    projection = track.GetDataForFrame(frameNum = frame)\n\
    if projection is not None:\n\
        camPos = projection.GetCameraSpaceDirection(focalLength = fl, sensorWidth = sw)\n\
        camPos = camPos * cameraDistance\n\
        globalPos = camMatrix.Mul(camPos)\n\
    if projection is not None:\n\
        obj.SetAbsPos(globalPos)\n\
    else:\n\
        obj.SetAbsPos(c4d.Vector(0.0, 0.0, 0.0))"

    groupNull = c4d.BaseObject(c4d.Onull) # Initialize a null object
    groupNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set group null's display to none
    groupNull.SetName("User 2D Tracks") # Set group null's name
    groupNull.InsertAfter(mt) # Put group null after Motion Tracker object
    doc.AddUndo(c4d.UNDO_NEW, groupNull) # Record undo for adding new object

    for i, ut in enumerate(reversed(userTracks)): # Iterate through user trackers
        null = c4d.BaseObject(c4d.Onull) # Initialize a null object
        null.SetName(ut.GetName()) # Set null's name
        null[c4d.NULLOBJECT_DISPLAY] = 2 # Set null's display to circle
        null[c4d.NULLOBJECT_RADIUS] = 5 # Set null's radius to 5
        pyTag = c4d.BaseTag(1022749) # Initialize a python tag
        pyTag[c4d.TPYTHON_CODE] = code # Set python tag's python script
        null.InsertTag(pyTag) # Put tag to the null
        CreateUserDataLink(pyTag, "Motion Tracker", mt) # Create a motion tracker user data
        CreateUserDataInt(pyTag, "Index", len(userTracks)-1-i) # Create user data for trakcer index
        CreateUserDataFloat(pyTag, "Camera Distance", 100) # Create user data for camera distance        
        doc.InsertObject(null) # Insert null object to the document
        null.InsertUnder(groupNull) # Put null under the group null

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(0) # Get selected objects
    for s in selection: # Iterate through selection
        if s.GetType() == 1028393: # If Motion Tracker object
            Create2DTracks(s) # Create user 2D tracks
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D  
  
# Execute main()
if __name__=='__main__':
    main()