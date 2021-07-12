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
  importlib.reload(operations)
  importlib.reload(import_export)
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
import bmesh

from math import pi
from math import radians

import datetime
import glob


name_filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//"


#-------------------------------------------------------
# Class for descript the panels of the button controller
#-------------------------------------------------------

class BUTTON_PT_import_export(Panel):
    bl_idname = 'BUTTON_PT_import_export'
    bl_label = 'Import/Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        
        layout.operator(BUTTON_OT_button_m_to_mm.bl_idname)
        layout.operator(BUTTON_OT_button_volume.bl_idname)
              
        layout.label(text= ("Volume : " + '{:.2f}'.format(bpy.context.scene.volume) + " mm³"))             

        layout.operator(BUTTON_OT_button_import_object.bl_idname)
        layout.operator(BUTTON_OT_button_export_object.bl_idname)

        if len(bpy.context.selected_objects) != 0:
            layout.label(text= ("Number of faces : " + str(len(bpy.context.active_object.data.polygons))))
            layout.label(text= ("Size of the stl file : ~" + str(int(len(bpy.context.active_object.data.polygons)/20.4)) + " Ko"))

        layout.operator(BUTTON_OT_button_triangulate.bl_idname)
 
class BUTTON_PT_rotation_offset(Panel):
    bl_idname = 'BUTTON_PT_rotation_offset'
    bl_label = 'Rotation and offset'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "angle_x")  
        row.prop(scene, "angle_y")
        row.prop(scene, "angle_z") 

        box2 = layout.box()
        row = box2.row()
        row.prop(context.scene, "offset")        
        
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
        
        layout.operator(BUTTON_OT_button_import_for_test.bl_idname)
        layout.operator(BUTTON_OT_button_select_faces.bl_idname)
        layout.operator(BUTTON_OT_button_generate_support.bl_idname)
        layout.operator(BUTTON_OT_button_generate_mold.bl_idname)
        layout.operator(BUTTON_OT_button_manifold.bl_idname)
        layout.operator(BUTTON_OT_button_regenerate_bottom.bl_idname)
        layout.operator(BUTTON_OT_button_generate_socle.bl_idname)
        
class BUTTON_PT_area(Panel):
    bl_idname = 'BUTTON_PT_area'
    bl_label = 'Area'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
        
        box = layout.box()
        row = box.row()
        row.prop(scene, "min_area")
        
        layout.operator(BUTTON_OT_button_generate_area.bl_idname)
        layout.operator(BUTTON_OT_button_separate_faces.bl_idname)
        layout.operator(BUTTON_OT_button_select_area.bl_idname)
        
class BUTTON_PT_resize(Panel):
    bl_idname = 'BUTTON_PT_resize'
    bl_label = 'Resize'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout 
        scene = context.scene 
        
        layout.operator(BUTTON_OT_button_select_resize_all.bl_idname)        
        
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "min_angle_z")  
        row.prop(scene, "max_angle_z")  
        
        layout.operator(BUTTON_OT_button_select_resize.bl_idname)          

        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "resize")  
        layout.operator(BUTTON_OT_button_resize.bl_idname)  
        
        layout.separator()
        
        layout.operator(BUTTON_OT_button_invert_selection.bl_idname)
        layout.operator(BUTTON_OT_button_delete_selection.bl_idname)
        layout.operator(BUTTON_OT_button_fill.bl_idname)          

class BUTTON_PT_lattice(Panel):
    bl_idname = 'BUTTON_PT_lattice'
    bl_label = 'Lattice'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout 
        scene = context.scene 

        layout.operator(BUTTON_OT_button_add_lattice.bl_idname) 
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
        
        layout.operator(BUTTON_OT_button_select_lattice.bl_idname) 
        layout.operator(BUTTON_OT_button_delete_lattice.bl_idname) 
        
class BUTTON_PT_voxel(Panel):
    bl_idname = 'BUTTON_PT_voxel'
    bl_label = 'Voxel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "voxel_size")
        layout.operator(BUTTON_OT_button_voxel.bl_idname) 
        layout.operator(BUTTON_OT_button_validate.bl_idname) 
        
        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "decimate_ratio")
        layout.operator(BUTTON_OT_button_decimate.bl_idname) 
        layout.operator(BUTTON_OT_button_validate.bl_idname) 
        
        box3 = layout.box()
        row = box3.row()
        row.prop(scene, "level_blocks")
        layout.operator(BUTTON_OT_button_remesh_blocks.bl_idname) 
        layout.operator(BUTTON_OT_button_validate_blocks.bl_idname) 
           
