import bpy
import glob

print("Start")

obj = bpy.context.active_object
        
nameCopy = "diff_copy"

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Make a copy of the object
new_obj = obj.copy()
new_obj.data = obj.data.copy()
new_obj.animation_data_clear()
bpy.context.collection.objects.link(new_obj)

# Rename the copy
new_obj.name = nameCopy

# Show the copy
new_obj.hide_viewport = True
new_obj.hide_viewport = False

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

# Select the support object
bpy.data.objects[nameObject[0] + ".001"].select_set(True)
bpy.data.objects[nameObject[0]].select_set(False)

# Switch in edit mode
bpy.ops.object.mode_set(mode = 'EDIT')

# Select all the faces
bpy.ops.mesh.select_all(action='SELECT')

# Extrude the support
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Bissect and delete the element under the xy plane
#bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Select the base object
bpy.data.objects[nameObject[0] + ".001"].select_set(False)
bpy.data.objects[nameObject[0]].select_set(True)

# Delete the base object
bpy.ops.object.delete(use_global=False, confirm=False)

# Select the support
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
bpy.data.objects[nameObject[0] + ".001"].select_set(True)

# Add the mold
bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(bpy.data.objects[nameCopy].dimensions[0], bpy.data.objects[nameCopy].dimensions[1], 2))

# Align the mold in Z
bpy.ops.object.align(align_mode='OPT_3', relative_to='OPT_1', align_axis={'Z'})

# Select the copy
bpy.context.view_layer.objects.active = bpy.data.objects[nameCopy]
bpy.data.objects[nameCopy].select_set(True)

# Align the mold in x and y
bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'X'})
bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

# Select the mold
bpy.context.view_layer.objects.active = bpy.data.objects["Cube"]
bpy.data.objects[nameCopy].select_set(False)

# Margins x and y
bpy.data.objects["Cube"].dimensions = [bpy.data.objects["Cube"].dimensions[0] + 0.5, bpy.data.objects["Cube"].dimensions[1] + 0.5, bpy.data.objects["Cube"].dimensions[2] ]

# Delete the object to the mold
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].operation = 'DIFFERENCE'
bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[nameCopy]
bpy.context.object.modifiers["Boolean"].solver = 'FAST'
bpy.context.object.modifiers["Boolean"].double_threshold = 0
bpy.ops.object.apply_all_modifiers()

# Delete the copy
object_to_delete = bpy.data.objects[nameCopy]
bpy.data.objects.remove(object_to_delete, do_unlink=True) 

# Select the support
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
bpy.data.objects[nameObject[0] + ".001"].select_set(True)
bpy.data.objects["Cube"].select_set(False)

# Merge the mold to the support
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["Cube"]
bpy.context.object.modifiers["Boolean"].solver = 'FAST'
bpy.context.object.modifiers["Boolean"].double_threshold = 0
bpy.ops.object.apply_all_modifiers()

# Delete the mold
object_to_delete = bpy.data.objects["Cube"]
bpy.data.objects.remove(object_to_delete, do_unlink=True)

# Export the stl file
bpy.ops.export_mesh.stl(filepath=pathOut)

print("End Script")