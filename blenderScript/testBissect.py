import bpy
import mathutils

print("START")

pi = 3.14159265

obj = bpy.context.active_object

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')


tabExtrudeFaces = []
tabOtherFaces = []

matrix_new = obj.matrix_world.to_3x3().inverted().transposed()
k = 0
for poly in obj.data.polygons:
    #print(poly.index)
    #bpy.ops.mesh.select_all(action = 'SELECT')
    #bpy.ops.mesh.bisect(plane_co=(0, 0, (obj.matrix_world @ poly.center)[2]), plane_no=(0, 0, 1), xstart=339, xend=946, ystart=232, yend=249, flip=False)
    no_world = matrix_new @ poly.normal
    no_world.normalize()
    angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))*180/pi
    if angle < 89.9 or angle > 90.1:
        k = k+1
        print(k)
        tabOtherFaces.append(poly)
        poly.hide = True
        
    else:
        tabExtrudeFaces.append(poly)
        
for i in range(len(tabOtherFaces)):
    print(i)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, (obj.matrix_world @ tabOtherFaces[i].center)[2]), plane_no=(0, 0, 1), xstart=339, xend=946, ystart=232, yend=249, flip=False)
      
bpy.ops.mesh.reveal(select = False) # unhide all faces

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

print("End Script")