"""
AR_OpenBugReportsFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenBugReportsFolder
Version: 1.0.0 (2021.09.03)
Description-US: Opens the bug reports folder.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

"""

# Libraries
import os
import c4d
from c4d import storage

# Main function
def main():

    f = storage.GeGetC4DPath(c4d.C4D_PATH_PREFS) # Get preference folder path
    f = os.path.dirname(r''+f+'') # Go up
    f = os.path.join(f, '_bugreports') # Bug reports folder
    storage.ShowInFinder(f) # Open folder

# Execute main()
if __name__=='__main__':
    main()