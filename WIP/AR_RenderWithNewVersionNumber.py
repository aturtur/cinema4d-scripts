"""
AR_RenderWithNewVersionNumber

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_RenderWithNewVersionNumber
Description-US: Updates render paths with a new version number.
Version: 1.0
"""

# Global variables
delimiter = "_v" # String that indicates version delimiter
render    = True # Render to Picture Viewer. Set to False if you just want to increase version number by one.

# Libraries
import c4d
import re
try:
    import redshift
    rs = True
except:
    rs = False
    pass

def GetVersion(filePath):
    """ Get version number from a file path"""
    versionList = re.findall(delimiter+"\d+",filePath) # Search delimiter+digits (e.g. _v001) string in file path and store those in a [list]
    if len(versionList) == 0: # If no versions found
        return False, False
    rawVersion = re.compile(delimiter).split(versionList[len(versionList)-1])[1] # Version number with zero padding [string]
    version = int(rawVersion) # Version number without zero padding [integer]
    return version, rawVersion # (e.g. 1, 001)

def FileName(filePath):
    """ Get a file name from a file path """
    splitted = filePath.rsplit(GetSep()) # Split file path
    fullFileName = splitted[len(splitted)-1] # Full file name with extension [string]
    firstPart = re.compile(delimiter+"\d+").split(fullFileName)[0] # File name first part before delimiter+digits [string]
    fileName = firstPart+delimiter+GetVersion(filePath)[1] # Base file name without extras [string]
    lastPart = re.compile(delimiter+"\d+").split(fullFileName)[1] # File name last part after delimiter+digits [string]
    return fullFileName, firstPart, lastPart, fileName # [string]

def GetNewPath(filePath, version):
    """ Get updated file path with given version number """
    oldVersion = GetVersion(filePath)[1] # Old version
    zeroPadding = len(oldVersion) # Zero padding
    newVersion = delimiter+str(version).zfill(zeroPadding) # New version with zero padding
    newPath = re.sub(r""+delimiter+oldVersion, newVersion, filePath) # New full file path
    return newPath # [string]

def main():
    """ Main function """
    up = 1 # Version step up integer
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    renderData = doc.GetActiveRenderData() # Get document render data
    doc.StartUndo() # Start recording undos    
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData)
    
    # Update render paths
    renderPath = renderData[c4d.RDATA_PATH]
    rVer, rVerStr = GetVersion(renderPath)
    if rVer != False:
        renderPath = GetNewPath(renderPath, rVer+up)
        doc.GetActiveRenderData()[c4d.RDATA_PATH] = renderPath
    
    multipassPath = renderData[c4d.RDATA_MULTIPASS_FILENAME]
    mpVer, mpVerStr = GetVersion(multipassPath)
    if mpVer != False:
        multipassPath = GetNewPath(multipassPath, mpVer+up)
        doc.GetActiveRenderData()[c4d.RDATA_MULTIPASS_FILENAME] = multipassPath
    
    if rs == True:
        vprs = redshift.FindAddVideoPost(renderData, redshift.VPrsrenderer)
        if vprs is None:
            return
        redshiftAovPath = vprs[c4d.REDSHIFT_RENDERER_AOV_PATH]
        rsAovVer, rsAovVerStr = GetVersion(redshiftAovPath)
        if rsAovVer != False:
            redshiftAovPath = GetNewPath(redshiftAovPath, rsAovVer+up)
            vprs[c4d.REDSHIFT_RENDERER_AOV_PATH] = redshiftAovPath
    
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Update Cinema 4D
    
    if render == True:
        c4d.CallCommand(12099) # Render to Picture Viewer

# Execute main()
if __name__=='__main__':
    main()