import datetime

import bpy
import mathutils

date_1 = datetime.datetime.now()

pi = 3.14159265
maxAngle = 89
maxAngleRad = maxAngle*pi/180

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')

xLim = obj.dimensions[0]/10
tabArea = []
tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(obj.matrix_world @ vertex.co) 
    for i in range(10):
        if tabVertices[vertex.index] <= ((i*xLim)+xLim):
            tabArea.append(i)
            break
        tabArea.append(i)
        
tabPoly = [[] for _ in range(10)]
for poly in obj.data.polygons:
    tabPoly[tabArea[poly.vertices[0]]].append(poly)

for poly in obj.data.polygons:
    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
    if angle < maxAngleRad:
        poly.select = True
        #print(poly.index)
        
        triangleCenter = (tabVertices[poly.vertices[0]]+tabVertices[poly.vertices[1]]+tabVertices[poly.vertices[2]])/3
                
        #for comparePoly in obj.data.polygons:
        #if  (mathutils.geometry.intersect_ray_tri(tabVertices[comparePoly.vertices[0]], tabVertices[comparePoly.vertices[1]], tabVertices[comparePoly.vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != comparePoly.index):
        #        poly.select = False
        #        break
        #print("TEST")
        #print(tabVertices[tabPoly[tabArea[poly.vertices[0]]][1440].vertices[2]])
        #print(len(tabPoly[tabArea[poly.vertices[0]]]))
        #break
        for i in range(len(tabPoly[tabArea[poly.vertices[0]]])):
            print(i)
            print(len(tabPoly[tabArea[poly.vertices[0]]]))
            if  (mathutils.geometry.intersect_ray_tri(tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[0]], tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[1]], tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != tabPoly[poly.vertices[0]][i].index):
                poly.select = False
                break  

bpy.ops.object.mode_set(mode = 'EDIT')
print("Endscript")

date_2 = datetime.datetime.now()

time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()

print(total_seconds)