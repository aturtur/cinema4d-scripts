"""
AR_OpenBugReportsFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenBugReportsFolder
Version: 1.0.2
Description-US: Opens the bug reports folder.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.2 (26.04.2022) - Cleaning confusion
1.0.1 (25.04.2022) - Minor bug fix
"""

# Libraries
import os
import c4d
from c4d import storage

# Main function
def main():

    folder = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get preference folder path
    folder = os.path.dirname(r''+folder+'') # Go up
    folder = os.path.join(folder, '_bugreports') # Bug reports folder
    storage.ShowInFinder(folder, True) # Open the folder

# Execute main()
if __name__=='__main__':
    main()