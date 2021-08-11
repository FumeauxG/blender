import bpy
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class

name_filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//"
'''string: default filename where the import and export function are going to point
'''

class STL_FILE_import(Operator, ImportHelper):
    '''
    Class that opens a file explorer to import stl file
    '''
    bl_idname = 'stl_file.import_file'
    bl_label = 'Import stl object file'
    bl_options = {'PRESET', 'UNDO'}
 
    # Type of the file
    filename_ext = '.stl'
    
    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )
 
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'} 
 
    def execute(self, context):
        print('Imported file: ', self.filepath)
        
        # Import the stl file
        bpy.ops.import_mesh.stl(filepath = self.filepath)
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})
    
        # Apply location
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # init properties of angles and offset
        bpy.context.scene.angle_x = 0
        bpy.context.scene.angle_y = 0
        bpy.context.scene.angle_z = 0
        bpy.context.scene.offset = 0 

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Deselect all the faces
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        
        return {'FINISHED'}
        
class STL_FILE_export(Operator, ExportHelper):
    '''
    Class that opens a file explorer to export stl file
    '''
    bl_idname = 'stl_file.export_file'
    bl_label = 'Export stl support file'
    bl_options = {'PRESET', 'UNDO'}
 
    # Type of the file
    filename_ext = '.stl'
    
    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )
    
    def invoke(self, context, event):
        # Default name of the file is the name of the mesh if a mesh is selected
        nameSupport = ""
        if bpy.context.active_object != None:
            nameSupport =  bpy.context.active_object.name
        else:
            nameSupport = "support"
        
        # Set the filepath
        self.filepath = nameSupport + ".stl"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        print('Exported file: ', self.filepath)
        
        # Export the stl file
        bpy.ops.export_mesh.stl(filepath = self.filepath)
        
        return {'FINISHED'}