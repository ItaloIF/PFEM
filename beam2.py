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
nu = 0.15 # Poisson's ratio of soil
E = 2460000*N/cm**2
ops.nDMaterial('ElasticIsotropic', mTg, E, nu)

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

ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
fx = 0
fy = -10*kN
ops.load(2, fx, fy)
#for i in range(nNode):
#    if (Node[i][0] == 2):
#        ops.load(i+1, fx, fy)

ops.system('FullGeneral') # probar otros solvers: 'UmfPack' 'SparseSYM'
ops.numberer('Plain')
ops.constraints('Plain')
ops.integrator('LoadControl',1)
ops.algorithm('Linear')
ops.analysis('Static')
ops.start()
ops.analyze(1)
ops.stop()

# Grafico de la deformada
fig = plt.figure(figsize=(25,5))
opsv.plot_defo(50)
plt.show()

fig = plt.figure(figsize=(50,10))
opsv.plot_model()
plt.show()

# Desplazamiento
disp = ops.nodeDisp(2,2)
print(disp)

# plot esfuerzos quad 2D
fig = plt.figure(figsize=(50,10))
sig_out = opsv.quad_sig_out_per_node() 
# componentes: sxx, syy, sxy, svm, s1, s2, angle. (n_nodes x 7)
opsv.plot_stress_2d(sig_out[:, 1], mesh_outline=1, cmap='plasma')
#plt.colorbar()
plt.show()

# plot esfuerzos en los puntos de integracion quad 2D
fig = plt.figure(figsize=(100,20))
eles_ips_crd, eles_nds_crd, nds_crd, quads_conn = opsv.quad_crds_node_to_ip()
eles_ips_sig_out, eles_nds_sig_out = opsv.quad_sig_out_per_ele()
opsv.plot_mesh_with_ips_2d(nds_crd, eles_ips_crd, eles_nds_crd, quads_conn,
                           eles_ips_sig_out, eles_nds_sig_out, 0)
plt.show()