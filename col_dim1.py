import openseespy.opensees as ops
from collections import defaultdict
import os
import math
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt

exec(open('source/tools.py').read())
exec(open('source/units.py').read())

ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# lectura del  archivo msh
meshName = 'gmsh/col1.msh'
  # generacion del diccionario
nodeDic = {(0,1): 1,(0,2): 1,
            (1,1): 1}
eleDic = {(2,1): 1}
Node, Ele = readMesh(meshName, nodeDic, eleDic)
nNode = len(Node)
nEle = len(Ele)

# paraview out
outPV('out/col_dim1')

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

# fuerza dinamica
ti = 0*s
tf = 0.2*s
fr = 10*Hz
prd = 1/fr
ops.timeSeries('Trig', 1, ti, tf, prd)
# https://openseespydoc.readthedocs.io/en/latest/src/pathTs.html
ops.pattern('UniformExcitation', 1, 1, '-accel', 1)
# https://openseespydoc.readthedocs.io/en/latest/src/uniformExcitation.html

# amortiguamiento de rayleigh 
ops.rayleigh(*setRayParam(0.05, 0.05, 0.2, 20))

# analysis commands
ops.constraints('Plain')
ops.numberer('Plain')
ops.system('UmfPack')
ops.algorithm('Linear')
ops.integrator('Newmark', 0.5, 0.25)
ops.analysis('Transient')

# analisis
# ops.analyze(400,0.001)
ops.start()
for i in range(400):
    ops.analyze(1,0.001)
    print(i)
ops.stop()

# Grafico de la deformada
fig = plt.figure(figsize=(25,5))
opsv.plot_defo(500)
plt.show()