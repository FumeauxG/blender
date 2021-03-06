import glob
import bpy
import bmesh

# Find the stl files
txtfiles = []
for file in glob.glob("C:/Gaetan/_Bachelor/blender/blenderScript/test/*.stl"):
    txtfiles.append(file)
# Choose the first stl file
pathIn = txtfiles[0]
print(txtfiles[0])

# out file
pathTemp = pathIn.split('.')
pathOut = pathTemp[0] + '_support.' + pathTemp[1]

# Find the name of the object
nameTemp = pathIn.split("\\")
print(nameTemp[1])
nameObject = nameTemp[1].split(".")
print(nameObject[0])

# Separate the selected faces
bpy.ops.mesh.separate(type='SELECTED')

# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Set support as active pbject
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]

# Delete the base object
object_to_delete = bpy.data.objects[nameObject[0]]
bpy.data.objects.remove(object_to_delete, do_unlink=True)


obj = bpy.context.active_object

# Switch in object mode
bpy.ops.object.mode_set(mode='EDIT')

# Unselect everything
bpy.ops.mesh.select_all(action="DESELECT")

# Load mesh
bm = bmesh.from_edit_mesh(bpy.context.selected_objects[0].data)
bm.faces.ensure_lookup_table()

loops = []
faces = bm.faces

while faces:
    faces[0].select_set(True)                   # select 1st face
    bpy.ops.mesh.select_linked()                # select all linked faces makes a full loop
    loops.append([f.index for f in faces if f.select])
    bpy.ops.mesh.hide(unselected=False)         # hide the detected loop
    faces = [f for f in bm.faces if not f.hide] # update faces

bpy.ops.mesh.reveal() # unhide all faces
print("Mesh has {} parts".format(len(loops)))

print("\nThe face lists are:")
for loop in loops:
    print(loop)

# Unselect everything
bpy.ops.mesh.select_all(action="DESELECT")

# Switch in edit mode
bpy.ops.object.mode_set(mode='OBJECT')

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

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Separate the selected faces
bpy.ops.mesh.separate(type='SELECTED')

# Set final support as active pbject
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".002"]

# Delete the temp support
object_to_delete = bpy.data.objects[nameObject[0] + ".001"]
bpy.data.objects.remove(object_to_delete, do_unlink=True)

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Extrude the support
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Bissect and delete the element under the xy plane
bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

# Export the stl file
bpy.ops.export_mesh.stl(filepath=pathOut)

print("End Script")