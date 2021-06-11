import bpy
import bmesh

print("Start")

obj = bpy.context.active_object
me = bpy.context.edit_object.data#bm = bmesh.from_edit_mesh(me)
bpy.ops.object.editmode_toggle() 

tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(vertex)

#for poly in obj.data.polygons:
#    if poly.select == True:
#        minValue = min(obj.data.vertices[poly.vertices[0]].co.z,obj.data.vertices[poly.vertices[1]].co.z,obj.data.vertices[poly.vertices[2]].co.z)
#        obj.data.vertices[poly.vertices[0]].co.z = minValue
#        obj.data.vertices[poly.vertices[1]].co.z = minValue
#        obj.data.vertices[poly.vertices[2]].co.z = minValue
tabPoly = []
k = 0
for poly in obj.data.polygons:
    print(poly.center[2])
    if poly.select == True:
        k = k+1
        if tabPoly == []:
            tabPoly.append(poly)
        else:
            i = 0
            for poly2 in tabPoly:
                if poly.center[2] > poly2.center[2]:
                    tabPoly.insert(i, poly)
                    break
                i = i + 1
            if i == (len(tabPoly)):
                tabPoly.append(poly)
        #print(tabVertices[poly.vertices[0]].co.z,tabVertices[poly.vertices[1]].co.z,tabVertices[poly.vertices[2]].co.z)
        #minValue = min(tabVertices[poly.vertices[0]].co.z,tabVertices[poly.vertices[1]].co.z,tabVertices[poly.vertices[2]].co.z)
        #print(minValue)
        #obj.data.vertices[poly.vertices[0]].co.z = minValue
        #obj.data.vertices[poly.vertices[1]].co.z = minValue
        #obj.data.vertices[poly.vertices[2]].co.z = minValue
    
for poly in tabPoly: 
    minValue = min(tabVertices[poly.vertices[0]].co.z,tabVertices[poly.vertices[1]].co.z,tabVertices[poly.vertices[2]].co.z)
    print(minValue)
    obj.data.vertices[poly.vertices[0]].co.z = minValue
    obj.data.vertices[poly.vertices[1]].co.z = minValue
    obj.data.vertices[poly.vertices[2]].co.z = minValue
    
print(k, len(tabPoly))   
                 
#for vertex in obj.data.vertices:
#    if vertex.select == True:
#        print(vertex.index)
#        print(vertex.co)
#        vertex.co.z = 0
#        print(vertex.co)

#for vert in me.vertices:
#    if vert.index%2:
#        print(vert.index)
#        new_location = vert.co
#        new_location[0] = new_location[0] + 1   #X
#        new_location[1] = new_location[1] + 1   #Y
#        new_location[2] = new_location[2] + 1   #Z
#        vert.co = new_location
#        print(vert.co)

#bmesh.update_edit_mesh(me)
#import bpy

#obj  = bpy.context.active_object
#mesh = obj.data
#vert = mesh.vertices[0]
#mat_world = obj.matrix_world

#pos_world = mat_world @ vert.co
#pos_world.z += 0.1
#vert.co = mat_world.inverted() @ pos_world
bpy.ops.object.editmode_toggle()
