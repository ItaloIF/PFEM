import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)

# dimensiones
L = 5
H = 0.5
B = 0.25
ops.node(1,0.0,0.0)
ops.node(2,L,0.0)
ops.node(3,L,H)
ops.node(4,0.0,H)

# propiedad del material
mTag = 1
E = 24600000000
nu = 0.2
ops.nDMaterial('ElasticIsotropic', mTag, E, nu)
eleArgs = ['tri31', B, 'PlaneStress', mTag]

# creacion de la malla
ops.mesh('line', 1, 2, 1, 2, 1, 2, 0.25)
ops.mesh('line', 2, 2, 2, 3, 1, 2, 0.25)
ops.mesh('line', 3, 2, 3, 4, 1, 2, 0.25)
ops.mesh('line', 4, 2, 4, 1, 1, 2, 0.25)
ops.mesh('quad', 5, 4, 1, 2, 3, 4, 1, 2, 0.25,*eleArgs)

fig = plt.figure(figsize=(4,4))
opsv.plot_model()
plt.show()

# condiciones de frontera
ops.fixX(0.0, *[1,1], '-tol', 1e-10)

ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
fx = 0
fy = -10000
ops.load(2,*[fx,fy])
ops.load(3,*[fx,fy])
ops.load(24,*[fx,fy])

ops.system('FullGeneral')
ops.numberer('Plain')
ops.constraints('Plain')
ops.integrator('LoadControl',1)
ops.algorithm('Linear')
ops.analysis('Static')
ops.analyze(1)

# Grafico de la deformada
fig = plt.figure(figsize=(25,5))
opsv.plot_defo(2)
plt.show()