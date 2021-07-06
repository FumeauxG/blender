bl_info = {
    "name": "Button Controller",
    "description": "Button Controller",
    "author": "Fumeaux Gaëtan",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "category": "Object",
}

# To support reload properly, try to access a package var, 
# if it's there, reload everything
if "bpy" in locals():
  import importlib
  importlib.reload(getter_and_setter)
  importlib.reload(import_export)
  #imp.reload(mycylinder)
  print("Reloaded multifiles")
else:
  from .getter_and_setter import *
  from .operations import *
  from .import_export import *
  print("Imported multifiles")

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
import mathutils
import bmesh

from math import pi
from math import radians
from math import sqrt

import datetime
import ctypes
import glob
import os

# For import export
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class


name_filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//"

class BUTTON_PT_import_export(Panel):
    bl_idname = 'BUTTON_PT_import_export'
    bl_label = 'Import/Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        
        layout.operator('btn.btn_op', text='m to mm').action = 'M_TO_MM'
        
        layout.separator()
        
        layout.label(text="Beta import/export")
        
        layout.operator('btn.btn_op', text='Import Object').action = 'IMPORT_OBJECT'
        layout.operator('btn.btn_op', text='Export Object').action = 'EXPORT_OBJECT' 

        if len(bpy.context.selected_objects) != 0:
            layout.label(text= ("Number of faces : " + str(len(bpy.context.active_object.data.polygons))))
            layout.label(text= ("Size of the stl file : ~" + str(int(len(bpy.context.active_object.data.polygons)/20.4)) + " Ko"))           
 
class BUTTON_PT_rotation(Panel):
    bl_idname = 'BUTTON_PT_rotation'
    bl_label = 'Rotation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "angle_x")  
        row.prop(scene, "angle_y")
        row.prop(scene, "angle_z")                
        
class BUTTON_PT_generation(Panel):
    bl_idname = 'BUTTON_PT_generation'
    bl_label = 'Generation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "max_angle")
        
        layout.operator('btn.btn_op', text='Import object old').action = 'IMPORT'
        #layout.operator('btn.btn_op', text='Select faces').action = 'SELECT'
        layout.operator('btn.btn_op', text='Select faces fast').action = 'SELECT_FAST'
        layout.operator('btn.btn_op', text='Generate support').action = 'GENERATE'
        
class BUTTON_PT_area(Panel):
    bl_idname = 'BUTTON_PT_area'
    bl_label = 'Area'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
    
        layout.label(text="Beta area")
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "min_area")
        
        layout.operator('btn.btn_op', text='Generate support (area)').action = 'GENERATE_AREA'
        
        layout.operator('btn.btn_op', text='Separate faces').action = 'SEPARATE'
        layout.operator('btn.btn_op', text='Select faces 2').action = 'SELECT2'
        
class BUTTON_PT_offset(Panel):
    bl_idname = 'BUTTON_PT_offset'
    bl_label = 'Offset'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
    
        layout.label(text="Beta offset")
        
        box = layout.box()
        row = box.row()
        row.prop(context.object, "offset")
        layout.operator('btn.btn_op', text='Offset').action = 'OFFSET'
        
        layout.separator()
        
        layout.operator('btn.btn_op', text='Mold1').action = 'MOLD1'
        
class BUTTON_PT_resize(Panel):
    bl_idname = 'BUTTON_PT_resize'
    bl_label = 'Resize'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout 
        scene = context.scene 
        
        layout.label(text="Beta resize")

        layout.operator('btn.btn_op', text='Select resize').action = 'SELECT_RESIZE'
        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "min_angle_z")  
        row.prop(scene, "max_angle_z")  
        layout.operator('btn.btn_op', text='Select resize all').action = 'SELECT_RESIZE_ALL'        

        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "resize")  
        layout.operator('btn.btn_op', text='Resize').action = 'RESIZE' 
        
        layout.separator()
        
        layout.operator('btn.btn_op', text='Delete selection').action = 'DELETE_SELECTION' 
        layout.operator('btn.btn_op', text='Fill').action = 'FILL' 

class BUTTON_PT_lattice(Panel):
    bl_idname = 'BUTTON_PT_lattice'
    bl_label = 'Lattice'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout 
        scene = context.scene 
        
        layout.label(text="Beta lattice")

        layout.operator('btn.btn_op', text='Add lattice').action = 'ADD_LATTICE'
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "lattice_size_x")  
        row.prop(scene, "lattice_size_y")
        row.prop(scene, "lattice_size_z")  
        
        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "lattice_offset_x")  
        row.prop(scene, "lattice_offset_y")
        row.prop(scene, "lattice_offset_z") 
        
        layout.operator('btn.btn_op', text='Select lattice').action = 'SELECT_LATTICE'
        layout.operator('btn.btn_op', text='Delete lattice').action = 'DELETE_LATTICE'
        
