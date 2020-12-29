import openseespy.opensees as ops
import openseespy.postprocessing.ops_vis as opsv
import matplotlib.pyplot as plt
ops.wipe()
ops.model('basic', '-ndm', 2, '-ndf', 2)
# creacion de nodos
ops.node(1, 0.0, 0.0)
ops.node(2, 5.0, 5.0)
ops.node(3, 0.0, 10.0)


# definir material
tgM = 1
E = 200000
ops.uniaxialMaterial('Elastic', tgM, E)
# https://openseespydoc.readthedocs.io/en/latest/src/uniaxialMaterial.html

# creacion de elementos
A = 5
ops.element('Truss',1,1,2,A,tgM) 
ops.element('Truss',2,*[2,3],A,tgM)
# https://openseespydoc.readthedocs.io/en/latest/src/element.html

# definir restricciones (Dirichlet)
ops.fix(1,1,1)
ops.fix(3,*[1,1])

# definir cargas (Neumann)
# creacion de una serie de tiempo
ops.timeSeries('Linear',1)
# https://openseespydoc.readthedocs.io/en/latest/src/timeSeries.html
# creacion de un 'pattern' o patron de carga
ops.pattern('Plain',1,1)
# https://openseespydoc.readthedocs.io/en/latest/src/pattern.html

ops.load(2,0.0,-100)

fig = plt.figure(figsize=(4,4))
opsv.plot_model()
# https://openseespydoc.readthedocs.io/en/latest/src/ops_vis.html
plt.show()

ops.system('FullGeneral')
# https://openseespydoc.readthedocs.io/en/latest/src/system.html
ops.numberer('Plain')
# https://openseespydoc.readthedocs.io/en/latest/src/numberer.html
ops.constraints('Plain')
# https://openseespydoc.readthedocs.io/en/latest/src/constraints.html
ops.integrator('LoadControl',1)
# https://openseespydoc.readthedocs.io/en/latest/src/integrator.html
ops.algorithm('Linear')
# https://openseespydoc.readthedocs.io/en/latest/src/algorithm.html
ops.analysis('Static')
# https://openseespydoc.readthedocs.io/en/latest/src/analysis.html
ops.analyze(1)

# Desplzamiento
disp = ops.nodeDisp(2)
print(disp)

# Fuerzas Internas
forceEle = ops.eleForce(1)
print(forceEle)

# Grafico de la deformada
fig = plt.figure(figsize=(4,4))
opsv.plot_defo(1000)
plt.show()