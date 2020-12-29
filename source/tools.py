def outPV(outName):
    if not os.path.exists(outName):
        os.makedirs(outName)
    ops.recorder('PVD', outName, 'disp')
    return None

def readMesh(meshName ,nodeDic, eleDic):
    # msh file version ASCII 4.1
    f = open(meshName,'r')
    nodeDic = defaultdict(lambda:0, nodeDic)
    eleDic = defaultdict(lambda:0, eleDic)
    Node = []
    Ele = []
    # read nodes
    while True:
        if(f.readline().split()[0] == "$Nodes"):
            break
    [nEnt, nNode] = list(map(int,f.readline().split()))[0:-2]
    for i in range(nEnt):
        dataEnt = list(map(int,f.readline().split()))
        for j in range(dataEnt[3]):
            f.readline()
        for j in range(dataEnt[3]):
            Node.append([nodeDic[dataEnt[0],dataEnt[1]]] + list(map(float,f.readline().split()))[0:-1])
    
    # read elements
    while True:
        if(f.readline().split()[0] == "$Elements"):
            break  
    [nEnt, nEle] = list(map(int,f.readline().split()))[0:-2]
    for i in range(nEnt):
        dataEnt = list(map(int,f.readline().split()))
        if (eleDic[dataEnt[0],dataEnt[1]] != 0):
            for j in range(dataEnt[3]):
                Ele.append([eleDic[dataEnt[0],dataEnt[1]]] + list(map(int,f.readline().split())))
        else:
            for j in range(dataEnt[3]):
                f.readline()
    f.close()
    return Node, Ele

# rayleigh damping parameters
def setRayParam(bi, bj, fi, fj):
    wi = 2*math.pi*fi#rad/s
    wj = 2*math.pi*fj #rad/s
    alphaM = 2*wi*wj*(bi*wj-bj*wi)/(wj**2-wi**2)
    betaK = 0.0
    betaK0 = 0.0
    betaKc = 2*(bj*wj-bi*wi)/(wj**2-wi**2)  
    return  alphaM, betaK, betaK0, betaKc

def boundFix(nNode, Node):
    for i in range(nNode):
        if (Node[i][0] == 1):
            ops.fix(i+1, *[1,1])
    return None

def boundVS(nNode, Node, idmEle, idmNode, vsDic):
    for i in range(nNode):
        if (Node[i][0] == 1):
            idmNode+=1
            ops.node(idmNode, *Node[i][1:])
            ops.fix(idmNode,*[1,1])
            idmEle+=1
            ops.element('zeroLength',idmEle,i+1,idmNode,'-mat',*vsDic[Node[i][0]],'-dir',1,2)
    return None