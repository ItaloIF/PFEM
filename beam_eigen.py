import openseespy.opensees as ops
from collections import defaultdict
import math
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt

exec(open('source/tools.py').read())
exec(open('source/units.py').read())

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# lectura del  archivo msh
meshName = 'gmsh/beam2.msh'
  # generacion del diccionario
nodeDic = {(0,1): 1,(0,4): 1, (0,2): 2, (0,3): 2,
            (1,4): 1, (1,2): 2}
eleDic = {(2,1): 1}
Node, Ele = readMesh(meshName, nodeDic, eleDic)
nNode = len(Node)
nEle = len(Ele)

# definir y construir el material
mTg = 1
rho = 2400*kg/m**3
nu = 0.20 # Poisson's ratio of soil
E = 2460000*N/cm**2
ops.nDMaterial('ElasticIsotropic', mTg, E, nu, rho)

# espesor de los elementos
B = 0.25*m

# construccion de nodos
for i in range(nNode):
    ops.node(i+1, *Node[i][1:])
  
# construccion de elementos
for i in range(nEle):
    if (Ele[i][0] == 1):
        ops.element('quad', i+1, *Ele[i][2:], B, 'PlaneStress', Ele[i][0])

# condiciones de frontera
boundFix(nNode, Node)

# calculo de los modos de vibracion
Nmodes = 6
Tmodes = ops.eigen(Nmodes)
for i in range(Nmodes):
    Tmodes[i] = 2*math.pi/Tmodes[i]**0.5
print(Tmodes)

# Grafico de la deformada
fig = plt.figure(figsize=(10,10))
opsv.plot_mode_shape(4, sfac=10)
plt.show()