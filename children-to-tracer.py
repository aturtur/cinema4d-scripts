import c4d

def main():
    doc.StartUndo()    
    active = doc.GetActiveObject()
    children = active.GetChildren()    
    tracer = c4d.BaseObject(1018655)
    tracerlist = c4d.InExcludeData()

    for x in children:
        tracerlist.InsertObject(x,1)
    
    tracer[c4d.MGTRACEROBJECT_OBJECTLIST] = tracerlist        
    doc.InsertObject(tracer)
    doc.AddUndo(c4d.UNDOTYPE_NEW, tracer)
    

    c4d.EventAdd()
    doc.EndUndo()

if __name__=='__main__':
    main()