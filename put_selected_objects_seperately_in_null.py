import c4d

def main():
    selection = doc.GetSelection()
    
    for x in selection:
        null = c4d.BaseObject(c4d.Onull)
        x.InsertUnder(null)
        doc.InsertObject(null)
        
    c4d.EventAdd()

if __name__=='__main__':
    main()
