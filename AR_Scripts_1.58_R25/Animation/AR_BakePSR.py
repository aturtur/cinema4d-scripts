"""
AR_BakePSR

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_BakePSR
Version: 1.0.2
Description-US: Bakes object to PSR animation in world space. Shift: In local space

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.2 (10.10.2021) - Updated to R25
1.0.1 (27.10.2020) - Fixed setTime bug
"""

# Libraries
import c4d

# Functions
def GetKeyMod():
    bc = c4d.BaseContainer() # Initialize a base container
    keyMod = "None" # Initialize a keyboard modifier status
    # Button is pressed
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):
        if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL: # Ctrl + Shift
                if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl + Shift
                    keyMod = 'Alt+Ctrl+Shift'
                else: # Shift + Ctrl
                    keyMod = 'Ctrl+Shift'
            elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Shift
                keyMod = 'Alt+Shift'
            else: # Shift
                keyMod = 'Shift'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt + Ctrl
                keyMod = 'Alt+Ctrl'
            else: # Ctrl
                keyMod = 'Ctrl'
        elif bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT: # Alt
            keyMod = 'Alt'
        else: # No keyboard modifiers used
            keyMod = 'None'
        return keyMod

def MoveToLast(obj, doc):
    items = doc.GetObjects() # Get top level items from the document
    last = items[-1] # The Last item in the hierarchy
    obj.InsertAfter(last) # Move object after the last item

def MoveToFirst(obj, doc):
    items = doc.GetObjects() # Get top level items from the document
    first = items[0] # The first item in the hierarchy
    obj.InsertBefore(first) # Move object before the first item

def CopyTags(source, target):
    hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Tag types that you dont wan't to delete
    tags = source.GetTags() # Get objects tags
    for t in reversed(tags): # Iterate through tags
        if type(t) not in hiddenTags:
            d = t.GetClone() # Duplicate the tag
            target.InsertTag(d) # Copy tag

def DisableDynamics(obj):
    tags = obj.GetTags() # Get objects tags
    for t in tags: # Iterate through tags
        if t.GetType() == 180000102: # If dynamics tag
            t[c4d.RIGID_BODY_ENABLED] = False # Disable dynamics

def DummyObject(obj, doc):
    dummyObject = obj.GetClone() # Initialize a camera object
    RemoveTags(dummyObject)
    dummyObject.SetName("Dummy "+obj.GetName()) # Set name
    doc.InsertObject(dummyObject) # Insert dummyObject to document
    MoveToLast(dummyObject, doc) # Move new camera in the object hierarchy
    pythontag = c4d.BaseTag(c4d.Tpython) # Initialize python tag
    dummyObject.InsertTag(pythontag) # Insert python tag to object
    prioritydata = c4d.PriorityData() # Initialize a priority data
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_MODE, c4d.CYCLE_GENERATORS) # Set priority to 'Generators'
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, 449) # Set priority value to last possible value
    prioritydata.SetPriorityValue(c4d.PRIORITYVALUE_CAMERADEPENDENT, False) # Set camera dependent to false
    pythontag[c4d.EXPRESSION_PRIORITY] = prioritydata # Set priority data
    pythontag[c4d.TPYTHON_FRAME] = True # Set frame dependet to true
    link1 = CreateUserDataLink(pythontag, "Object", obj) # Create user data link
    pythontag[c4d.TPYTHON_CODE] = ( "import c4d\n"
                                    "def main():\n"
                                    "\tcam = op[c4d.ID_USERDATA,1]\n"
                                    "\tmat = cam.GetMg()\n"
                                    "\tobj = op.GetObject()\n"
                                    "\tobj.SetMg(mat)")
    return dummyObject

def CleanKeys(obj):
    """ Removes unnecessary keyframes """
    ctracks = obj.GetCTracks() # Get object's CTracks
    for ctrack in ctracks: # Iterate through CTracks
        curve = ctrack.GetCurve() # Get Curve (keyframe holder)
        keyCount = curve.GetKeyCount() # Get Keyframe count
        keysToDelete = [] # Initialize an array for kayframes that can be deleted
        for key in range(0, keyCount): # Iterate through keyframes
            keyValue = curve.GetKey(key).GetValue() # Get keyframe value
            if (key != 0) and (key != keyCount-1): # If not first or last keyframe
                prevKey = curve.GetKey(key-1).GetValue() # Get previous keyframes value
                nextKey = curve.GetKey(key+1).GetValue() # Get next keyframes value
                if keyValue == prevKey and keyValue == nextKey: # If current keyframe has same value with previous and next keyframe
                    keysToDelete.append(key) # Add this keyframe to deleted keys
        for d in reversed(keysToDelete): # Iterate through keystoDelete array
            curve.DelKey(d) # Delete keyframe
    # Remove unused tracks
    ctracks = obj.GetCTracks() # Get object's CTracks again
    for ctrack in ctracks:
        curve = ctrack.GetCurve()
        keyCount = curve.GetKeyCount()
        if keyCount == 2: # If CTrack has only two keyframes
            if curve.GetKey(0).GetValue() == curve.GetKey(1).GetValue(): # ...and if they has same value
                ctrack.Remove() # ...CTrack can be removed