class BUTTON_PT_measure(Panel):
    bl_idname = 'BUTTON_PT_measure'
    bl_label = 'Measure'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context): 
        layout = self.layout    
        scene = context.scene
        
        layout.operator(BUTTON_OT_button_measure_distance.bl_idname) 
        layout.label(text= ("X : " + '{:.2f}'.format(bpy.context.scene.distance[0]) + " mm"))
        layout.label(text= ("Y : " + '{:.2f}'.format(bpy.context.scene.distance[1]) + " mm"))
        layout.label(text= ("Z : " + '{:.2f}'.format(bpy.context.scene.distance[2]) + " mm"))
        layout.label(text= ("Distance : " + '{:.2f}'.format(bpy.context.scene.distance[3]) + " mm"))


#-------------------------------------------------------
# Class for descript the buttons of the button controller
#-------------------------------------------------------

class BUTTON_OT_button_m_to_mm(Operator):
  bl_idname = "btn.m_to_mm"
  bl_label = "m to mm"
  bl_description = 'Change the Blender scale from metre to milimetre'
 
  def execute(self, context):
    Button_Operations.m_to_mm()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_volume(Operator):
  bl_idname = "btn.volume"
  bl_label = "Volume"
  bl_description = 'Calculate the volume of the selected mesh'
 
  def execute(self, context):
    Button_Operations.volume()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_import_object(Operator):
  bl_idname = "btn.import_object"
  bl_label = "Import Object"
  bl_description = 'Open a file explorer to import a stl file'
 
  def execute(self, context):
    bpy.ops.stl_file.import_file('INVOKE_DEFAULT') 
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_export_object(Operator):
  bl_idname = "btn.export_object"
  bl_label = "Export Object"
  bl_description = 'Open a file explorer to export a stl file'
 
  def execute(self, context):
    bpy.ops.stl_file.export_file('INVOKE_DEFAULT') 
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_triangulate(Operator):
  bl_idname = "btn.triangulate"
  bl_label = "Triangulate"
  bl_description = 'Triangulate all the faces of the selected mesh'
 
  def execute(self, context):
    Button_Operations.triangulate()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}    

class BUTTON_OT_button_import_for_test(Operator):
  bl_idname = "btn.import_for_test"
  bl_label = "Import for test"
  bl_description = 'Import the first stl of the specified file name'
 
  def execute(self, context):
    # init properties of angles and offset
    bpy.context.scene.angle_x = 0
    bpy.context.scene.angle_y = 0
    bpy.context.scene.angle_z = 0
    bpy.context.scene.offset = 0 

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
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_select_faces(Operator):
  bl_idname = "btn.select_faces"
  bl_label = "Select faces"
  bl_description = 'Select the faces needed support'
 
  def execute(self, context):
    Button_Operations.select_faces(bpy.context.scene.max_angle)
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_generate_support(Operator):
  bl_idname = "btn.generate_support"
  bl_label = "Generate support"
  bl_description = 'Generate support for the selected faces'
 
  def execute(self, context):
    Button_Operations.generate_support()
    Button_Operations.manifold()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}
    
class BUTTON_OT_button_generate_mold(Operator):
  bl_idname = "btn.generate_mold"
  bl_label = "Generate mold"
  bl_description = 'Generate mold for the selected faces'
 
  def execute(self, context):
    date_x = datetime.datetime.now()

    obj = bpy.context.active_object
    moldOffset = bpy.context.scene.offset#obj.offset

    nameCopy = "temp_copy"

    nameObject = bpy.context.active_object.name
    
    # Switch in object mode 
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Apply location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
    
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
    #bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
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
    
    # Apply location
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
    
    # init properties of angles
    bpy.context.scene.angle_x = 0
    bpy.context.scene.angle_y = 0
    bpy.context.scene.angle_z = 0
    bpy.context.scene.offset = 0
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_manifold(Operator):
  bl_idname = "btn.manifold"
  bl_label = "Manifold"
  bl_description = 'Find the non manifold vertices and add edges and faces to fill the hole'
 
  def execute(self, context):
    Button_Operations.manifold()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_regenerate_bottom(Operator):
  bl_idname = "btn.regenerate_bottom"
  bl_label = "Regenerate bottom"
  bl_description = 'Regenerate bottom if the bottom is bad generated'
 
  def execute(self, context):
    Button_Operations.regenerate_bottom()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_generate_socle(Operator):
  bl_idname = "btn.generate_socle"
  bl_label = "Generate socle"
  bl_description = 'Generate a socle to the selected mesh'
 
  def execute(self, context):
    Button_Operations.generate_socle()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}


