import datetime

import bpy
import mathutils

date_1 = datetime.datetime.now()
print("Start Script")

pi = 3.14159265
maxAngle = 89
maxAngleRad = maxAngle*pi/180

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')

lim = 10
xLim = obj.dimensions[0]/lim
tabArea = []
tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(obj.matrix_world @ vertex.co) 
    for i in range(lim):
        if tabVertices[vertex.index].x <= ((i*xLim)+xLim):
            tabArea.append(i)
            break
        
tabPoly = [[] for _ in range(lim)]
for poly in obj.data.polygons:
    tabPoly[tabArea[poly.vertices[0]]].append(poly)

for poly in tabPoly[0]:
    poly.select = True

#for poly in obj.data.polygons:
#    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
##    if angle < maxAngleRad:
#        poly.select = True
        #print(poly.index)
        
#        triangleCenter = (tabVertices[poly.vertices[0]]+tabVertices[poly.vertices[1]]+tabVertices[poly.vertices[2]])/3
#        for i in range(len(tabPoly[tabArea[poly.vertices[0]]])):
#            if  (mathutils.geometry.intersect_ray_tri(tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[0]], tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[1]], tabVertices[tabPoly[tabArea[poly.vertices[0]]][i].vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != tabPoly[tabArea[poly.vertices[0]]][i].index):
#                poly.select = False
#                break 
            #tabVertices[tabPoly[tabArea[poly.vertices[1]]][i].vertices[0]]
       # if tabArea[poly.vertices[0]] != tabArea[poly.vertices[1]]:
       #     print("+")
       #     for i in range(len(tabPoly[tabArea[poly.vertices[1]]])):
       #         if  (mathutils.geometry.intersect_ray_tri(tabVertices[tabPoly[tabArea[poly.vertices[1]]][i].vertices[0]], tabVertices[tabPoly[tabArea[poly.vertices[1]]][i].vertices[1]], tabVertices[tabPoly[tabArea[poly.vertices[1]]][i].vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != tabPoly[tabArea[poly.vertices[1]]][i].index):
       #             poly.select = False
       #             break
       # if (tabArea[poly.vertices[0]] != tabArea[poly.vertices[2]]) and (tabArea[poly.vertices[1]] != tabArea[poly.vertices[2]]): 
       #     for i in range(len(tabPoly[tabArea[poly.vertices[2]]])):
       #         if  (mathutils.geometry.intersect_ray_tri(tabVertices[tabPoly[tabArea[poly.vertices[2]]][i].vertices[0]], tabVertices[tabPoly[tabArea[poly.vertices[2]]][i].vertices[1]], tabVertices[tabPoly[tabArea[poly.vertices[2]]][i].vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != tabPoly[tabArea[poly.vertices[2]]][i].index):
       #             poly.select = False
       #             break
                
bpy.ops.object.mode_set(mode = 'EDIT')
print("Endscript")

date_2 = datetime.datetime.now()

time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()

print(total_seconds)