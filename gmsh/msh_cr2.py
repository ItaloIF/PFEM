import gmsh

# initial commands
gmsh.initialize()
gmsh.clear()
gmsh.option.setNumber('General.Terminal', 1)
msTg = 'gmsh/mc2'
gmsh.model.add(msTg)
gmg = gmsh.model.geo

# geometry (m)
R = 30

# define points 
ms = 1 # mesh size
gmg.addPoint(0, 0, 0, ms, 1) # load point
gmg.addPoint(-R, 0, 0, ms, 2)
gmg.addPoint(R, 0, 0, ms, 3)
gmg.addPoint(-5, 0, 0, ms, 4)
gmg.addPoint(5, 0, 0, ms, 5)

gmg.addLine(1, 4, 1)
gmg.addLine(4, 2, 2)
gmg.addCircleArc(2, 1, 3, 3)
gmg.addLine(3, 5, 4)
gmg.addLine(5, 1, 5)

gmg.addCurveLoop([1, 2, 3, 4, 5] , 1)

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