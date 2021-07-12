import glob
import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
import mathutils
from math import pi
from math import radians
from math import sqrt
import datetime
import bmesh
import ctypes

# For import export
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class

import os

obj = bpy.context.active_object

nameCopy = "temp_copy"

nameObject = bpy.context.active_object.name

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')
# Make a copy of the object
new_obj = bpy.context.active_object.copy()
new_obj.data = bpy.context.active_object.data.copy()
new_obj.animation_data_clear()
bpy.context.collection.objects.link(new_obj)

# Rename the copy
new_obj.name = nameCopy

# Show the copy
new_obj.hide_viewport = True
new_obj.hide_viewport = False

# Select the copy
bpy.data.objects[nameObject].select_set(False)
bpy.data.objects[nameCopy].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[nameCopy]

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Select all the faces
bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=True, xstart=312, xend=839, ystart=150, yend=104, flip=False)


# Select all the faces
bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0, -0, -0.1), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Deselect all the faces
bpy.ops.mesh.select_all(action='DESELECT')

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

obj = bpy.context.active_object

# Find the mondial matrix of the mesh for the rotation of the mesh
matrix_new = obj.matrix_world.to_3x3().inverted().transposed()

for poly in obj.data.polygons:
    # Find the normal vector in function of the angles of the mesh               
    no_world = matrix_new @ poly.normal
    no_world.normalize()
    print(no_world)

    # Calculate the angle between the normal and the downward vector if the normal vector is no null
    if no_world != mathutils.Vector((0,0,0)):
        angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))
    else:
        angle = 0

    # Check if the angle is between the min and max angles z
    if angle < radians(91) and angle >  radians(89):
        # Select the faces and update min and max x and y location
        poly.select = True
      
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')  
      
bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_shrink_fatten={"value":0.2, "use_even_offset":False, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False, "use_accurate":False})

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT') 
    
# Select the
bpy.data.objects[nameObject].select_set(True)
bpy.data.objects[nameCopy].select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject] 

# Join the mesh and the bottom
bpy.ops.object.join()
