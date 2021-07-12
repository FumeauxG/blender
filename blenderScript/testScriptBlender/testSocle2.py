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

nameObject = bpy.context.active_object.name

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Select all the faces
bpy.ops.mesh.select_all(action='SELECT')

# Delete the actual bottom
bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), clear_inner=True, xstart=187, xend=982, ystart=219, yend=247, flip=False)

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

# Get the active object
obj = bpy.context.active_object

# Get the min and max location in x and y of the mesh
xMax = float('-inf')
xMin = float('inf')
yMax = float('-inf')
yMin = float('inf')
for poly in obj.data.polygons:
    xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
    xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
    yMax = max(yMax, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
    yMin = min(yMin, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
print(xMax,xMin,yMax,yMin)
# Add the new bottom
bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.002),rotation=(3.14159, 0, 0), scale=(1, 1, 1))

# Resize the mold
bpy.data.objects["Plane"].dimensions = [bpy.data.objects[nameObject].dimensions[0], bpy.data.objects[nameObject].dimensions[1], 0]

# Apply transformation of the mold
#bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Select the mesh and the bottom
bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
bpy.data.objects[nameObject].select_set(True)
bpy.data.objects["Plane"].select_set(True)

# Join the mesh and the bottom
bpy.ops.object.join()

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Intersect the bottom with the mesh
bpy.ops.mesh.intersect(mode='SELECT_UNSELECT', separate_mode='NONE', solver='EXACT')

# Deselect all the faces
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_mode(type="VERT")

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

# Get the active object
obj = bpy.context.active_object

for v in obj.data.vertices:
    if (v.co.x < xMax + 0.001 and v.co.x > xMax - 0.001) or (v.co.x < xMin + 0.001 and v.co.x > xMin - 0.001):
        if (v.co.y < yMax + 0.001 and v.co.y > yMax - 0.001) or (v.co.y < yMin + 0.001 and v.co.y > yMin - 0.001):
            v.select = True
            
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Delete the selected vertices
bpy.ops.mesh.delete(type='VERT')

bpy.ops.mesh.select_mode(type="FACE")
