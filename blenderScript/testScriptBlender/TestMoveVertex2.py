import bpy
import bmesh

print("Start")

obj = bpy.context.active_object
me = bpy.context.edit_object.data#bm = bmesh.from_edit_mesh(me)

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(vertex)

tabPoly = []
k = 0
for poly in obj.data.polygons:
    #print(poly.center[2])
    if poly.select == True:
        k = k+1
        if tabPoly == []:
            tabPoly.append(poly)
        else:
            i = 0
            for poly2 in tabPoly:
                if poly.center[2] < poly2.center[2]:
                    tabPoly.insert(i, poly)
                    break
                i = i + 1
            if i == (len(tabPoly)):
                tabPoly.append(poly)
        
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
        
me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)

# Deselect all
bpy.ops.mesh.select_all(action = 'DESELECT')

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

i = 0    
for poly in tabPoly:
    poly.select = True 
    print(poly.center[2])
    if poly.hide == False:
        minValue = min(tabVertices[poly.vertices[0]].co.z,tabVertices[poly.vertices[1]].co.z,tabVertices[poly.vertices[2]].co.z)
        #print(minValue)
        obj.data.vertices[poly.vertices[0]].co.z = minValue
        obj.data.vertices[poly.vertices[1]].co.z = minValue
        obj.data.vertices[poly.vertices[2]].co.z = minValue
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(me)
        grow_faces = set(v for v in bm.verts if v.select for v in v.link_faces if not v.hide)
        for v in grow_faces:
            i = 1 +i
            #print(v)
            v.hide = True
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        print(i)
        #break

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')  
bpy.ops.mesh.reveal(select = False) # unhide all faces
bmesh.update_edit_mesh(me)  

#print(k, len(tabPoly))   
                 
# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')
