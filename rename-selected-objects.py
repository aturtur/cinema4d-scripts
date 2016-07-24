# rename selected objects from n to n(selected items)
import c4d

def main():
    n = 1    
    s = doc.GetSelection()    
    doc.StartUndo()
    for x in s: 
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)
        x.SetName(n)
        n = n+1
    doc.EndUndo()
    
    c4d.EventAdd()

if __name__=='__main__':
    main()
