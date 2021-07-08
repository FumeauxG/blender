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

date_1 = datetime.datetime.now()
print("Start")

maxAngle = radians(10)
print(maxAngle, maxAngle*180/pi)

obj = bpy.context.active_object

# Add the vertices location in an array
tabVertices = []
for vertex in obj.data.vertices:
   tabVertices.append(obj.matrix_world @ vertex.co)
   
vecDir = mathutils.Vector((0,0,-1))


# Arrays for the function C parameters
tabPoly = []
tabNormalX = []
tabNormalY = []
tabNormalZ = []
tabFaces = []

tabPoint1X = []
tabPoint1Y = []
tabPoint2X = []
tabPoint2Y = []
tabPoint3X = []
tabPoint3Y = []
tabPoint1Z = []
tabPoint2Z = []
tabPoint3Z = []

# Fill the arrays
for poly in obj.data.polygons:
    tabPoly.append(poly.index)
    tabNormalX.append(poly.normal[0])
    tabNormalY.append(poly.normal[1])
    tabNormalZ.append(poly.normal[2])
    tabFaces.append(0)
    
    tabPoint1X.append(tabVertices[poly.vertices[0]].x)
    tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
    tabPoint2X.append(tabVertices[poly.vertices[1]].x)
    tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
    tabPoint3X.append(tabVertices[poly.vertices[2]].x)
    tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
    tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
    tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
    tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

print(len(tabPoly))   

# Get the C function
functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")
print(os.path.dirname(__file__))

# Create array for C function
seq = ctypes.c_int * len(tabPoly)
arrIndex = seq(*tabPoly)

seq = ctypes.c_float * len(tabNormalX)
arrNormalX = seq(*tabNormalX)
seq = ctypes.c_float * len(tabNormalY)
arrNormalY = seq(*tabNormalY)
seq = ctypes.c_float * len(tabNormalZ)
arrNormalZ = seq(*tabNormalZ)

seq = ctypes.c_int * len(tabFaces)
arrFaces = seq(*tabFaces)

seq = ctypes.c_float * len(tabPoint1X)
arrPoint1X = seq(*tabPoint1X)
seq = ctypes.c_float * len(tabPoint1Y)
arrPoint1Y = seq(*tabPoint1Y)
seq = ctypes.c_float * len(tabPoint2X)
arrPoint2X = seq(*tabPoint2X)
seq = ctypes.c_float * len(tabPoint2Y)
arrPoint2Y = seq(*tabPoint2Y)
seq = ctypes.c_float * len(tabPoint3X)
arrPoint3X = seq(*tabPoint3X)
seq = ctypes.c_float * len(tabPoint3Y)
arrPoint3Y = seq(*tabPoint3Y)
seq = ctypes.c_float * len(tabPoint1Z)
arrPoint1Z = seq(*tabPoint1Z)
seq = ctypes.c_float * len(tabPoint2Z)
arrPoint2Z = seq(*tabPoint2Z)
seq = ctypes.c_float * len(tabPoint3Z)
arrPoint3Z = seq(*tabPoint3Z)

date_3 = datetime.datetime.now()

# Call the C function
functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

date_4 = datetime.datetime.now()

# Switch in edit mode
bpy.ops.object.mode_set(mode = 'EDIT')
# Deselect all the faces
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Select all the faces needed support
for i in range(len(arrFaces)):
    if arrFaces[i] == 1:
        obj.data.polygons[tabPoly[i]].select = True
print(len(arrFaces))

# Switch in edit mode
bpy.ops.object.mode_set(mode = 'EDIT')
print("End")

date_2 = datetime.datetime.now()
time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()
print(total_seconds)

time_delta = (date_4 - date_3)
total_seconds = time_delta.total_seconds()
print("C time : ", total_seconds)

###############################################################

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

obj = bpy.context.active_object

# Get the name of the object
nameObject = obj.name

# Separate the selected faces
bpy.ops.mesh.separate(type='SELECTED')

# Switch in object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

# Select the support object
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]
bpy.data.objects[nameObject + ".001"].select_set(True)
bpy.data.objects[nameObject].select_set(False)

# Switch in edit mode
bpy.ops.object.mode_set(mode = 'EDIT')

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
# Unselect everything
bpy.ops.mesh.select_all(action="DESELECT")

# Load mesh
me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)
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
    
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
# Unselect everything
bpy.ops.mesh.select_all(action="DESELECT")
# Switch in object mode
bpy.ops.object.mode_set(mode='OBJECT')

for rows in range(len(loops)):
    #rows = 1
    for columns in loops[rows]:
        bpy.context.active_object.data.polygons[columns].select = True
    # Switch in edit mode
    bpy.ops.object.mode_set(mode='EDIT')   
    bpy.ops.transform.resize(value=(1.5, 1.5, 1.5), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, True, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.mesh.select_all(action='DESELECT')
    # Switch in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    print(rows)
    #break


# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 0.05), "orient_type":'NORMAL', "orient_matrix":((-0.717895, -0.696151, -2.50182e-07), (-0.696151, 0.717895, -2.93744e-07), (3.84095e-07, -3.67133e-08, -1)), "orient_matrix_type":'NORMAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Switch in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Select the object
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
bpy.data.objects[nameObject].select_set(True)
bpy.data.objects[nameObject + ".001"].select_set(True)

bpy.ops.object.join()

'''
bpy.context.object.location[2] = 0.001

# Select the object
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
bpy.data.objects[nameObject].select_set(True)
bpy.data.objects[nameObject + ".001"].select_set(False)

bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].operation = 'UNION'
bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[nameObject + ".001"]
bpy.context.object.modifiers["Boolean"].solver = 'FAST'
bpy.context.object.modifiers["Boolean"].double_threshold = 0
bpy.ops.object.apply_all_modifiers()

# Delete the copy
object_to_delete = bpy.data.objects[nameObject + ".001"]
bpy.data.objects.remove(object_to_delete, do_unlink=True) 
'''
