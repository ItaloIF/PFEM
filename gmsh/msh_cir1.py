import gmsh

# initial commands
gmsh.initialize()
gmsh.clear()
gmsh.option.setNumber('General.Terminal', 1)
msTg = 'gmsh/mc1'
gmsh.model.add(msTg)
gmg = gmsh.model.geo

# geometry (m)
R = 30

# define points 
ms = 1 # mesh size
gmg.addPoint(0, 0, 0, ms, 1) # load point
gmg.addPoint(-R, 0, 0, ms, 2)
gmg.addPoint(R, 0, 0, ms, 3)

gmg.addLine(1, 2, 1)
gmg.addCircleArc(2, 1, 3, 2)
gmg.addLine(3, 1, 3)

gmg.addCurveLoop([1, 2, 3] , 1)

# define surface
gmg.addPlaneSurface([1], 1)

# transforme tri to  quad
gmsh.model.geo.synchronize()
gmsh.model.geo.mesh.setRecombine(2, 1)

#mesh generate
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write(msTg + '.msh')
gmsh.fltk.run()
gmsh.finalize()