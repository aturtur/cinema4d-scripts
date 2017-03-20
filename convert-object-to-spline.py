# convert selected object to spline
import c4d

def main():
    c4d.CallCommand(12236)      # make editable
    c4d.CallCommand(16351)      # edges mode
    c4d.CallCommand(12112)      # select all
    c4d.CallCommand(1009671)    # edge to spline
    c4d.CallCommand(1019951)    # delete without children
    
if __name__=='__main__':
    main()