class BUTTON_OT_button_generate_area(Operator):
  bl_idname = "btn.generate_area"
  bl_label = "Generate support (area)"
  bl_description = 'Generate support for the selected faces with the area min parameter'
 
  def execute(self, context):
    Button_Operations.separate_faces()
    Button_Operations.select_area(bpy.context.scene.min_area)
    Button_Operations.generate_support()
    Button_Operations.manifold()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_separate_faces(Operator):
  bl_idname = "btn.separate_faces"
  bl_label = "Separate faces"
  bl_description = 'Separate selected faces in a new mesh and delete the base object'
 
  def execute(self, context):
    Button_Operations.separate_faces()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_select_area(Operator):
  bl_idname = "btn.select_area"
  bl_label = "Select area"
  bl_description = 'Find all the separated pieces of the mesh and select the pieces where the area is higher than the minimum area value'
 
  def execute(self, context):
    Button_Operations.select_area(bpy.context.scene.min_area)
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}


class BUTTON_OT_button_select_resize_all(Operator):
  bl_idname = "btn.select_resize_all"
  bl_label = "Select resize all"
  bl_description = 'Select all the faces connected to the selected faces'
 
  def execute(self, context):
    Button_Operations.select_resize_all()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}
    
class BUTTON_OT_button_select_resize(Operator):
  bl_idname = "btn.select_resize"
  bl_label = "Select resize"
  bl_description = 'Select all the faces connected to the selected faces between a min and max angle between the normal and the downward vector'
 
  def execute(self, context):
    Button_Operations.select_resize(bpy.context.scene.min_angle_z, bpy.context.scene.max_angle_z)
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_resize(Operator):
  bl_idname = "btn.resize"
  bl_label = "Resize"
  bl_description = 'Resize the selection'
 
  def execute(self, context):
    Button_Operations.resize()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_invert_selection(Operator):
  bl_idname = "btn.invert_selection"
  bl_label = "Invert selection"
  bl_description = 'Invert the selection'
 
  def execute(self, context):
    Button_Operations.invert_selection()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}    

class BUTTON_OT_button_delete_selection(Operator):
  bl_idname = "btn.delete_selection"
  bl_label = "Delete selection"
  bl_description = 'Delete the selection'
 
  def execute(self, context):
    Button_Operations.delete_selection()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_fill(Operator):
  bl_idname = "btn.fill"
  bl_label = "Fill"
  bl_description = 'Fill hole for the selection'
 
  def execute(self, context):
    Button_Operations.fill()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}


class BUTTON_OT_button_add_lattice(Operator):
  bl_idname = "btn.add_lattice"
  bl_label = "Add lattice"
  bl_description = 'Add a lattice object with the size and location of the selected mesh'
 
  def execute(self, context):
    Button_Operations.add_lattice()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_select_lattice(Operator):
  bl_idname = "btn.select_lattice"
  bl_label = "Select lattice"
  bl_description = 'Select faces in the lattice of the selected mesh'
 
  def execute(self, context):
    Button_Operations.select_lattice()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_delete_lattice(Operator):
  bl_idname = "btn.delete_lattice"
  bl_label = "Delete lattice"
  bl_description = 'Delete the existing lattice'
 
  def execute(self, context):
    Button_Operations.delete_lattice()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}


class BUTTON_OT_button_voxel(Operator):
  bl_idname = "btn.voxel"
  bl_label = "Add Voxel"
  bl_description = 'Add a voxel remesh to the selected mesh'
 
  def execute(self, context):
    Button_Operations.voxel()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_decimate(Operator):
  bl_idname = "btn.decimate"
  bl_label = "Add Decimate"
  bl_description = 'Decrease the number of the faces to the selected mesh'
 
  def execute(self, context):
    Button_Operations.decimate()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_validate(Operator):
  bl_idname = "btn.validate"
  bl_label = "Validate"
  bl_description = 'Apply modifier to the selected mesh'
 
  def execute(self, context):
    Button_Operations.validate()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_remesh_blocks(Operator):
  bl_idname = "btn.remesh_blocks"
  bl_label = "Remesh Blocks"
  bl_description = 'Add a blocks remesh to the selected mesh and make an intersection with the mesh to keep the same occupied surface'
 
  def execute(self, context):
    Button_Operations.remesh_blocks()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

class BUTTON_OT_button_validate_blocks(Operator):
  bl_idname = "btn.validate_blocks"
  bl_label = "Validate Blocks"
  bl_description = 'Apply blocks modifier to the selected mesh and extrude the bottom on the xy plane'
 
  def execute(self, context):
    Button_Operations.validate_blocks()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}


