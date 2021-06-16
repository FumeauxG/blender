import bpy
import bmesh
import mathutils
import datetime

pi = 3.14159265

date_1 = datetime.datetime.now()
print("Start")

xMax = float('-inf')
xMin = float('inf')

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

obj = bpy.context.active_object

tabSelectedFaces = []

for poly in obj.data.polygons:
    if poly.select == True:
        tabSelectedFaces.append(poly)
        print("TEST")
        #print(obj.matrix_world @ obj.data.vertices[poly.vertices[0]].co)
        #print(obj.data.vertices[poly.vertices[0]].co.x)
        xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
        xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)

        
print(xMax)
print("TEST")
#print(tabSelectedFaces)



# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

#print("End Script")

me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)

#grow_faces = []
k = 0
for poly in obj.data.polygons:
    grow_faces = set(v for v in bm.verts if v.select for v in v.link_faces if (not v.select and not v.hide))
    #print(grow_faces)
    #for v in bm.verts:
     #   if v.select:
    #        for v in v.link_faces:
    #            if not v.select:
    #                grow_faces.append(v)
            
    #bpy.ops.mesh.select_all(action='DESELECT')
    for v in grow_faces:
        v.select = True
        angle = mathutils.Vector(v.normal).angle(mathutils.Vector((0,0,-1)))*180/pi
        print(angle)
    break

    if grow_faces == set():
    #if grow_faces == []:
        #print("Salut")
        break;

    matrix_new = obj.matrix_world.to_3x3().inverted().transposed()

    for v in grow_faces:
        no_world = matrix_new @ v.normal
        no_world.normalize()
        print(no_world)
        if no_world != mathutils.Vector((0,0,0)):
            angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,1)))*180/pi
        else:
            angle = 0
        #if no_world[2]<0.1 and no_world[2]>= 0:
        if angle<179.9 and angle>= 89.9:
            v.select = True
            xMax = max(xMax, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
            xMin = min(xMin, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
            
            #xMax = max(xMax, obj.data.vertices[v.vertices[0]].co.x, obj.data.vertices[v.vertices[1]].co.x, obj.data.vertices[v.vertices[2]].co.x)
            #xMin = min(xMin, obj.data.vertices[v.vertices[0]].co.x, obj.data.vertices[v.vertices[1]].co.x, obj.data.vertices[v.vertices[2]].co.x)
        else:
            v.hide = True
    k = k+1
    print(k)
    #break
 
print(xMax,xMin,xMax-xMin) 
                
bpy.ops.mesh.reveal(select = False) # unhide all faces
bmesh.update_edit_mesh(me)

#print(tabSelectedFaces[0].normal[2])

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

#for poly in obj.data.polygons:
#    if poly.select == True:
#        if poly.normal[2] <0.01:
#            poly.select = False
        
# Switch in object mode 
bpy.ops.object.mode_set(mode='EDIT')

print("End Script")

date_2 = datetime.datetime.now()

time_delta = (date_2 - date_1)
total_seconds = time_delta.total_seconds()

print("Time : ", total_seconds)        