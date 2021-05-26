import bpy
import bmesh

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode='EDIT', toggle=False) # Go to edit mode
bpy.ops.mesh.select_all(action="DESELECT") # unselect everything

bm = bmesh.from_edit_mesh(obj.data) # load mesh
bm.faces.ensure_lookup_table()

loops = []
faces = bm.faces

while faces:
    faces[0].select_set(True) # select 1st face
    bpy.ops.mesh.select_linked() # select all linked faces makes a full loop
    loops.append([f.index for f in faces if f.select])
    bpy.ops.mesh.hide(unselected=False) # hide the detected loop
    faces = [f for f in bm.faces if not f.hide] # update faces

bpy.ops.mesh.reveal() # unhide all faces
print("Mesh has {} parts".format(len(loops)))

print("\nThe face lists are:")
for loop in loops:
    print(loop)

bpy.ops.mesh.select_all(action="DESELECT") # unselect everything
bpy.ops.object.mode_set(mode='OBJECT') # Go to edit mode
#for loop in loops[0]:
#    bpy.context.active_object.data.polygons[loop].select = True
#    print(loop)

area = 0 
for rows in range(len(loops)):
    area = 0
    for columns in loops[rows]:
        area = area + bpy.context.active_object.data.polygons[columns].area
    print(rows)
    print(area)
    if area > 0.1:
        for columns in loops[rows]:
            bpy.context.active_object.data.polygons[columns].select = True
    
bpy.ops.object.mode_set(mode='EDIT') # Go to edit mode