def CreateUserDataLink(obj, name, link, parentGroup=None, shortname=None):
    """ Create user data link """
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

def SetCurrentFrame(frame, doc):
    """ Changes editor's current frame to  """
    doc.SetTime(c4d.BaseTime(frame,doc.GetFps())) # Set current time to given frame
    doc.ExecutePasses(None, True, True, True, 0) # Animate the current frame of the document
    c4d.GeSyncMessage(c4d.EVMSG_TIMECHANGED) # Send a synchronous event message that time has changed
    return

def RemoveTags(obj):
    """ Removes tags of the object  """
    hiddenTags = [c4d.PointTag, c4d.PolygonTag] # Tag types that you dont wan't to delete
    tags = obj.GetTags() # Get tags
    for t in tags: # Iterate through tags
        if type(t) not in hiddenTags: # If not protected tag type
            t.Remove() # Remove tag

def Bake(source, target):
    """ Bake function  """

    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    fps = doc.GetFps() # Get Frame Rate
    startFrame = doc.GetLoopMinTime().GetFrame(fps) # Get first frame of Preview Range
    endFrame = doc.GetLoopMaxTime().GetFrame(fps) # Get last frame of Preview Range

    for i in range(startFrame, endFrame+1): # Iterate through Preview Range
        SetCurrentFrame(i, doc) # Set current frame
        frame = doc.GetTime().GetFrame(fps) # Get current frame

        dataVault = [ [903, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [903, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [903, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Position
                      [904, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [904, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR], # Rotation
                      [905, c4d.DTYPE_REAL, 1000, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1001, c4d.DTYPE_VECTOR], [905, c4d.DTYPE_REAL, 1002, c4d.DTYPE_VECTOR],  # Scale
                    ]

        for data in dataVault: # Iterate through data vault
            if len(data) == 2: # Float
                desc = c4d.DescID(c4d.DescLevel(data[0], data[1],0))
                value = source[data[0]]

            if len(data) == 4: # Vector
                desc = c4d.DescID(c4d.DescLevel(data[0], data[3],0), c4d.DescLevel(data[2], data[1],0))
                value = source[data[0],data[2]]

            track = target.FindCTrack(desc) # Try to find CTrack
            if not track: # If CTrack does not exists
                track = c4d.CTrack(target, desc) # Initialize CTrack
                target.InsertTrackSorted(track) # Insert CTrack to the object

            curve = track.GetCurve() # Get Curve of the CTrack
            currentTime = c4d.BaseTime(frame, fps) # Get current time
            key = curve.AddKey(currentTime)["key"]
            track.FillKey(doc, target, key)

            if data[1] == c4d.DTYPE_REAL: # Float
                key.SetValue(curve, value)
            else: # If boolean or integer
                key.SetValue(curve, value)
                key.SetGeData(curve, value) # Keyframe value needs to be set with SetGeData

def main():
    """ The first function to run """
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selected = doc.GetActiveObjects(0) # Get selected objects
    doc.StartUndo() # Start recording undos
    keyMod = GetKeyMod() # Get keymodifier
    if keyMod == "None":
        bakedObjects = [] # Initialize a list for collecting baked objects
        for s in selected: # Iterate through objects
            dummyObject = DummyObject(s, doc) # Dummy object
            bakeObj = s.GetClone() # Bake object
            name = s.GetName() # Get object's name
            bakeObj.SetName(name+"_baked") # Set baked object's name
            bakeObj.InsertAfter(dummyObject) # Insert object to document
            doc.AddUndo(c4d.UNDOTYPE_NEW, bakeObj) # Add undo command for creating a new object
            doc.ExecutePasses(None, True, True, True, 0) # Animate the current frame of the document
            RemoveTags(bakeObj) # Remove tags of the object
            Bake(dummyObject, bakeObj) # Bake the object
            CleanKeys(bakeObj) # Clean keyframes
            CopyTags(s, bakeObj)
            DisableDynamics(bakeObj)
            dummyObject.Remove() # Delete dummy object
            bakedObjects.append(bakeObj)

        for baked in reversed(bakedObjects):
            MoveToFirst(baked, doc) # Sort

    if keyMod == "Shift":
        for s in selected: # Iterate through objects
            bakeObj = s.GetClone() # Bake object
            name = s.GetName() # Get object's name
            bakeObj.SetName(name+"_baked") # Set baked object's name
            bakeObj.InsertAfter(s) # Insert object to document
            doc.AddUndo(c4d.UNDOTYPE_NEW, bakeObj) # Add undo command for creating a new object
            doc.ExecutePasses(None, True, True, True, 0) # Animate the current frame of the document
            RemoveTags(bakeObj) # Remove tags of the object
            Bake(s, bakeObj) # Bake the object
            CleanKeys(bakeObj) # Clean keyframes
            CopyTags(s, bakeObj)
            DisableDynamics(bakeObj)

    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()