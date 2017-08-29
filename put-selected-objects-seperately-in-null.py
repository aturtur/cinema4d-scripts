import c4d

def main():
    doc.StartUndo()
    selection = doc.GetSelection()
    
    for x in selection:
        null = c4d.BaseObject(c4d.Onull)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        x.InsertUnder(null)
        doc.InsertObject(null)
        doc.AddUndo(c4d.UNDOTYPE_NEW, null)

    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()