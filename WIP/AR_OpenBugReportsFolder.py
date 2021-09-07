"""
AR_OpenBugReportsFolder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_OpenBugReportsFolder
Version: 1.0.0 (2021.09.03)
Description-US: Opens bug reports folder

Written for Maxon Cinema 4D R21.207
Python version 2.7.14

"""

# Libraries
import os
import c4d
from c4d import storage as s

# Main function
def main():

    f = s.GeGetC4DPath(c4d.C4D_PATH_PREFS)
    f = os.path.dirname(r''+f+'')
    f = os.path.join(f, '_bugreports')
    s.ShowInFinder(f)

# Execute main()
if __name__=='__main__':
    main()