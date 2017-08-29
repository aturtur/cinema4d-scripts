import c4d

def GetNextObject(op):
    if op==None:
        return None  
    if op.GetDown():
        return op.GetDown()  
    while not op.GetNext() and op.GetUp():
        op = op.GetUp()  
    return op.GetNext() 
 
def IterateHierarchy(op):
    if op is None:
        return 
    count = 0  
    while op:
        count += 1
        print op.GetName()
        op = GetNextObject(op) 
    return count

def main():
    start_object = doc.GetFirstObject()
    count = IterateHierarchy(start_object)
    print "Iterated " + str(count) + " objects."
  
if __name__=='__main__':
    main()