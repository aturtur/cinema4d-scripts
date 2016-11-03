import c4d

def main():
    doc.StartUndo()
    s = doc.GetSelection()    
    for x in s:                
        p = x.GetUp()
        doc.AddUndo(c4d.UNDOTYPE_BITS, x)
        x.DelBit(c4d.BIT_ACTIVE)
        doc.AddUndo(c4d.UNDOTYPE_BITS, p)
        p.SetBit(c4d.BIT_ACTIVE)
    c4d.EventAdd()
    doc.EndUndo()
    
if __name__=='__main__':
    main()