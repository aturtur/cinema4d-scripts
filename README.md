# Cinema 4D Sripts

My collection of Maxon Cinema 4D scripts.

## Scripts for Script Manager
#### Add materials to objects with same name
This script simply adds materials to objects that have exaclty same name as the material.

#### Add nulls with constraint tags to selected points
This script creates null objects to polygon objects's selected points. UPDATED2: Now it works with multiple objects.

#### Children to tracer
This script creates a tracer object and puts selected object's children on it.

#### Clone own materials
This script creates individual materials for selected objects from existing texture tags.

#### Convert object to spline
This script simply converts polygon object to spline object.

#### Create spline from selected nulls
This script creates spline object from selected null objects. UPDATED: Now you can give subdivisions count.

#### Get XPresso node ID
This script prints the first XPresso node's ID to console. Select only the XPresso tag and run the script.

#### Hex to material
This script gives you a input dialog where you can put HEX color value and then it makes a material from it.

#### Import image folder
This script imports image folder and makes individual materials from image files.

#### Import obj folder
This script imports folder and merges every object on it to the current project.

### Make dynamic spline with control points
Select a spline or bunch of splines and run this script. The script makes splines dynamic and adds null controllers.

### Make dynamic spline between selected nulls
Select two nulls and run the script. 

#### MML ASC to point cloud
This script imports ASC files from MML (maanmittauslaitos) [NLS (national land survey of finland)] and creates polygon objects with points. More info: https://tiedostopalvelu.maanmittauslaitos.fi/tp/kartta?lang=fi
Elevation model - ASC file to point cloud.

#### Nulls to points
This script creates points to one polygon object from selected nulls.

#### Pixeur color palette to materials
This script imports Pixeur color palette file and makes individual materials from it.

#### Projector camera
This is some random script that I should delete.

#### Put selected objects seperately in Null
This script puts selected objects seperately in a null object.

#### Randomise selected objects color
This script randomises selected objects color.

#### Randomise selected objects position
This script randomises selected objects position. Minumum and maximum values and axis restriction are hard coded.

#### Voronoi pattern plane
This script makes a plane with voronoi pattern. Useless script for fun.

## Scripts for Python Tag
#### Tag color object with layer color
This script will colorize object with layer color. You just need to enable "Use Color" in "Basic" tab.

#### Tag show if correct camera
This script shows the object if correct camera is active. You need to put manually one user data field.

#### Tag show only if active
This script hides object when it is unactive and shows it when it is active. Very handy python tag with deformers and effectors.

#### Tag toggle background by activating camera
This script toggles background and/or foreground object depending is the camera active. You need to two add user data fields manually.

## Templates
#### Template input qualifiers
Template for input qualifiers. When you run the script and hold Ctrl, Shift or Alt same time.

#### Template XPresso node
Template for creating and connecting XPresso nodes.