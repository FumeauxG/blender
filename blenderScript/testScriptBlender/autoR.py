import bpy
import mathutils

from math import pi
from math import radians

# Switch in the object mode
bpy.ops.object.mode_set(mode = 'OBJECT')

obj = bpy.context.active_object

# Add the vertices location in an array
tabVertices = []
for vertex in obj.data.vertices:
   tabVertices.append(vertex.co)


tabHeight = []
tabArea = []
tabVolume = []
tabRatio = []
for x in range(180):
    x = 179
    bpy.context.active_object.rotation_euler[0] = radians(x)
    # Align the object on the xy plane
    bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
    
    # Apply location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    tabHeight.append(bpy.context.active_object.dimensions[2])
    
    for poly in bpy.context.active_object.data.polygons:
        if poly.normal != mathutils.Vector((0,0,0)):
            angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
        else:
            angle = 0
        area = 0
        volume = 0
        if angle < radians(60):
            print("S",poly.index)
            poly.select
            area = area + poly.area
            volume = volume + (poly.center[2])* mathutils.geometry.area_tri((bpy.context.active_object.matrix_world @ tabVertices[poly.vertices[0]]).to_2d(), (bpy.context.active_object.matrix_world @ tabVertices[poly.vertices[1]]).to_2d(), (bpy.context.active_object.matrix_world @ tabVertices[poly.vertices[2]]).to_2d())
            print(area,volume)
        tabRatio.append(area + volume)
            
    bpy.context.active_object.rotation_euler[0] = radians(-x)
    # Apply location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    

i = 0
for x in range(180):
    if tabRatio[x] < tabRatio[i] and tabHeight[x] < tabHeight[i]:
        i = x

print(tabRatio)
print(tabHeight)
print(i)
bpy.context.active_object.rotation_euler[0] = radians(i)

            
    
    