class BUTTON_PT_voxel(Panel):
    bl_idname = 'BUTTON_PT_voxel'
    bl_label = 'Voxel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        
        layout.label(text="Beta voxel")
        
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "voxel_size")
        layout.operator('btn.btn_op', text='Add Voxel').action = 'VOXEL'
        layout.operator('btn.btn_op', text='Validate').action = 'VALIDATE'
        
        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "decimate_ratio")
        layout.operator('btn.btn_op', text='Add Decimate').action = 'DECIMATE'
        layout.operator('btn.btn_op', text='Validate').action = 'VALIDATE'
        
        layout.separator()
        
        layout.operator('btn.btn_op', text='Manifold').action = 'MANIFOLD'
        layout.operator('btn.btn_op', text='Volume').action = 'VOLUME'
              
        layout.label(text= ("Volume : " + '{:.2f}'.format(bpy.context.scene.volume) + " mm³"))
        
        box3 = layout.box()
        row = box3.row()
        row.prop(scene, "level_blocks")
        layout.operator('btn.btn_op', text='Remesh Blocks').action = 'REMESH_BLOCKS'
        layout.operator('btn.btn_op', text='Validate Blocks').action = 'VALIDATE_BLOCKS'
           
class BUTTON_PT_measure(Panel):
    bl_idname = 'BUTTON_PT_measure'
    bl_label = 'Measure'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
        
        layout.operator('btn.btn_op', text='Measure distance').action = 'MEASURE_DISTANCE'
        layout.label(text= ("X : " + '{:.2f}'.format(bpy.context.scene.distance[0]) + " mm"))
        layout.label(text= ("Y : " + '{:.2f}'.format(bpy.context.scene.distance[1]) + " mm"))
        layout.label(text= ("Z : " + '{:.2f}'.format(bpy.context.scene.distance[2]) + " mm"))
        layout.label(text= ("Distance : " + '{:.2f}'.format(bpy.context.scene.distance[3]) + " mm"))
        
