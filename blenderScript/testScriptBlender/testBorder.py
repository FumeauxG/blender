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
    #else:
        #print(v)
        #print(v.link_edges)
        #for linkEdge in v.link_faces:
        #    linkEdge.hide = True
        #v.link_edges.hide = True
        
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
print(loops)

bpy.ops.mesh.reveal(select = False) # unhide all faces

n = 0
for i in range(len(loops[n])):
    print(i)
    print("Salut",loops[n][i])
    bm.edges[loops[n][i]].select = True
   

#bpy.ops.mesh.select_mode(type="FACE")

print("End Script")