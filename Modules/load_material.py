"""
Name-US: Material's Name
Description-US: Material's Description

Note: Create an image file 64x64 pixel resolution tiff-format with transparent background
and give it same name as the material script.
"""

# Libraries
import ar_modules

# Functions
def main():
    # File path of the template
    materialPath = ""

    # Import the template
    ar_modules.ImportMaterial(
        path = materialPath,    # Material path
        add  = True             # Apply material to selected object(s)
    )

# Execute main()
if __name__=='__main__':
    main()