class BUTTON_OT_button_op(Operator):
    bl_idname = 'btn.btn_op'
    bl_label = 'Button'
    bl_description = 'Button'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('M_TO_MM', 'm to mm', 'm to mm'),
            ('IMPORT_OBJECT', 'Import Object', 'Import Object'),
            ('EXPORT_OBJECT', 'Export Object', 'Export Object'),
            
            ('IMPORT', 'Import object old', 'Import object old'),
            ('SELECT_FAST', 'Select faces fast', 'Select faces fast'),
            ('GENERATE', 'Generate support', 'Generate support'),
            
            ('GENERATE_AREA', 'Generate support (area)', 'Generate support (area)'),
            ('SEPARATE', 'Separate faces', 'Separate faces)'),
            ('SELECT2', 'Select faces 2', 'Select faces 2'),
            
            ('OFFSET', 'Offset', 'Offset'),
            ('MOLD1', 'Mold1', 'Mold1'),
            ('MOLD2', 'Mold2', 'Mold2'),
            
            ('SELECT_RESIZE', 'Select resize', 'Select resize'),
            ('SELECT_RESIZE_ALL', 'Select resize all', 'Select resize all'),
            ('RESIZE', 'Resize', 'Resize'),
            ('DELETE_SELECTION', 'Delete selection', 'Delete selection'),
            ('FILL', 'Fill', 'Fill'),
            
            ('ADD_LATTICE', 'Add lattice', 'Add lattice'),
            ('SELECT_LATTICE', 'Select lattice', 'Select lattice'),
            ('DELETE_LATTICE', 'Delete lattice', 'Delete lattice'),
            
            ('VOXEL', 'Voxel', 'Voxel'),
            ('DECIMATE', 'Decimate', 'Decimate'),
            ('VALIDATE', 'Validate', 'Validate'),
            ('MANIFOLD', 'Manifold', 'Manifold'),
            ('VOLUME', 'Volume', 'Volume'),
            ('REMESH_BLOCKS', 'Remesh Blocks', 'Remesh Blocks'),
            ('VALIDATE_BLOCKS', 'Validate Blocks', 'Validate Blocks'),
            
            ('MEASURE_DISTANCE', 'Measure distance', 'Measure distance'),
                       
        ]
    )
 
    def execute(self, context):
        if self.action == 'M_TO_MM':   
            self.m_to_mm(context=context)
        elif self.action == 'IMPORT_OBJECT':   
            self.import_object(context=context)
        elif self.action == 'EXPORT_OBJECT':   
            self.export_object(context=context)
            
        elif self.action == 'IMPORT':
            self.import_object_old(context=context)
        elif self.action == 'SELECT_FAST':   
            self.select_faces_fast(context=context) 
        elif self.action == 'GENERATE':   
            self.generate_support(context=context)
            
        elif self.action == 'GENERATE_AREA':   
            self.generate_support_area(context=context)
        elif self.action == 'SEPARATE':   
            self.separate_faces(context=context)
        elif self.action == 'SELECT2':   
            self.select_faces_2(context=context)  
            
        elif self.action == 'OFFSET':   
            self.offset(context=context) 
        elif self.action == 'MOLD1':   
            self.mold1(context=context)
            
        elif self.action == 'SELECT_RESIZE':   
            self.select_resize(context=context) 
        elif self.action == 'SELECT_RESIZE_ALL':   
            self.select_resize_all(context=context) 
        elif self.action == 'RESIZE':   
            self.resize(context=context) 
        elif self.action == 'DELETE_SELECTION':   
            self.delete_selection(context=context) 
        elif self.action == 'FILL':   
            self.fill(context=context)

        elif self.action == 'ADD_LATTICE':   
            self.add_lattice(context=context)  
        elif self.action == 'SELECT_LATTICE':   
            self.select_lattice(context=context)   
        elif self.action == 'DELETE_LATTICE':   
            self.delete_lattice(context=context)    
            
        elif self.action == 'VOXEL':   
            self.voxel(context=context)
        elif self.action == 'DECIMATE':   
            self.decimate(context=context)
        elif self.action == 'VALIDATE':   
            self.validate(context=context)
        elif self.action == 'MANIFOLD':   
            self.manifold(context=context)
        elif self.action == 'VOLUME':   
            self.volume(context=context)
        elif self.action == 'REMESH_BLOCKS':   
            self.remesh_blocks(context=context)
        elif self.action == 'VALIDATE_BLOCKS':   
            self.validate_blocks(context=context) 

        elif self.action == 'MEASURE_DISTANCE':   
            self.measure_distance(context=context)             
            
        return {'FINISHED'}

    @staticmethod
    def m_to_mm(context):          
        # Set blender unit in mm
        bpy.context.scene.unit_settings.scale_length = 0.001
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
        
    @staticmethod
    def import_object(context):   
        bpy.ops.stl_file.import_file('INVOKE_DEFAULT')         
        
    @staticmethod
    def export_object(context):
        bpy.ops.stl_file.export_file('INVOKE_DEFAULT')
          
    @staticmethod
    def import_object_old(context):
        # init properties of angles
        bpy.context.scene.angle_x = 0
        bpy.context.scene.angle_y = 0
        bpy.context.scene.angle_z = 0
    
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Delete the existing cube or support
        object_to_delete = bpy.context.selected_objects[0]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)
        
        # Find the stl files
        txtfiles = []
        #for file in glob.glob("C:/Gaetan/_Bachelor/blender/blenderScript/test/*.stl"):
        for file in glob.glob(name_filepath + "*.stl"):
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

        print("Make Selection")

    @staticmethod
    def select_faces_fast(context): 
        Button_Operations.select_faces(bpy.context.scene.max_angle)
   
    @staticmethod
    def generate_support(context):
        Button_Operations.generate_support()
        Button_Operations.manifold_and_triangulate()

    @staticmethod
    def generate_support_area(context):
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.active_object
        
        # Get the name of the object
        nameObject = obj.name

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Set support as active pbject
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]

        # Delete the base object
        object_to_delete = bpy.data.objects[nameObject]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # Load mesh
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()

        loops = []
        faces = bm.faces

        while faces:
            faces[0].select_set(True)                   # select 1st face
            bpy.ops.mesh.select_linked()                # select all linked faces makes a full loop
            loops.append([f.index for f in faces if f.select])
            bpy.ops.mesh.hide(unselected=False)         # hide the detected loop
            faces = [f for f in bm.faces if not f.hide] # update faces

        bpy.ops.mesh.reveal() # unhide all faces
        print("Mesh has {} parts".format(len(loops)))

        print("\nThe face lists are:")
        for loop in loops:
            print(loop)

        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='OBJECT')

        area = 0 
        for rows in range(len(loops)):
            area = 0
            for columns in loops[rows]:
                area = area + bpy.context.active_object.data.polygons[columns].area
            print(rows)
            print(area)
            if area > bpy.context.scene.min_area:
                for columns in loops[rows]:
                    bpy.context.active_object.data.polygons[columns].select = True

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Set final support as active object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".002"]

        # Delete the temp support
        object_to_delete = bpy.data.objects[nameObject + ".001"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Create new edit mode bmesh to easily acces mesh data
        mesh = bpy.context.object.data  # Get selected object's mesh
        bm = bmesh.from_edit_mesh(mesh) 

        # Select all vertices that have 1 or 2 links and deselect the others
        for v in bm.verts:
            v.select_set(len(v.link_edges) in (1,2))

        bmesh.update_edit_mesh(mesh)  # Transfer the data back to the object's mesh
        
        # Delete the selected vertices
        bpy.ops.mesh.delete(type='VERT')
        
        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rename the support
        bpy.context.active_object.name = nameObject + "_support"

        print("End Script")

    @staticmethod
    def separate_faces(context):
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
    
        obj = bpy.context.active_object
        
        # Get the name of the object
        nameObject = obj.name

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Set support as active object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]

        # Delete the base object
        object_to_delete = bpy.data.objects[nameObject]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Recover the name
        bpy.context.active_object.name = nameObject

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")
 
    @staticmethod
    def select_faces_2(context): 
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")
        
        # Load mesh
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        bm.faces.ensure_lookup_table()

        loops = []
        faces = bm.faces

        while faces:
            faces[0].select_set(True)                   # select 1st face
            bpy.ops.mesh.select_linked()                # select all linked faces makes a full loop
            loops.append([f.index for f in faces if f.select])
            bpy.ops.mesh.hide(unselected=False)         # hide the detected loop
            faces = [f for f in bm.faces if not f.hide] # update faces

        bpy.ops.mesh.reveal() # unhide all faces
        print("Mesh has {} parts".format(len(loops)))

        print("\nThe face lists are:")
        for loop in loops:
            print(loop)
            
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        area = 0 
        for rows in range(len(loops)):
            area = 0
            for columns in loops[rows]:
                area = area + bpy.context.active_object.data.polygons[columns].area
            print(rows)
            print(area)
            print(bpy.context.scene.min_area)
            if area > bpy.context.scene.min_area:
                for columns in loops[rows]:
                    bpy.context.active_object.data.polygons[columns].select = True

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
   
    @staticmethod
    def offset(context): 
        obj = bpy.context.active_object
        bpy.context.active_object.offset
        
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
    
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'}) 
    
        offsetZ = obj.location[2]
        
        obj.location[2] = offsetZ + obj.offset
        
        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

    @staticmethod
    def mold1(context): 
        date_x = datetime.datetime.now()

        obj = bpy.context.active_object
        moldOffset = obj.offset
    
        nameCopy = "temp_copy"

        nameObject = bpy.context.active_object.name
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Make a copy of the object
        new_obj = bpy.context.active_object.copy()
        new_obj.data = bpy.context.active_object.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)

        # Rename the copy
        new_obj.name = nameCopy

        # Show the copy
        new_obj.hide_viewport = True
        new_obj.hide_viewport = False

        # Select the copy
        bpy.data.objects[nameObject].select_set(False)
        bpy.data.objects[nameCopy].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[nameCopy]

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the base object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
        bpy.data.objects[nameCopy + ".001"].select_set(False)
        bpy.data.objects[nameObject].select_set(True)
        
        # Delete the copy
        object_to_delete = bpy.data.objects[nameCopy]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)
        
        # Make an other copy of the object
        new_obj = bpy.context.active_object.copy()
        new_obj.data = bpy.context.active_object.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)

        # Rename the copy
        new_obj.name = nameCopy

        # Show the copy
        new_obj.hide_viewport = True
        new_obj.hide_viewport = False

        # Select the copy
        bpy.data.objects[nameObject].select_set(False)
        bpy.data.objects[nameCopy].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[nameCopy]

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Cut the faces above the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=False, clear_outer=True, xstart=60, xend=424, ystart=126, yend=224, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Select faces below 89°
        Button_Operations.select_faces(radians(89))

        # Extrude the selected faces to the high 
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 10), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add the mold
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0),rotation=(3.14159, 0, 0), scale=(1, 1, 1))

        # Resize the mold
        bpy.data.objects["Plane"].dimensions = [bpy.data.objects[nameObject].dimensions[0], bpy.data.objects[nameObject].dimensions[1], 0]

        # Align the mold in Z
        bpy.ops.object.align(align_mode='OPT_3', relative_to='OPT_1', align_axis={'Z'})

        # Select the object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
        bpy.data.objects[nameObject].select_set(True)

        # Align the mold in x and y
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

        # Margins x and y
        bpy.data.objects["Plane"].dimensions = [bpy.data.objects[nameObject].dimensions[0]+0.3, bpy.data.objects[nameObject].dimensions[1]+0.3, 0]

        # Apply transformation of the mold
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Select the copy and the mold
        bpy.context.view_layer.objects.active = bpy.data.objects[nameCopy]
        bpy.data.objects[nameCopy].select_set(True)
        bpy.data.objects[nameObject].select_set(False)

        # Join the outline and the mold
        bpy.ops.object.join()

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Cut the intersected faces
        bpy.ops.mesh.intersect(mode='SELECT', separate_mode='NONE')

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Only keep the faces on the plane xy
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=True, xstart=1273, xend=2086, ystart=286, yend=287, flip=False)

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Triangulate all the faces
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')

        # Select the object and the mold
        bpy.data.objects[nameObject].select_set(True)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Join the object and the mold
        bpy.ops.object.join()

        # Recover the name
        obj = bpy.context.active_object
        obj.name = nameObject
        
        # Select faces
        Button_Operations.select_faces(radians(10))

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the support object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]
        bpy.data.objects[nameObject + ".001"].select_set(True)
        bpy.data.objects[nameCopy + ".001"].select_set(True)
        bpy.data.objects[nameObject].select_set(False)
        
        # Delete the copy
        object_to_delete = bpy.data.objects[nameObject]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)
        
        # Join the outline and the mold
        bpy.ops.object.join()
        
        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Create new edit mode bmesh to easily acces mesh data
        mesh = bpy.context.object.data  # Get selected object's mesh
        bm = bmesh.from_edit_mesh(mesh) 

        # Select all vertices that have 1 or 2 links and deselect the others
        for v in bm.verts:
            v.select_set(len(v.link_edges) in (1,2))

        bmesh.update_edit_mesh(mesh)  # Transfer the data back to the object's mesh
        
        # Delete the selected vertices
        bpy.ops.mesh.delete(type='VERT')

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        #bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
        bpy.ops.mesh.bisect(plane_co=(0, 0, moldOffset), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Add the bottom
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, moldOffset-0.2), scale=(1,1,1))
        bpy.data.objects["Cube"].dimensions = [bpy.data.objects[nameObject + ".001"].dimensions[0], bpy.data.objects[nameObject + ".001"].dimensions[1], 0.4]

        # Select the copy
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]
        bpy.data.objects[nameObject + ".001"].select_set(True)

        # Align the mold in x and y
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

        bpy.ops.object.join()

        date_y = datetime.datetime.now()
        time_delta = (date_y - date_x)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)

        print("End Script")
              
    @staticmethod
    def select_resize(context):
        date_1 = datetime.datetime.now()
        print("Start")

        xMax = float('-inf')
        xMin = float('inf')
        
        obj = bpy.context.active_object
        matrix_new = obj.matrix_world.to_3x3().inverted().transposed()

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        tabSelectedFaces = []

        for poly in obj.data.polygons:
            if poly.select == True:
                tabSelectedFaces.append(poly)
                xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)

        k = 0
        for poly in obj.data.polygons:
            grow_faces = set(v for v in bm.verts if v.select for v in v.link_faces if (not v.select and not v.hide))

            if grow_faces == set():
                break;

            for v in grow_faces:
                no_world = matrix_new @ v.normal
                no_world.normalize()
                print(no_world)
                if no_world != mathutils.Vector((0,0,0)):
                    angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))
                else:
                    angle = 0
            
                if angle < bpy.context.scene.max_angle_z and angle >  bpy.context.scene.min_angle_z:
                    v.select = True
                    xMax = max(xMax, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
                    xMin = min(xMin, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
                else:
                    v.hide = True
            k = k+1
            print(k)
         
        print(xMax,xMin,xMax-xMin) 
        
        #global sizeX
        #sizeX = xMax-xMin
        bpy.context.scene.size = xMax-xMin
        #global oldResize
        #oldResize = 1
        bpy.context.scene.oldResize = 1
                        
        bpy.ops.mesh.reveal(select = False) # unhide all faces
        bmesh.update_edit_mesh(me)

        print("End Script")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print("Time : ", total_seconds)        

    @staticmethod
    def select_resize_all(context):
        date_1 = datetime.datetime.now()
        print("Start")

        xMax = float('-inf')
        xMin = float('inf')
        
        obj = bpy.context.active_object

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        tabSelectedFaces = []

        for poly in obj.data.polygons:
            if poly.select == True:
                tabSelectedFaces.append(poly)
                xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)

        k = 0
        for poly in obj.data.polygons:
            grow_faces = set(v for v in bm.verts if v.select for v in v.link_faces if not v.select)

            if grow_faces == set():
                break;

            for v in grow_faces:
                v.select = True
                xMax = max(xMax, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
                xMin = min(xMin, v.verts[0].co.x, v.verts[1].co.x, v.verts[2].co.x)
                
            k = k+1
            print(k)
         
        print(xMax,xMin,xMax-xMin) 
        
        #global sizeX
        #sizeX = xMax-xMin
        bpy.context.scene.size = xMax-xMin
        #global oldResize
        #oldResize = 1
        bpy.context.scene.oldResize = 1
                        
        bmesh.update_edit_mesh(me)

        print("End Script")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print("Time : ", total_seconds)
        
    @staticmethod
    def resize(context):
        #global sizeX
        #global oldResize
        #print(sizeX)
        #print(oldResize)
        #scaleX = 1/oldResize
        scaleX = 1/bpy.context.scene.oldResize
        bpy.ops.transform.resize(value=(scaleX, scaleX, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

        #scaleX = 1+(2*bpy.context.scene.resize/sizeX)
        scaleX = 1+(2*bpy.context.scene.resize/bpy.context.scene.size)
        if scaleX < 0:
            scaleX = 1
        print(scaleX)
        #oldResize = scaleX
        bpy.context.scene.oldResize = scaleX
        bpy.ops.transform.resize(value=(scaleX, scaleX, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

    @staticmethod
    def delete_selection(context):
        print("START")

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for obj in bpy.context.selected_objects:
            if obj.name != bpy.context.view_layer.objects.active.name:
                # Delete the existing copy
                object_to_delete = obj
                bpy.data.objects.remove(object_to_delete, do_unlink=True) 

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
                
        print("End Script")

    @staticmethod
    def fill(context):
        bpy.ops.mesh.fill()  

    @staticmethod
    def add_lattice(context):
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT') 
    
        obj = bpy.context.active_object
        
        flagLattice = False
        for o in bpy.data.objects:
            if o.type == 'LATTICE':
                flagLattice = True
                
        if flagLattice == False:
            nameObject = obj.name
            bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            # Select the object
            bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
            bpy.data.objects[nameObject].select_set(True)
            bpy.data.objects["Lattice"].select_set(False)
            

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')

        tabVertices = []
        for vertex in obj.data.vertices:
            tabVertices.append(obj.matrix_world @ vertex.co)
            if xPlus < (obj.matrix_world @ vertex.co).x:
                xPlus = (obj.matrix_world @ vertex.co).x
            elif xMoins > (obj.matrix_world @ vertex.co).x:
                xMoins = (obj.matrix_world @ vertex.co).x
                
            if yPlus < (obj.matrix_world @ vertex.co).y:
                yPlus = (obj.matrix_world @ vertex.co).y
            elif yMoins > (obj.matrix_world @ vertex.co).y:
                yMoins = (obj.matrix_world @ vertex.co).y
                
            if zPlus < (obj.matrix_world @ vertex.co).z:
                zPlus = (obj.matrix_world @ vertex.co).z
            elif zMoins > (obj.matrix_world @ vertex.co).z:
                zMoins = (obj.matrix_world @ vertex.co).z

        bpy.data.objects["Lattice"].scale = (obj.dimensions[0], obj.dimensions[1], obj.dimensions[2])
        bpy.data.objects["Lattice"].location = ((xPlus+xMoins)/2, (yPlus+yMoins)/2,(zPlus+zMoins)/2)

        bpy.types.Scene.lattice_size_x = bpy.props.FloatProperty(name = "Size X", min = 0, max = 2*obj.dimensions[0], soft_min = 0, soft_max = 2*obj.dimensions[0], step = 10, get=Get_And_Set_Lattice.get_lattice_size_x, set=Get_And_Set_Lattice.set_lattice_size_x, unit = 'LENGTH')
        bpy.types.Scene.lattice_size_y = bpy.props.FloatProperty(name = "Size Y", min = 0, max = 2*obj.dimensions[1], soft_min = 0, soft_max = 2*obj.dimensions[1], step = 10, get=Get_And_Set_Lattice.get_lattice_size_y, set=Get_And_Set_Lattice.set_lattice_size_y, unit = 'LENGTH')
        bpy.types.Scene.lattice_size_z = bpy.props.FloatProperty(name = "Size Z", min = 0, max = 2*obj.dimensions[2], soft_min = 0, soft_max = 2*obj.dimensions[2], step = 10, get=Get_And_Set_Lattice.get_lattice_size_z, set=Get_And_Set_Lattice.set_lattice_size_z, unit = 'LENGTH')
        
        bpy.context.scene.lattice_size_x = obj.dimensions[0]
        bpy.context.scene.lattice_size_y = obj.dimensions[1]
        bpy.context.scene.lattice_size_z = obj.dimensions[2]
        
        bpy.types.Scene.lattice_offset_x = bpy.props.FloatProperty(name = "Size X", min = -obj.dimensions[0], max = obj.dimensions[0], soft_min = -obj.dimensions[0], soft_max = obj.dimensions[0], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_x, set=Get_And_Set_Lattice.set_lattice_offset_x, unit = 'LENGTH')
        bpy.types.Scene.lattice_offset_y = bpy.props.FloatProperty(name = "Size Y", min = -obj.dimensions[1], max = obj.dimensions[1], soft_min = -obj.dimensions[1], soft_max = obj.dimensions[1], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_y, set=Get_And_Set_Lattice.set_lattice_offset_y, unit = 'LENGTH')
        bpy.types.Scene.lattice_offset_z = bpy.props.FloatProperty(name = "Size Z", min = -obj.dimensions[2], max = obj.dimensions[2], soft_min = -obj.dimensions[2], soft_max = obj.dimensions[2], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_z, set=Get_And_Set_Lattice.set_lattice_offset_z, unit = 'LENGTH')
        
        bpy.context.scene.lattice_offset_x = 0
        bpy.context.scene.lattice_offset_y = 0
        bpy.context.scene.lattice_offset_z = 0

    @staticmethod
    def select_lattice(context):
        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        obj = bpy.context.active_object
        
        # Deselect all the faces
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        xMax = float('-inf')
        xMin = float('inf')

        for poly in obj.data.polygons:
            if (obj.matrix_world @ poly.center)[0]>=(bpy.data.lattices['Lattice'].points[0].co[0]*bpy.data.objects["Lattice"].scale[0]+bpy.data.objects["Lattice"].location[0]) and (obj.matrix_world @ poly.center)[0]<=(bpy.data.lattices['Lattice'].points[1].co[0]*bpy.data.objects["Lattice"].scale[0]+bpy.data.objects["Lattice"].location[0]):
                if (obj.matrix_world @ poly.center)[1]>=(bpy.data.lattices['Lattice'].points[0].co[1]*bpy.data.objects["Lattice"].scale[1]+bpy.data.objects["Lattice"].location[1]) and (obj.matrix_world @ poly.center)[1]<=(bpy.data.lattices['Lattice'].points[2].co[1]*bpy.data.objects["Lattice"].scale[1]+bpy.data.objects["Lattice"].location[1]):
                    if (obj.matrix_world @ poly.center)[2]>=(bpy.data.lattices['Lattice'].points[0].co[2]*bpy.data.objects["Lattice"].scale[2]+bpy.data.objects["Lattice"].location[2]) and (obj.matrix_world @ poly.center)[2]<=(bpy.data.lattices['Lattice'].points[4].co[2]*bpy.data.objects["Lattice"].scale[2]+bpy.data.objects["Lattice"].location[2]):
                        poly.select = True
                        xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                        xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                        
        #global sizeX
        #sizeX = xMax-xMin
        bpy.context.scene.size = xMax-xMin
        #global oldResize
        #oldResize = 1
        bpy.context.scene.oldResize = 1
                        
        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

    @staticmethod
    def delete_lattice(context):
        flagLattice = False
        for o in bpy.data.objects:
            if o.type == 'LATTICE':
                # Delete the existing lattice
                object_to_delete = bpy.data.objects["Lattice"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True) 
    
    @staticmethod
    def voxel(context):
        obj = bpy.context.active_object
    
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Remove all modifiers from the object
        obj.modifiers.clear()

        # Remesh the object with voxels
        bpy.ops.object.modifier_add(type='REMESH')
        bpy.context.object.modifiers["Remesh"].mode = 'VOXEL'
        bpy.context.object.modifiers["Remesh"].voxel_size = bpy.context.scene.voxel_size
        bpy.context.object.modifiers["Remesh"].adaptivity = 0
        bpy.context.object.modifiers["Remesh"].use_smooth_shade = False
        
    @staticmethod
    def decimate(context):
        obj = bpy.context.active_object
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Remove all modifiers from the object
        obj.modifiers.clear()

        # Decimate the faces of the object
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].decimate_type = 'COLLAPSE'
        bpy.context.object.modifiers["Decimate"].ratio = bpy.context.scene.decimate_ratio
        bpy.context.object.modifiers["Decimate"].use_symmetry = False
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True

    @staticmethod
    def validate(context):
        bpy.ops.object.apply_all_modifiers()
        
        obj = bpy.context.active_object
        print("Number of faces", len(obj.data.polygons))

    @staticmethod
    def manifold(context):
        Button_Operations.manifold_and_triangulate()

    @staticmethod
    def volume(context):
        obj = context.active_object
        
        scene = context.scene
        unit = scene.unit_settings
        
        # Set blender unit in mm
        unit.scale_length = 0.001
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'       
        
        scale = 1.0 if unit.system == 'NONE' else unit.scale_length
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        me = bpy.context.edit_object.data
        bm_orig = bmesh.from_edit_mesh(me)
        
        # Make a copy of the mesh
        bm = bm_orig.copy()

        # Apply modifier to the copy
        bm.transform(obj.matrix_world)
        
        print(scale)
        print(bm.calc_volume())
        
        # Calcul the volume
        bpy.types.Scene.volume = bm.calc_volume() * (scale ** 3.0) / (0.001 ** 3.0)
        print(bpy.types.Scene.volume)
        
        # Delete the copy
        bm.free()
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def remesh_blocks(context):
        obj = bpy.context.active_object
        
        nameCopy = "temp_copy"

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Remove all modifiers from the object
        obj.modifiers.clear()

        for o in bpy.data.objects:
            if o.type == 'MESH' and o.name == nameCopy:
                # Delete the existing copy
                object_to_delete = bpy.data.objects[nameCopy]
                bpy.data.objects.remove(object_to_delete, do_unlink=True) 
                
            
        # Make a copy of the object
        new_obj = obj.copy()
        new_obj.data = obj.data.copy()
        new_obj.animation_data_clear()
        bpy.context.collection.objects.link(new_obj)

        # Rename the copy
        new_obj.name = nameCopy

        # Hide the copy
        new_obj.hide_viewport = True

        # Remesh the faces of the object with blocks
        bpy.ops.object.modifier_add(type='REMESH')
        bpy.context.object.modifiers["Remesh"].mode = 'BLOCKS'
        bpy.context.object.modifiers["Remesh"].octree_depth = bpy.context.scene.level_blocks
        bpy.context.object.modifiers["Remesh"].scale = 0.99
        bpy.context.object.modifiers["Remesh"].use_remove_disconnected = False
        bpy.context.object.modifiers["Remesh"].threshold = 1
        bpy.context.object.modifiers["Remesh"].use_smooth_shade = False

        # Make intersection between the remesh object and the original
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].operand_type = 'OBJECT'
        bpy.context.object.modifiers["Boolean"].object = bpy.data.objects[nameCopy]
        bpy.context.object.modifiers["Boolean"].solver = 'FAST'
        bpy.context.object.modifiers["Boolean"].double_threshold = 0

    @staticmethod
    def validate_blocks(context):
        # Validate the remesh blocks modifiers
        bpy.ops.object.apply_all_modifiers()
        
        # Select faces where normals point down
        date_1 = datetime.datetime.now()
        print("Start")
        
        # Select the bottom faces
        Button_Operations.select_faces(radians(10))

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False) 

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # Pass in vertices selection
        bpy.ops.mesh.select_mode(type="VERT")

        # Select non manifold vertices
        bpy.ops.mesh.select_non_manifold()

        # Add an edge or face to selected
        bpy.ops.mesh.edge_face_add()

        # Pass in faces selection
        bpy.ops.mesh.select_mode(type="FACE")
        
        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Triangulate the faces
        bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED_ALTERNATE', ngon_method='CLIP')

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
      
        # Delete the copy
        object_to_delete = bpy.data.objects["temp_copy"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True) 
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
    @staticmethod
    def measure_distance(context):
        obj = bpy.context.active_object
    
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the two selected vertices
        twoVerts = [None, None]
        index = 0
        for vertex in obj.data.vertices:
            if vertex.select:
                twoVerts[index] = (obj.matrix_world @ vertex.co)
                index = index + 1
                if index == 2:
                    break   
        
        print(twoVerts)
        
        if twoVerts[0] != None and twoVerts[1] != None:
            bpy.context.scene.distance[0] = abs(twoVerts[0].x - twoVerts[1].x)
            bpy.context.scene.distance[1] = abs(twoVerts[0].y - twoVerts[1].y)
            bpy.context.scene.distance[2] = abs(twoVerts[0].z - twoVerts[1].z)
            bpy.context.scene.distance[3] = sqrt(bpy.context.scene.distance[0]**2 + bpy.context.scene.distance[1]**2 + bpy.context.scene.distance[2]**2)
        else:
            bpy.context.scene.distance[0] = 0
            bpy.context.scene.distance[1] = 0
            bpy.context.scene.distance[2] = 0
            bpy.context.scene.distance[3] = 0  
            
        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

  
def register(): 
    # register all the classes
    classes = (Get_And_Set_Rotation, Get_And_Set_Lattice, Button_Operations)
    register = bpy.utils.register_classes_factory(classes)
    
    register_class(STL_FILE_import)
    register_class(STL_FILE_export)

    register_class(BUTTON_PT_import_export)   
    register_class(BUTTON_OT_button_op)
    register_class(BUTTON_PT_rotation)
    register_class(BUTTON_PT_generation)
    register_class(BUTTON_PT_area)
    register_class(BUTTON_PT_offset)
    register_class(BUTTON_PT_resize)
    register_class(BUTTON_PT_lattice)
    register_class(BUTTON_PT_voxel) 
    register_class(BUTTON_PT_measure) 
 
    # create personal properties
    bpy.types.Scene.angle_x = bpy.props.FloatProperty(name="Angle x", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_x, set=Get_And_Set_Rotation.set_angle_x, unit = 'ROTATION')
    bpy.types.Scene.angle_y = bpy.props.FloatProperty(name="Angle y", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_y, set=Get_And_Set_Rotation.set_angle_y, unit = 'ROTATION')
    bpy.types.Scene.angle_z = bpy.props.FloatProperty(name="Angle z", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_z, set=Get_And_Set_Rotation.set_angle_z, unit = 'ROTATION')
    bpy.types.Scene.max_angle = bpy.props.FloatProperty(name="Max Angle", default = pi/4, options={'SKIP_SAVE'}, min = 0, max = pi/2, soft_min = 0, soft_max = pi/2, step = 100, unit = 'ROTATION')
    bpy.types.Scene.min_area = bpy.props.FloatProperty(name="Min Area", default = 0.1, options={'SKIP_SAVE'}, min = 0, max = 1, soft_min = 0, soft_max = 1, step = 1, unit = 'AREA')
    bpy.types.Object.offset = bpy.props.FloatProperty(name = "Offset", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 10, unit = 'LENGTH')
    bpy.types.Scene.resize = bpy.props.FloatProperty(name = "Resize", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 1, unit = 'LENGTH')
    bpy.types.Scene.lattice_size_x = bpy.props.FloatProperty(name = "Size X", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_size_y = bpy.props.FloatProperty(name = "Size Y", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_size_z = bpy.props.FloatProperty(name = "Size Z", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_x = bpy.props.FloatProperty(name = "Offset X", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_y = bpy.props.FloatProperty(name = "Offset Y", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_z = bpy.props.FloatProperty(name = "Offset Z", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.min_angle_z = bpy.props.FloatProperty(name="Min Angle z", default = pi/2, options={'SKIP_SAVE'}, min = 0, max = radians(181),soft_min = 0, soft_max = radians(181), step = 100, unit = 'ROTATION')
    bpy.types.Scene.max_angle_z = bpy.props.FloatProperty(name="Max Angle z", default = pi/2, options={'SKIP_SAVE'}, min = 0, max = radians(181),soft_min = 0, soft_max = radians(181), step = 100, unit = 'ROTATION')
    bpy.types.Scene.size = bpy.props.FloatProperty(default = 0)
    bpy.types.Scene.oldResize = bpy.props.FloatProperty(default = 1)
    bpy.types.Scene.voxel_size = bpy.props.FloatProperty(name="Voxel Size", default = 0.01, options={'SKIP_SAVE'}, min = 0.01, max = 0.1,soft_min = 0.01, soft_max = 0.1, step = 1, unit = 'LENGTH')
    bpy.types.Scene.decimate_ratio = bpy.props.FloatProperty(name="Decimate Ratio", default = 0.01, options={'SKIP_SAVE'}, min = 0, max = 1,soft_min = 0, soft_max = 1, step = 1)
    bpy.types.Scene.volume = bpy.props.FloatProperty(name="Volume", default = 0, options={'SKIP_SAVE'}, min = 0, step = 100)
    bpy.types.Scene.level_blocks = bpy.props.IntProperty(name="Level Blocks", default = 5, options={'SKIP_SAVE'}, min = 1, max = 9,soft_min = 1, soft_max = 9, step = 1)
    bpy.types.Scene.distance = bpy.props.FloatVectorProperty(name='Distance', default=(0.0, 0.0, 0.0, 0.0), options={'SKIP_SAVE'}, step=3, size=4)
 
def unregister():
    # delete personal properties
    del bpy.types.Scene.angle_x
    del bpy.types.Scene.angle_y
    del bpy.types.Scene.angle_z
    del bpy.types.Scene.max_angle
    del bpy.types.Scene.min_area
    del bpy.types.Object.offset
    del bpy.types.Scene.resize
    del bpy.types.Scene.lattice_size_x
    del bpy.types.Scene.lattice_size_y
    del bpy.types.Scene.lattice_size_z
    del bpy.types.Scene.lattice_offset_x
    del bpy.types.Scene.lattice_offset_y
    del bpy.types.Scene.lattice_offset_z
    del bpy.types.Scene.min_angle_z
    del bpy.types.Scene.max_angle_z
    del bpy.types.Scene.size
    del bpy.types.Scene.oldResize
    del bpy.types.Scene.voxel_size
    del bpy.types.Scene.decimate_ratio
    del bpy.types.Scene.volume
    del bpy.types.Scene.level_blocks
    del bpy.types.Scene.distance

    # unregister all the classes 
    classes = (Get_And_Set_Rotation, Get_And_Set_Lattice, Button_Operations)
    unregister = bpy.utils.register_classes_factory(classes)
 
    unregister_class(STL_FILE_import)
    unregister_class(STL_FILE_export)

    unregister_class(BUTTON_PT_import_export)    
    unregister_class(BUTTON_OT_button_op)
    unregister_class(BUTTON_PT_rotation)
    unregister_class(BUTTON_PT_generation)
    unregister_class(BUTTON_PT_area)
    unregister_class(BUTTON_PT_offset)
    unregister_class(BUTTON_PT_resize)
    unregister_class(BUTTON_PT_lattice)
    unregister_class(BUTTON_PT_voxel)
    unregister_class(BUTTON_PT_measure) 
 
 
if __name__ == '__main__':
    register()