import openseespy.opensees as ops
import os
import math
from collections import defaultdict
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt

exec(open('source/tools.py').read())
exec(open('source/units.py').read())

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# lectura del  archivo msh
meshName = 'gmsh/mc2.msh'
  # generacion del diccionario
nodeDic = {(0,2): 1,(0,3): 1, (0,1): 2, (0,4): 2, (0,5): 2,
            (1,3): 1, (1,1): 2, (1,5): 2}
eleDic = {(2,1): 1}
Node, Ele = readMesh(meshName, nodeDic, eleDic)
nNode = len(Node)
nEle = len(Ele)

# paraview out
outPV('out/soil_dim3')

# definir y construir el material
mTg = 1
rho = 2000*kg/m**3  # densidad del suelo
Vs = 350.0*m/s # velocidad de inda de corte del suelo
G = rho*Vs*Vs # modulo de corte
nu = 0.15 # coeficiente de poisson
E = 2*G*(1+nu)
ops.nDMaterial('ElasticIsotropic', mTg, E, nu, rho)

# material de los bordes viscosos
lm = nu*E/((1+nu)*(1-2*nu))
Vc = math.sqrt((lm + 2*G)/rho)
Cn = rho*Vc
Ct = rho*Vs
ops.uniaxialMaterial('Viscous', 100, Cn, 1.0)
ops.uniaxialMaterial('Viscous', 101, Ct, 1.0)
# https://openseespydoc.readthedocs.io/en/latest/src/Viscous.html

# espesor de los elementos
B = 1*m

# construccion de nodos
for i in range(nNode):
    ops.node(i+1, *Node[i][1:])
  
# construccion de elementos
for i in range(nEle):
    if (Ele[i][0] == 1):
        ops.element('quad', i+1, *Ele[i][2:], B, 'PlaneStrain', Ele[i][0])

# condiciones de frontera
vsDic = {1: (100,101)}
boundVS(nNode, Node, nEle, nNode, vsDic)

# fuerza dinamica
ti = 0*s
tf = 0.2*s
fr = 20*Hz
prd = 1/fr
ops.timeSeries('Trig', 1, ti, tf, prd)
ops.pattern('Plain', 1, 1)
fx = 0
fy = -100*N
for i in range(nNode):
  if (Node[i][0] == 2):
    ops.load(i+1, fx, fy)

# amortiguamiento de rayleigh 
ops.rayleigh(*setRayParam(0.02, 0.02, 0.2, 20))

# analysis commands
ops.constraints('Plain')
ops.numberer('Plain')
ops.system('UmfPack')
ops.algorithm('Linear')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

# analisis
ops.start()
ops.analyze(400,0.001)
ops.stop()