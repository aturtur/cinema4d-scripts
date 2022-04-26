"""
AR_OpenBugReportsFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenBugReportsFolder
Version: 1.0.1
Description-US: Opens the bug reports folder.

Written for Maxon Cinema 4D R25.117
Python version 3.9.1

Change log:
1.0.1 (25.04.2022) - Fixed that the folder opens and not the parent folder
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

    if c4d.GeGetCurrentOS() == c4d.OPERATINGSYSTEM_WIN: # If operating system is Windows
        os.startfile(folder)
    else: # If operating system is Mac
        os.system('open "%s"' % folder)
        
# Execute main()
if __name__=='__main__':
    main()