class BUTTON_OT_button_measure_distance(Operator):
  bl_idname = "btn.measure_distance"
  bl_label = "Measure distance"
  bl_description = 'Calculate the distance between two selected vertices'
 
  def execute(self, context):
    Button_Operations.measure_distance()
    self.report({'INFO'}, f"This is {self.bl_idname}")
    return {'FINISHED'}

        
# List of classes that is not a subclass of a Blender type class
utilityClasses = (
    Get_And_Set_Rotation, 
    Get_And_Set_Offset, 
    Get_And_Set_Lattice, 
    Button_Operations
)

# List of classes that is a subclass of a Blender type class
blenderClasses = (
    STL_FILE_import,
    STL_FILE_export,
    
    
    BUTTON_PT_import_export,
    BUTTON_PT_rotation_offset,
    BUTTON_PT_generation,
    BUTTON_PT_area,
    BUTTON_PT_resize,
    BUTTON_PT_lattice,
    BUTTON_PT_voxel,
    BUTTON_PT_measure,
    
    
    BUTTON_OT_button_m_to_mm,
    BUTTON_OT_button_volume,
    BUTTON_OT_button_import_object,
    BUTTON_OT_button_export_object,
    BUTTON_OT_button_import_for_test,
    BUTTON_OT_button_triangulate,
    
    BUTTON_OT_button_select_faces,
    BUTTON_OT_button_generate_support,
    BUTTON_OT_button_generate_mold,
    BUTTON_OT_button_manifold,
    BUTTON_OT_button_regenerate_bottom,
    BUTTON_OT_button_generate_socle,
    
    BUTTON_OT_button_generate_area,
    BUTTON_OT_button_separate_faces,
    BUTTON_OT_button_select_area,
    
    BUTTON_OT_button_select_resize_all,
    BUTTON_OT_button_select_resize,
    BUTTON_OT_button_resize,
    BUTTON_OT_button_invert_selection,
    BUTTON_OT_button_delete_selection,
    BUTTON_OT_button_fill,
    
    BUTTON_OT_button_add_lattice,
    BUTTON_OT_button_select_lattice,
    BUTTON_OT_button_delete_lattice,
    
    BUTTON_OT_button_voxel,
    BUTTON_OT_button_decimate,
    BUTTON_OT_button_validate,
    BUTTON_OT_button_remesh_blocks,
    BUTTON_OT_button_validate_blocks,
    
    BUTTON_OT_button_measure_distance
) 
  
