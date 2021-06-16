import bpy
import bmesh

print("START")

pi = 3.14159265

obj = bpy.context.active_object

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)

tabVertEdges = set(e for e in bm.edges if e.verts[0].co[0] == e.verts[1].co[0] and e.verts[0].co[1] == e.verts[1].co[1] and e.verts[0].co[2] != e.verts[1].co[2])

#for e in tabVertEdges:
#    print(e.index)
#    e.select = True

#bmesh.update_edit_mesh(me)


loops = []
for e in tabVertEdges:
    # Deselect all
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    print(e.index)
    e.select = True
    bpy.ops.mesh.loop_multi_select(ring = True)
    
    grow_faces = set(e for e in tabVertEdges if e.select for e in e.link_faces)
    
    for f in grow_faces:
        f.select = True
    loops.append([f.index for f in bm.faces if f.select])
    bpy.ops.mesh.hide(unselected=False)         # hide the detected loop
    tabVertEdges = [e for e in tabVertEdges if not e.select] # update faces

bpy.ops.mesh.reveal(select = False) # unhide all faces
bmesh.update_edit_mesh(me)

print(loops)

# Deselect all
bpy.ops.mesh.select_all(action = 'DESELECT')

for i in range(len(loops[0])):
    print(i)
    print("Salut",loops[0][i])
    bm.faces[loops[0][i]].select = True
 
    
bmesh.update_edit_mesh(me) 
    
print("End Script")