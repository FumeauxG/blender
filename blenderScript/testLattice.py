import bpy
import mathutils

#bpy.data.lattices['Lattice'].points[0].co_deform = mathutils.Vector((-1, -1, -1))
#bpy.data.lattices['Lattice'].points[1].co_deform = mathutils.Vector((1, -1, -1))
#bpy.data.lattices['Lattice'].points[2].co_deform = mathutils.Vector((-1, 1, -1))
#bpy.data.lattices['Lattice'].points[3].co_deform = mathutils.Vector((1, 1, -1))
#bpy.data.lattices['Lattice'].points[4].co_deform = mathutils.Vector((-1, -1, 1))
#bpy.data.lattices['Lattice'].points[5].co_deform = mathutils.Vector((1, -1, 1))
#bpy.data.lattices['Lattice'].points[6].co_deform = mathutils.Vector((-1, 1, 1))
#bpy.data.lattices['Lattice'].points[7].co_deform = mathutils.Vector((1, 1, 1))

obj = bpy.context.active_object

xPlus = float('-inf')
xMoins = float('inf')
yPlus = float('-inf')
yMoins = float('inf')
zPlus = float('-inf')
zMoins = float('inf')

tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(obj.matrix_world @ vertex.co)
    if xPlus < (obj.matrix_world @ vertex.co).x:
        xPlus = (obj.matrix_world @ vertex.co).x
    elif xMoins > (obj.matrix_world @ vertex.co).x:
        xMoins = (obj.matrix_world @ vertex.co).x
        
    if yPlus < (obj.matrix_world @ vertex.co).y:
        yPlus = (obj.matrix_world @ vertex.co).y
    elif yMoins > (obj.matrix_world @ vertex.co).y:
        yMoins = (obj.matrix_world @ vertex.co).y
        
    if zPlus < (obj.matrix_world @ vertex.co).z:
        zPlus = (obj.matrix_world @ vertex.co).z
    elif zMoins > (obj.matrix_world @ vertex.co).z:
        zMoins = (obj.matrix_world @ vertex.co).z

print(obj.matrix_world @ obj.dimensions)
print(obj.dimensions)
bpy.data.lattices['Lattice'].points[0].co_deform = mathutils.Vector((xMoins,yMoins,zMoins))
bpy.data.lattices['Lattice'].points[1].co_deform = mathutils.Vector((xPlus,yMoins,zMoins))
bpy.data.lattices['Lattice'].points[2].co_deform = mathutils.Vector((xMoins,yPlus,zMoins))
bpy.data.lattices['Lattice'].points[3].co_deform = mathutils.Vector((xPlus,yPlus,zMoins))
bpy.data.lattices['Lattice'].points[4].co_deform = mathutils.Vector((xMoins,yMoins,zPlus))
bpy.data.lattices['Lattice'].points[5].co_deform = mathutils.Vector((xPlus,yMoins,zPlus))
bpy.data.lattices['Lattice'].points[6].co_deform = mathutils.Vector((xMoins,yPlus,zPlus))
bpy.data.lattices['Lattice'].points[7].co_deform = mathutils.Vector((xPlus,yPlus,zPlus))


