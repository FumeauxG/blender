###########################
# Test automatized Blender 3
# Author : Fumeaux Gaëtan
# v1.0
###########################
# Conditions to start :
# - One object selected
###########################


import glob
import bpy
import mathutils

print("Start Script")

# Delete the existing cube or support
object_to_delete = bpy.context.selected_objects[0]
bpy.data.objects.remove(object_to_delete, do_unlink=True)

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

# Import the stl file
bpy.ops.import_mesh.stl(filepath=pathIn)

# Rename the base object
bpy.context.selected_objects[0].name = nameObject[0]

# Align the object on the xy plane
bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})

############################################################################################
# Math calculation
pi = 3.14159265
maxAngle = 60
maxAngleRad = maxAngle*pi/180

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')

tabVertices = []
for vertex in obj.data.vertices:
   tabVertices.append(obj.matrix_world @ vertex.co) 
    
for poly in obj.data.polygons:
    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
    if angle < maxAngleRad:
        poly.select = True
        
        triangleCenter = (tabVertices[poly.vertices[0]]+tabVertices[poly.vertices[1]]+tabVertices[poly.vertices[2]])/3
                
        for comparePoly in obj.data.polygons:
            if  (mathutils.geometry.intersect_ray_tri(tabVertices[comparePoly.vertices[0]], tabVertices[comparePoly.vertices[1]], tabVertices[comparePoly.vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != comparePoly.index):
                poly.select = False
                break
                

bpy.ops.object.mode_set(mode = 'EDIT')
############################################################################################

# Separate the selected faces
bpy.ops.mesh.separate(type='SELECTED')

# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Select the support object
bpy.data.objects[nameObject[0] + ".001"].select_set(True)
bpy.data.objects[nameObject[0]].select_set(False)

# Switch in edit mode
bpy.ops.object.mode_set(mode = 'EDIT')

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Extrude the support
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Bissect and delete the element under the xy plane
bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Select the support object
bpy.data.objects[nameObject[0] + ".001"].select_set(False)
bpy.data.objects[nameObject[0]].select_set(True)

# Delete the base object
bpy.ops.object.delete(use_global=False, confirm=False)

# Export the stl file
bpy.ops.export_mesh.stl(filepath=pathOut)

# Select the support
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
bpy.data.objects[nameObject[0] + ".001"].select_set(True)

print("End Script")