import datetime

import bpy
import mathutils

date_1 = datetime.datetime.now()
print("Start")

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
print("Endscript")

date_2 = datetime.datetime.now()

time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()

print(total_seconds)