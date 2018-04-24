import c4d

def main():
    doc.StartUndo()
    s = doc.GetSelection()
    c = 0
    for x in s:
        if c != 0:
            copy = s[0].GetClone()
            copy.InsertUnder(x)
            doc.AddUndo(c4d.UNDOTYPE_NEW, copy)
        else:
            c=c+1
    c4d.EventAdd()
    doc.EndUndo()
if __name__=='__main__':
    main()