def register():    
    # register all the utility classes
    register = bpy.utils.register_classes_factory(utilityClasses)

    # register all the blender classes    
    for cls in blenderClasses:
        bpy.utils.register_class(cls)

    # create personal properties
    bpy.types.Scene.volume = bpy.props.FloatProperty(name="Volume", default = 0, options={'SKIP_SAVE'}, min = 0, step = 100)
    
    bpy.types.Scene.angle_x = bpy.props.FloatProperty(name="Angle x", description="Angle x of the selected mesh", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_x, set=Get_And_Set_Rotation.set_angle_x, unit = 'ROTATION')
    bpy.types.Scene.angle_y = bpy.props.FloatProperty(name="Angle y", description="Angle y of the selected mesh", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_y, set=Get_And_Set_Rotation.set_angle_y, unit = 'ROTATION')
    bpy.types.Scene.angle_z = bpy.props.FloatProperty(name="Angle z", description="Angle x of the selected mesh", default = 0, options={'SKIP_SAVE'}, min = -pi, max = pi, soft_min = -pi, soft_max = pi, step = 100, get=Get_And_Set_Rotation.get_angle_z, set=Get_And_Set_Rotation.set_angle_z, unit = 'ROTATION')
    bpy.types.Scene.offset = bpy.props.FloatProperty(name = "Offset", description="Offset of the selected mesh", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 10,get=Get_And_Set_Offset.get_offset, set=Get_And_Set_Offset.set_offset, unit = 'LENGTH')
        
    bpy.types.Scene.max_angle = bpy.props.FloatProperty(name="Max Angle", description="Angle under the face is selected", default = pi/4, options={'SKIP_SAVE'}, min = 0, max = pi/2, soft_min = 0, soft_max = pi/2, step = 100, unit = 'ROTATION')    
    bpy.types.Scene.min_area = bpy.props.FloatProperty(name="Min Area", description="Minimum value of the area for select the faces of a piece of a mesh", default = 0.1, options={'SKIP_SAVE'}, min = 0, max = 1, soft_min = 0, soft_max = 1, step = 1, unit = 'AREA')
    
    bpy.types.Scene.min_angle_z = bpy.props.FloatProperty(name="Min Angle z", description="Min angle between the normal and downward vector where the connected faces is selected", default = pi/2, options={'SKIP_SAVE'}, min = 0, max = radians(181),soft_min = 0, soft_max = radians(181), step = 100, unit = 'ROTATION')
    bpy.types.Scene.max_angle_z = bpy.props.FloatProperty(name="Max Angle z", description="Max angle between the normal and downward vector where the connected faces is selected", default = pi/2, options={'SKIP_SAVE'}, min = 0, max = radians(181),soft_min = 0, soft_max = radians(181), step = 100, unit = 'ROTATION')
    bpy.types.Scene.resize = bpy.props.FloatProperty(name = "Resize", description="Value of the size to resize the selected mesh", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 1, unit = 'LENGTH')    
    bpy.types.Scene.sizeX = bpy.props.FloatProperty(default = 0)
    bpy.types.Scene.sizeY = bpy.props.FloatProperty(default = 0)
    bpy.types.Scene.oldResizeX = bpy.props.FloatProperty(default = 1)
    bpy.types.Scene.oldResizeY = bpy.props.FloatProperty(default = 1)
    
    bpy.types.Scene.lattice_size_x = bpy.props.FloatProperty(name = "Size X", description="Size x of the lattice", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_size_y = bpy.props.FloatProperty(name = "Size Y", description="Size y of the lattice", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_size_z = bpy.props.FloatProperty(name = "Size Z", description="Size z of the lattice", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_x = bpy.props.FloatProperty(name = "Offset X", description="Offfset x of the lattice", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_y = bpy.props.FloatProperty(name = "Offset Y", description="Offfset y of the lattice", default = 0, step = 10, unit = 'LENGTH')
    bpy.types.Scene.lattice_offset_z = bpy.props.FloatProperty(name = "Offset Z", description="Offfset z of the lattice", default = 0, step = 10, unit = 'LENGTH')
    
    bpy.types.Scene.voxel_size = bpy.props.FloatProperty(name="Voxel Size", description="Size of the voxel in object space used for volume evaluation", default = 0.01, options={'SKIP_SAVE'}, min = 0.01, max = 0.1,soft_min = 0.01, soft_max = 0.1, step = 1, unit = 'LENGTH')
    bpy.types.Scene.decimate_ratio = bpy.props.FloatProperty(name="Decimate Ratio", description="Ratio of triangles to reduce to", default = 0.01, options={'SKIP_SAVE'}, min = 0, max = 1,soft_min = 0, soft_max = 1, step = 1)
    bpy.types.Scene.level_blocks = bpy.props.IntProperty(name="Level Blocks", description="Resolution of the blocks", default = 5, options={'SKIP_SAVE'}, min = 1, max = 9,soft_min = 1, soft_max = 9, step = 1)
    
    bpy.types.Scene.distance = bpy.props.FloatVectorProperty(name='Distance',  default=(0.0, 0.0, 0.0, 0.0), options={'SKIP_SAVE'}, step=3, size=4)
 
def unregister():
    # delete personal properties
    del bpy.types.Scene.volume
    
    del bpy.types.Scene.angle_x
    del bpy.types.Scene.angle_y
    del bpy.types.Scene.angle_z
    del bpy.types.Scene.offset
        
    del bpy.types.Scene.max_angle
    del bpy.types.Scene.min_area

    del bpy.types.Scene.min_angle_z
    del bpy.types.Scene.max_angle_z
    del bpy.types.Scene.resize
    del bpy.types.Scene.sizeX
    del bpy.types.Scene.sizeY
    del bpy.types.Scene.oldResizeX
    del bpy.types.Scene.oldResizeY
    
    del bpy.types.Scene.lattice_size_x
    del bpy.types.Scene.lattice_size_y
    del bpy.types.Scene.lattice_size_z
    del bpy.types.Scene.lattice_offset_x
    del bpy.types.Scene.lattice_offset_y
    del bpy.types.Scene.lattice_offset_z
    
    del bpy.types.Scene.voxel_size
    del bpy.types.Scene.decimate_ratio
    del bpy.types.Scene.level_blocks
    
    del bpy.types.Scene.distance

    # unregister all the utility classes 
    unregister = bpy.utils.register_classes_factory(utilityClasses)

    # unregister all the blender classes  
    for cls in blenderClasses:
        bpy.utils.unregister_class(cls)
 
 
if __name__ == '__main__':
    register()