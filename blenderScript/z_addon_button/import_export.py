import bpy
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class

name_filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//"

# import class
class STL_FILE_import(Operator, ImportHelper):
    bl_idname = 'stl_file.import_file'
    bl_label = 'Import stl object file'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.stl'
    
    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )
 
    def invoke(self, context, event):
        self.filepath = name_filepath
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

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Deselect all
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        
        return {'FINISHED'}
        
# export class 
class STL_FILE_export(Operator, ExportHelper):
    bl_idname = 'stl_file.export_file'
    bl_label = 'Export stl support file'
    bl_options = {'PRESET', 'UNDO'}
 
    filename_ext = '.stl'
    
    filter_glob: StringProperty(
        default='*.stl',
        options={'HIDDEN'}
    )
    
    def invoke(self, context, event):
        nameSupport = ""
        if bpy.context.active_object != None:
            nameSupport =  bpy.context.active_object.name
        else:
            nameSupport = "support"
          
        self.filepath = name_filepath + nameSupport + ".stl"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        print('Exported file: ', self.filepath)
        
        # Export the stl file
        bpy.ops.export_mesh.stl(filepath = self.filepath)
        
        return {'FINISHED'}