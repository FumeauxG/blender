import bpy

obj = bpy.context.active_object

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')

# Make a copy of the object
new_obj = obj.copy()
new_obj.data = obj.data.copy()
new_obj.animation_data_clear()
bpy.context.collection.objects.link(new_obj)

# Rename the copy
new_obj.name = "temp_copy"

# Hide the copy
new_obj.hide_viewport = True


# Remesh the faces of the object with blocks
bpy.ops.object.modifier_add(type='REMESH')
bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
bpy.context.object.modifiers["Remesh"].octree_depth = 5
bpy.context.object.modifiers["Remesh"].scale = 0.99
bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
bpy.context.object.modifiers["Remesh"].threshold = 1
bpy.context.object.modifiers["Remesh"].use_smooth_shade = False

# Make intersection between the remesh object and the original
bpy.ops.object.modifier_add(type='BOOLEAN')
bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
bpy.context.object.modifiers["Boolean"].object = bpy.data.objects["temp_copy"]
bpy.context.object.modifiers["Boolean"].solver = 'FAST'
bpy.context.object.modifiers["Boolean"].double_threshold = 0


#bpy.ops.object.apply_all_modifiers()
