import gmsh

# initial commands
gmsh.initialize()
gmsh.clear()
gmsh.option.setNumber('General.Terminal', 1)
msTg = 'beam1'
gmsh.model.add(msTg)
gmg = gmsh.model.geo

# geometry (m)
L = 5.0
H = 0.5

# define points 
ms = 0.10 # mesh size
gmg.addPoint(0, 0, 0, ms, 1) # load point
gmg.addPoint(L, 0, 0, ms, 2)
gmg.addPoint(L, H, 0, ms, 3)
gmg.addPoint(0, H, 0, ms, 4)

# define lines
gmg.addLine(1, 2, 1)
gmg.addLine(2, 3, 2)
gmg.addLine(3, 4, 3)
gmg.addLine(4, 1, 4)

gmsh.model.geo.addCurveLoop([1, 2, 3, 4] , 1)

# define surface
gmsh.model.geo.addPlaneSurface([1], 1)

# transforme tri to  quad
gmsh.model.geo.synchronize()
gmsh.model.geo.mesh.setRecombine(2, 1)

#mesh generate
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.fltk.run()
gmsh.write(msTg + '.msh')
gmsh.finalize()