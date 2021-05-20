###########################
# Test automatized Blender
# Author : Fumeaux Gaëtan
# v1.0 (semi-auto)
###########################
# Conditions to start :
# Part a :
# - One object selected
# - Pres ctrl + shift + F to start
###########################


import glob
import bpy

# The script
def myFunction():
    # Delete the existing cube or support
    object_to_delete = bpy.context.selected_objects[0]
    bpy.data.objects.remove(object_to_delete, do_unlink=True)

    # Find the stl files
    txtfiles = []
    for file in glob.glob("C:/Gaetan/_Bachelor/blender/blenderScript/test/*.stl"):
        txtfiles.append(file)
    # Choose the first stl file
    pathIn = txtfiles[0]
    print(txtfiles[0])

    # out file
    pathTemp = pathIn.split('.')
    pathOut = pathTemp[0] + '_support.' + pathTemp[1]

    # Find the name of the object
    nameTemp = pathIn.split("\\")
    print(nameTemp[1])
    nameObject = nameTemp[1].split(".")
    print(nameObject[0])

    # Import the stl file
    bpy.ops.import_mesh.stl(filepath=pathIn)

    # Rename the base object
    bpy.context.selected_objects[0].name = nameObject[0]

    # Align the object on the xy plane
    bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})

    # Switch in the edit mode
    bpy.ops.object.editmode_toggle()

    # Deselect all
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.mesh.select_mode(type="FACE")

    print("Make Selection")
    
#########################################
# Blender keypad integration
#########################################
bl_info = {
    "name": "zeBlenderTestKeypad2a",
    "description": "Test automatized Blender semi-auto part a",
    "author": "Fumeaux Gaëtan",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "category": "Object",
}

class WorkMacro(bpy.types.Operator):
    """Work Macro"""
    bl_idname = "object.semi_auto_part_a"
    bl_label = "Semi-auto support part a"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        print("Start semi-auto support part a") 
        myFunction()
        return {'FINISHED'}


# store keymaps here to access after registration
addon_keymaps = []


def register():
    bpy.utils.register_class(WorkMacro)

    # handle the keymap
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new(WorkMacro.bl_idname, 'F', 'PRESS', ctrl=True, shift=True)
    addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(WorkMacro)

    # handle the keymap
    wm = bpy.context.window_manager
    for km in addon_keymaps:
        wm.keyconfigs.addon.keymaps.remove(km)
    # clear the list
    del addon_keymaps[:]


if __name__ == "__main__":
    register()