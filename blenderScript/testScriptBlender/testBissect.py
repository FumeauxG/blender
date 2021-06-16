import bpy
import bmesh
import mathutils
import datetime

date_1 = datetime.datetime.now()
print("START")

pi = 3.14159265

obj = bpy.context.active_object

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)

tabExtrudeFaces = []
tabOtherFaces = []

matrix_new = obj.matrix_world.to_3x3().inverted().transposed()
k = 0
for poly in bm.faces:
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
        poly.select = True
        poly.hide = True
        
    else:
        tabExtrudeFaces.append(poly)

bpy.ops.mesh.region_to_loop()
bmesh.update_edit_mesh(me) 
        
#for i in range(len(tabOtherFaces)):
#    print(i)
#    bpy.ops.mesh.select_all(action='SELECT')
#    bpy.ops.mesh.bisect(plane_co=(0, 0, (obj.matrix_world @ tabOtherFaces[i].calc_center_median())[2]), plane_no=(0, 0, 1), xstart=339, xend=946, ystart=232, yend=249, flip=False)

grow_faces = set(v for v in bm.verts if v.select)      

for v in grow_faces:
    print(v.index)
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, (obj.matrix_world @ v.co)[2]), plane_no=(0, 0, 1), xstart=339, xend=946, ystart=232, yend=249, flip=False)
    
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.mesh.reveal(select = False) # unhide all faces
bmesh.update_edit_mesh(me)  

print("End Script")

date_2 = datetime.datetime.now()
time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()
print("Time : ", total_seconds)   