###########################
# Test automatized Blender
# Author : Fumeaux Gaëtan
# v1.0 (semi-auto)
###########################
# Conditions to start :
# Part a :
# - One object selected
###########################


import glob
import bpy

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