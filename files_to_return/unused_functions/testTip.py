import bpy
import bmesh

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Select all faces
bpy.ops.mesh.select_all(action='SELECT')

bpy.ops.mesh.tris_convert_to_quads()

# Split all connected faces
bpy.ops.mesh.edge_split(type='EDGE')

bpy.ops.mesh.select_all(action='DESELECT')

# Load mesh
me = bpy.context.edit_object.data
bm = bmesh.from_edit_mesh(me)
# Ensure internal data needed for int subscription is initialized
bm.faces.ensure_lookup_table()

# Resize all faces
for f in bm.faces:
    f.select_set(True) 
    bpy.ops.transform.resize(value=(0.2, 0.2, 0.2), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    f.select_set(False)
    