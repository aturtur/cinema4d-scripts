import c4d

def main():
    doc = c4d.documents.GetActiveDocument()
    selo = doc.GetActiveObjects(0)
    if len(selo) > 0:
        for o in selo:
                select_points = o.GetPointS()
                pc = len(o.GetAllPoints())
                select_points.DeselectAll()
                select_points.Select(0)
                name = o.GetName()
                nulla = c4d.BaseObject(c4d.Onull)
                if nulla is None:
                    return
                nulla[c4d.NULLOBJECT_DISPLAY] = 2
                nulla.SetAbsPos(c4d.Vector(o.GetPoint(0)[0],o.GetPoint(0)[1],o.GetPoint(0)[2]))
                nulla.SetName(name+" A")
                doc.InsertObject(nulla)
                aTag = o.MakeTag(1018074)
                aTag[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = nulla
                doc.ExecutePasses(None, 0, 1, 1, 0)
                c4d.CallButton(aTag, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR)
                c4d.EventAdd()                
                select_points.DeselectAll()
                select_points.Select(pc-1)
                nullb = c4d.BaseObject(c4d.Onull)
                if nullb is None:
                    return
                nullb[c4d.NULLOBJECT_DISPLAY] = 2
                nullb.SetAbsPos(c4d.Vector(o.GetPoint(pc-1)[0],o.GetPoint(pc-1)[1],o.GetPoint(pc-1)[2]))
                nullb.SetName(name+" B")
                doc.InsertObject(nullb)
                bTag = o.MakeTag(1018074)
                bTag[c4d.HAIR_CONSTRAINTS_TAG_ANCHOR_LINK] = nullb
                doc.ExecutePasses(None, 0, 1, 1, 0)
                c4d.CallButton(bTag, c4d.HAIR_CONSTRAINTS_TAG_SET_ANCHOR)
                c4d.EventAdd()                
                o.InsertTag(c4d.BaseTag(1018068))
    c4d.EventAdd()
    
if __name__ == "__main__":
    main()