import bpy
import bmesh

print("Start")

obj = bpy.context.active_object

bpy.ops.mesh.region_to_loop()

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)

tabVert = []
for v in bm.verts:
    if v.select == True:
        tabVert.append(v)
        
tabEdge = []
for e in bm.edges:
    if e.select == True:
        tabEdge.append(e)
    else:
        e.hide = True
        
bmesh.update_edit_mesh(me)
        
# Unselect everything
bpy.ops.mesh.select_all(action="DESELECT")

loops = []
while tabEdge:
    tabEdge[0].select_set(True)                   # select 1st face
    bpy.ops.mesh.select_linked()                # select all linked faces makes a full loop
    loops.append([e.index for e in tabEdge if e.select])
    bpy.ops.mesh.hide(unselected=False)         # hide the detected loop
    tabEdge = [e for e in tabEdge if not e.hide] # update faces
#print(loops)

bpy.ops.mesh.reveal(select = False) # unhide all faces

for i in range(len(loops[0])):
    #print(i)
    #print("Salut",loops[0][i])
    bm.edges[loops[0][i]].select = True
  

#bpy.ops.mesh.select_mode(type="FACE")

#for i in range(len(loops[0])): 
grow_faces = set(v for v in bm.verts if v.select for v in v.link_faces if not v.hide)
for v in grow_faces:
    v.select = True

tabVertices = []
for vertex in obj.data.vertices:
    tabVertices.append(vertex)
    
# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')  

#for poly in obj.data.polygons:
#    if poly.select == True:
#        minValue = min(obj.data.vertices[poly.vertices[0]].co.z,obj.data.vertices[poly.vertices[1]].co.z,obj.data.vertices[poly.vertices[2]].co.z)
#        obj.data.vertices[poly.vertices[0]].co.z = minValue
#        obj.data.vertices[poly.vertices[1]].co.z = minValue
#        obj.data.vertices[poly.vertices[2]].co.z = minValue
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
                if poly.center[2] > poly2.center[2]:
                    tabPoly.insert(i, poly)
                    break
                i = i + 1
            if i == (len(tabPoly)):
                tabPoly.append(poly)
print(k)
                
for poly in tabPoly:
    minValue = min(tabVertices[poly.vertices[0]].co.z,tabVertices[poly.vertices[1]].co.z,tabVertices[poly.vertices[2]].co.z)
    print("SALUT",minValue)
    obj.data.vertices[poly.vertices[0]].co.z = minValue
    obj.data.vertices[poly.vertices[1]].co.z = minValue
    obj.data.vertices[poly.vertices[2]].co.z = minValue
    print(obj.data.vertices[poly.vertices[0]].co.z,obj.data.vertices[poly.vertices[1]].co.z,obj.data.vertices[poly.vertices[2]].co.z)


# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

bpy.ops.mesh.select_mode(type="FACE")  

print("End Script")