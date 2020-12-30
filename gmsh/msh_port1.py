import gmsh

# initial commands
gmsh.initialize()
gmsh.clear()
gmsh.option.setNumber('General.Terminal', 1)
msTg = 'port1'
gmsh.model.add(msTg)
gmg = gmsh.model.geo

# geometry (m)
Lx = 5.0
Ly = 4.0
H = 0.5

# define points 
ms = 0.10 # mesh size
gmg.addPoint(0, 0, 0, ms, 1) 
gmg.addPoint(H, 0, 0, ms, 2)
gmg.addPoint(H, Ly-H, 0, ms, 3)
gmg.addPoint(Lx-H, Ly-H, 0, ms, 4)
gmg.addPoint(Lx-H, 0, 0, ms, 5)
gmg.addPoint(Lx, 0, 0, ms, 6)
gmg.addPoint(Lx, Ly, 0, ms, 7)
gmg.addPoint(0, Ly, 0, ms, 8)

# define lines
gmg.addLine(1, 2, 1)
gmg.addLine(2, 3, 2)
gmg.addLine(3, 4, 3)
gmg.addLine(4, 5, 4)
gmg.addLine(5, 6, 5)
gmg.addLine(6, 7, 6)
gmg.addLine(7, 8, 7)
gmg.addLine(8, 1, 8)


gmsh.model.geo.addCurveLoop([1, 2, 3, 4, 5, 6, 7, 8] , 1)

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