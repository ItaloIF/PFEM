import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
ops.wipe()
ops.model('basic', '-ndm', 3, '-ndf', 6)

ops.node(1, 0.0, 5.0, 5.0)
ops.node(2, 5.0, 5.0, 5.0)
ops.node(3, 5.0, 5.0, 0.0)
ops.node(4, 5.0, 0.0, 0.0)

E_mod = 1
G_mod = 1
Area = 4000000
Iy = 1000000
Iz = 300000
Jxx = 300000
ops.geomTransf('Linear', 1, *[0,1,0])
ops.geomTransf('Linear', 2, *[0,0,-1])
ops.element('elasticBeamColumn', 1, 1, 2, Area, E_mod, G_mod, Jxx, Iy, Iz, 1)
ops.element('elasticBeamColumn', 2, 3, 2, Area, E_mod, G_mod, Jxx, Iy, Iz, 1)
ops.element('elasticBeamColumn', 3, 4, 3, Area, E_mod, G_mod, Jxx, Iy, Iz, 2)

# definir restricciones (Dirichlet)
ops.fix(1,*[1,1,1,1,1,1])
ops.fix(4,*[1,1,1,1,1,1])

# definir cargas (Neumann)
ops.timeSeries('Linear',1)
ops.pattern('Plain',1,1)
ops.load(2,0.0,-100.0,0.0,0.0,0.0,0.0)

fig = plt.figure(figsize=(4,4))
opsv.plot_model()
#plt.show()

ops.system('FullGeneral')
ops.numberer('Plain')
ops.constraints('Plain')
ops.integrator('LoadControl',1)
ops.algorithm('Linear')
ops.analysis('Static')
ops.analyze(1)

# Desplazamiento
disp = ops.nodeDisp(2)
print(disp)

# Fuerzas Internas
forceEle = ops.eleForce(1)
print(forceEle)

# Grafico de la deformada
fig = plt.figure(figsize=(4,4))
opsv.plot_defo(200)
plt.show()