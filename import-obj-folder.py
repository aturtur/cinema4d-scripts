import c4d
from c4d import storage as s
import os

def main():
    folder = s.LoadDialog(c4d.FILESELECTTYPE_ANYTHING,'Select folder to import',c4d.FILESELECT_DIRECTORY,'')
    if not folder: return
    files = os.listdir(folder)
    for f in files:
        c4d.documents.MergeDocument(doc, folder+'\\'+f, 1)
    c4d.EventAdd()
if __name__=='__main__':
    main()