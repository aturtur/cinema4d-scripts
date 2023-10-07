"""
AR_ImportGaea

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ImportGaea
Version: 1.0.0
Description-US: Creates terrain setup from Gaea heightfield map. Requires Redshift!

Note: It is recommended that you export with following settings
    Format: EXR
    ColorSpace: sRGB
    Range: Raw

    By default uses default terrain definitionn:
        Height: 2,6 km
        Scale: 5 km

Written for Maxon Cinema 4D 2023.2.1
Python version 3.10.8

Change log:
1.0.0 (10.01.2023) - Initial realease
"""

# Libraries
import c4d
import redshift
from c4d import storage as s
from c4d import gui as g

# Functions
def CreateGaeaTerrainSetup(fn):

    size       = 5000 # Gaea's standard width is 5 km
    height     = 2600 # Gaea's standard height is 2.6 km
    resolution = 512 # Segment count
    # -------------------------------------------------------------------------------
    terrainNull   = c4d.BaseObject(c4d.Onull) # Initialize null object 
    terrainEditor = c4d.BaseObject(c4d.Oplane) # Initialize object for editor use
    terrainRender = c4d.BaseObject(c4d.Oplane) # Initialize object for render use

    # Null Settings
    terrainNull.SetName("Terrain") # Set terrain null's name
    terrainNull[c4d.ID_BASELIST_ICON_FILE] = "5169" # Set landscape icon to null object
    terrainNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set null's shape to none

    protectionTagA = c4d.BaseTag(5629) # Initialize protection tag
    protectionTagB = c4d.BaseTag(5629) # Initialize protection tag
    terrainEditor.InsertTag(protectionTagA) # Insert protection tag to terrain object
    terrainRender.InsertTag(protectionTagB) # Insert protection tag to terrain object
    # -------------------------------------------------------------------------------
    # Editor Terrain Setup
    terrainEditor.SetName("Terrain Editor")
    terrainEditor[c4d.PRIM_PLANE_WIDTH] = size
    terrainEditor[c4d.PRIM_PLANE_HEIGHT] = size
    terrainEditor[c4d.PRIM_PLANE_SUBW] = resolution
    terrainEditor[c4d.PRIM_PLANE_SUBH] = resolution
    terrainEditor[c4d.PRIM_AXIS] = 2 # 0;+X, 1;-X, 2;+Y, 3;-Y, 4;+Z, 5;-Z
    terrainEditor[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 2 # 2;Default, 0;On, 1;Off
    terrainEditor[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 1

    # Bitmap shader
    shader = c4d.BaseShader(c4d.Xbitmap) # Initialize bitmap shader
    shader[c4d.BITMAPSHADER_FILENAME] = fn # Set bitmap file
    shader[c4d.BITMAPSHADER_COLORPROFILE] = 2 # Set shader's color profile to 'sRGB'
    #shader[c4d.BITMAPSHADER_COLORPROFILE] = 1 # Set shader's color profile to 'Linear'

    # Displacer
    displacer = c4d.BaseObject(c4d.Odisplacer) # Initialize displacer deformer
    displacer[c4d.MGDISPLACER_DISPLACEMENT_HEIGHT] = height # Set displaced height
    displacer[c4d.MGDISPLACER_DISPLACEMENTMODE] = 0 # # Set displacement type to 'Intensity'
    displacer[c4d.ID_MG_SHADER_SHADER] = shader # Set displacer shader
    displacer[c4d.ID_MG_SHADER_TEXTAG_TILE] = False # Disable tiling to prevent jaggy edges
    displacer.InsertUnder(terrainEditor) # Insert displacer deformer under terrain editor object
    displacer.InsertShader(shader) # Insert shader to displacer
    #displacer.Message(c4d.MSG_UPDATE) # Update
    # -------------------------------------------------------------------------------
    # Render Terrain Setup
    terrainRender.SetName("Terrain Render")
    terrainRender[c4d.PRIM_PLANE_WIDTH] = size
    terrainRender[c4d.PRIM_PLANE_HEIGHT] = size
    terrainRender[c4d.PRIM_PLANE_SUBW] = resolution
    terrainRender[c4d.PRIM_PLANE_SUBH] = resolution
    terrainRender[c4d.PRIM_AXIS] = 2 # 0;+X, 1;-X, 2;+Y, 3;-Y, 4;+Z, 5;-Z
    terrainRender[c4d.ID_BASEOBJECT_VISIBILITY_EDITOR] = 1 # 2;Default, 0;On, 1;Off
    terrainRender[c4d.ID_BASEOBJECT_VISIBILITY_RENDER] = 2

    # RS Object Tag
    rsObjectTag = c4d.BaseTag(1036222) # Initialize RS Object Tag
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_OVERRIDE] = True

    # RS Object Tag Tessalation Options
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_SUBDIVISIONENABLED] = True
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_SCREENSPACEADAPTIVE] = False
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_MINTESSELLATIONLENGTH] = 0
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_MAXTESSELLATIONSUBDIVS] = 2

    # RS Object Tag Displacement Options
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTENABLED] = True
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_MAXDISPLACEMENT] = height
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_DISPLACEMENTSCALE] = height
    rsObjectTag[c4d.REDSHIFT_OBJECT_GEOMETRY_AUTOBUMPENABLED] = True

    terrainRender.InsertTag(rsObjectTag) # Insert RS Object tag to terrain object
    # -------------------------------------------------------------------------------
    # Redshift Material Setup
    material = c4d.BaseMaterial(1036224) # Initialize legacy Redshift material
    material.SetName("Terrain") # Set material name
    doc.InsertMaterial(material, checknames=True) # Add material to the document
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, material) # Record undo for creating the material

    # Redshift Material Node Setup
    rsnm = redshift.GetRSMaterialNodeMaster(material) # Get Redshift material node master
    root = rsnm.GetRoot() # Get node master root
    outputNode = root.GetChildren()[0] # Get output node
    displacementPort = outputNode.AddPort(c4d.GV_PORT_INPUT, 10001) # Add displacement input port
    inputPort = outputNode.GetInPorts()[0] # Get input port
    
    # RS Standard Material Node
    materialNode = rsnm.CreateNode(root, 1036227, None, x = 75, y = 300) # Create Standard Material node
    materialNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "StandardMaterial" # Set node type
    materialNode[c4d.ID_GVBASE_COLOR] = c4d.Vector(0.529, 0.345, 0.333) # Set node color
    materialNode.GetOutPort(0).Connect(inputPort) # Connect ports

    # RS Texture Node
    textureNode = rsnm.CreateNode(root, 1036227, None, x = 0, y = 400) # Create Texture node
    textureNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "TextureSampler" # Set node type
    textureNode[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0,c4d.REDSHIFT_FILE_PATH] = fn # Image path
    textureNode[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_TEX0,c4d.REDSHIFT_FILE_COLORSPACE] = "RS_INPUT_COLORSPACE_RAW" # Color space
    textureNode[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_MIRRORU] = True # Mirror U
    textureNode[c4d.REDSHIFT_SHADER_TEXTURESAMPLER_MIRRORV] = True # Mirror V

    # RS Displacement Node
    displacementNode = rsnm.CreateNode(root, 1036227, None, x = 150, y = 400) # Create Displacement node
    displacementNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = "Displacement" # Set node type
    displacementInPort = displacementNode.AddPort(c4d.GV_PORT_INPUT, 10000) # Add Tex Map input port

    # Connect Nodes
    textureNode.GetOutPorts()[0].Connect(displacementInPort) # Connect
    displacementPort.Connect(displacementNode.GetOutPorts()[0]) # Connect
    # -------------------------------------------------------------------------------
    # Insert Material Tag
    textureTag = c4d.BaseTag(5616) # Initialize texture tag
    textureTag[c4d.TEXTURETAG_MATERIAL] = material # Assign material
    textureTag[c4d.TEXTURETAG_PROJECTION] = 6 # UVW Mapping
    terrainNull.InsertTag(textureTag) # Insert texture tag to object
    # -------------------------------------------------------------------------------
    # Insert objects
    terrainEditor.InsertUnder(terrainNull)
    terrainRender.InsertUnderLast(terrainNull)
    doc.InsertObject(terrainNull)
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, terrainNull)
    c4d.EventAdd() # Refresh Cinema 4D
    return

def main():
    doc.StartUndo() # Start recording undos

    fn = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,"Select reference file",c4d.FILESELECT_LOAD) # Load file
    if fn == None: return None # If no file, stop the script
    CreateGaeaTerrainSetup(fn) # Run the function

    doc.EndUndo() # Stop recording undos
    pass

# Execute main
if __name__ == '__main__':
    main()
    
