"""
Name-US: Template's Name
Description-US: Template's Description

Note: Create an image file 64x64 pixel resolution tiff-format with transparent background
and give it same name as the template script.
"""

# Libraries
import ar_modules

# Functions
def main():
    # File path of the template
    templatePath = ""

    # Import the template
    ar_modules.MergeDocument(
        path              = templatePath, # Template path
        objects           = True, # Import objects
        materials         = True, # Import materials
        documentSettings  = True, # Import project settings
        renderSettings    = True, # Import render settings
        viewportSettings  = True, # Import viewport settings
        camera            = True  # Set active camera
        ) # Template path

# Execute main()
if __name__=='__main__':
    main()