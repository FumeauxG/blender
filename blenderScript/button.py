bl_info = {
    "name": "Button Controller",
    "description": "Button Controller",
    "author": "Fumeaux Gaëtan",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "category": "Object",
}

import glob
import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
import mathutils
import datetime
import bmesh
import ctypes

# For import export
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty
from bpy.utils import register_class


 
class BUTTON_PT_rotation(Panel):
    bl_idname = 'BUTTON_PT_rotation'
    bl_label = 'Rotation'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.operator('btn.btn_op', text='Rotation x').action = 'ROTX'
        layout.operator('btn.btn_op', text='Rotation y').action = 'ROTY'
        layout.operator('btn.btn_op', text='Rotation z').action = 'ROTZ'
        
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
        
        layout.operator('btn.btn_op', text='Import object').action = 'IMPORT'
        layout.operator('btn.btn_op', text='Select faces').action = 'SELECT'
        layout.operator('btn.btn_op', text='Select faces fast').action = 'SELECTFAST'
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
        layout.operator('btn.btn_op', text='Generate support (area2)').action = 'GENERATE_AREA_2'
        
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
        
        layout.operator('btn.btn_op', text='Mold').action = 'MOLD'

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
        
class BUTTON_PT_import_export(Panel):
    bl_idname = 'BUTTON_PT_import_export'
    bl_label = 'Import/Export'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
 
    def draw(self, context):
        layout = self.layout    
        scene = context.scene
        
        layout.label(text="Beta import/export")
        
        layout.operator('btn.btn_op', text='Test import').action = 'TEST_IMPORT'
        layout.operator('btn.btn_op', text='Test export').action = 'TEST_EXPORT'      
        
class BUTTON_OT_button_op(Operator):
    bl_idname = 'btn.btn_op'
    bl_label = 'Button'
    bl_description = 'Button'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('ROTX', 'rotation x', 'rotation x'),
            ('ROTY', 'rotation y', 'rotation y'),
            ('ROTZ', 'rotation z', 'rotation z'),
            
            ('IMPORT', 'Import object', 'Import object'),
            ('SELECT', 'Select faces', 'Select faces'),
            ('SELECTFAST', 'Select faces fast', 'Select faces fast'),
            ('GENERATE', 'Generate support', 'Generate support'),
            
            ('GENERATE_AREA', 'Generate support (area)', 'Generate support (area)'),
            ('SEPARATE', 'Separate faces', 'Separate faces)'),
            ('SELECT2', 'Select faces 2', 'Select faces 2'),
            ('GENERATE_AREA_2', 'Generate support (area2)', 'Generate support (area2)'),
            
            ('OFFSET', 'Offset', 'Offset'),
            ('MOLD', 'Mold', 'Mold'),
            
            ('SELECT_RESIZE', 'Select resize', 'Select resize'),
            ('SELECT_RESIZE_ALL', 'Select resize all', 'Select resize all'),
            ('RESIZE', 'Resize', 'Resize'),
            ('DELETE_SELECTION', 'Delete selection', 'Delete selection'),
            ('FILL', 'Fill', 'Fill'),
            
            ('VOXEL', 'Voxel', 'Voxel'),
            ('DECIMATE', 'Decimate', 'Decimate'),
            ('VALIDATE', 'Validate', 'Validate'),
            ('MANIFOLD', 'Manifold', 'Manifold'),
            ('VOLUME', 'Volume', 'Volume'),
            ('REMESH_BLOCKS', 'Remesh Blocks', 'Remesh Blocks'),
            ('VALIDATE_BLOCKS', 'Validate Blocks', 'Validate Blocks'),
            
            ('TEST_IMPORT', 'Test import', 'Test import'),
            ('TEST_EXPORT', 'Test export', 'Test export')            
        ]
    )
 
    def execute(self, context):
        if self.action == 'ROTX':
            self.rot_x(context=context)
        elif self.action == 'ROTY':
            self.rot_y(context=context)
        elif self.action == 'ROTZ':
            self.rot_z(context=context)
            
        elif self.action == 'IMPORT':
            self.import_object(context=context)
        elif self.action == 'SELECT':   
            self.select_faces(context=context) 
        elif self.action == 'SELECTFAST':   
            self.select_faces_fast(context=context) 
        elif self.action == 'GENERATE':   
            self.generate_support(context=context)
            
        elif self.action == 'GENERATE_AREA':   
            self.generate_support_area(context=context)
        elif self.action == 'SEPARATE':   
            self.separate_faces(context=context)
        elif self.action == 'SELECT2':   
            self.select_faces_2(context=context) 
        elif self.action == 'GENERATE_AREA_2':   
            self.generate_support_area_2(context=context) 
            
        elif self.action == 'OFFSET':   
            self.offset(context=context) 
        elif self.action == 'MOLD':   
            self.mold(context=context)
            
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
         
        elif self.action == 'TEST_IMPORT':   
            self.test_import(context=context)
        elif self.action == 'TEST_EXPORT':   
            self.test_export(context=context)
            
            
        return {'FINISHED'}
    
    
    @staticmethod
    def rot_x(context):
        pi = 3.14159265
        
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        oldX  = (bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi
        oldY  = (bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi
        oldZ  = (bpy.context.selected_objects[0].rotation_euler[2]) * 180/pi

        #convert degrees to radians
        x = ((90+oldX)%360)*pi/180
        y = oldY*pi/180
        z = oldZ*pi/180
        xyz_rot = (x,y,z)

        for obj in bpy.context.selected_objects:
            obj.rotation_euler = xyz_rot
            
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
 
        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
 
        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT') 
 
    @staticmethod
    def rot_y(context):
        pi = 3.14159265

        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        oldX  = (bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi
        oldY  = (bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi
        oldZ  = (bpy.context.selected_objects[0].rotation_euler[2]) * 180/pi

        #convert degrees to radians
        x = oldX*pi/180
        y = ((90+oldY)%360)*pi/180
        z = oldZ*pi/180
        xyz_rot = (x,y,z)

        for obj in bpy.context.selected_objects:
            obj.rotation_euler = xyz_rot
            
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})

        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
 
        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
 
    @staticmethod
    def rot_z(context):
        pi = 3.14159265

        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        oldX  = (bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi
        oldY  = (bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi
        oldZ  = (bpy.context.selected_objects[0].rotation_euler[2]) * 180/pi

        #convert degrees to radians
        x = oldX*pi/180
        y = oldY*pi/180
        z = ((90+oldZ)%360)*pi/180
        xyz_rot = (x,y,z)

        for obj in bpy.context.selected_objects:
            obj.rotation_euler = xyz_rot
            
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})

        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
 
        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        
    @staticmethod
    def import_object(context):
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
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Deselect all
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")

        print("Make Selection")
        
    @staticmethod
    def select_faces(context):
        date_1 = datetime.datetime.now()
        print("Start")

        pi = 3.14159265
        maxAngle = bpy.context.scene.max_angle
        print(maxAngle)
        maxAngleRad = maxAngle*pi/180

        obj = bpy.context.active_object

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co) 
        
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]

        print(vecDir)
        for poly in obj.data.polygons:
            angle = mathutils.Vector(poly.normal).angle(vecDir)
            if angle < maxAngleRad:
                poly.select = True
                print(poly.index)
                triangleCenter = (tabVertices[poly.vertices[0]]+tabVertices[poly.vertices[1]]+tabVertices[poly.vertices[2]])/3
                        
                for comparePoly in obj.data.polygons:
                    if  (mathutils.geometry.intersect_ray_tri(tabVertices[comparePoly.vertices[0]], tabVertices[comparePoly.vertices[1]], tabVertices[comparePoly.vertices[2]], mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != comparePoly.index):
                        poly.select = False
                        break
                        

        bpy.ops.object.mode_set(mode = 'EDIT')
        print("Endscript")

        date_2 = datetime.datetime.now()

        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()

        print(total_seconds)

    @staticmethod
    def select_faces_fast(context):
        date_1 = datetime.datetime.now()
        print("Start")

        pi = 3.14159265
        maxAngle = bpy.context.scene.max_angle
        print(maxAngle)

        obj = bpy.context.active_object

        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)
           
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]


        tabPoly = []
        tabNormalX = []
        tabNormalY = []
        tabNormalZ = []
        tabFaces = []

        tabPoint1X = []
        tabPoint1Y = []
        tabPoint2X = []
        tabPoint2Y = []
        tabPoint3X = []
        tabPoint3Y = []
        tabPoint1Z = []
        tabPoint2Z = []
        tabPoint3Z = []

        for poly in obj.data.polygons:
            tabPoly.append(poly.index)
            tabNormalX.append(poly.normal[0])
            tabNormalY.append(poly.normal[1])
            tabNormalZ.append(poly.normal[2])
            tabFaces.append(0)
            
            tabPoint1X.append(tabVertices[poly.vertices[0]].x)
            tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
            tabPoint2X.append(tabVertices[poly.vertices[1]].x)
            tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
            tabPoint3X.append(tabVertices[poly.vertices[2]].x)
            tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
            tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
            tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        print(len(tabPoly))   

        functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")


        seq = ctypes.c_int * len(tabPoly)
        arrIndex = seq(*tabPoly)

        seq = ctypes.c_float * len(tabNormalX)
        arrNormalX = seq(*tabNormalX)
        seq = ctypes.c_float * len(tabNormalY)
        arrNormalY = seq(*tabNormalY)
        seq = ctypes.c_float * len(tabNormalZ)
        arrNormalZ = seq(*tabNormalZ)

        seq = ctypes.c_int * len(tabFaces)
        arrFaces = seq(*tabFaces)

        seq = ctypes.c_float * len(tabPoint1X)
        arrPoint1X = seq(*tabPoint1X)
        seq = ctypes.c_float * len(tabPoint1Y)
        arrPoint1Y = seq(*tabPoint1Y)
        seq = ctypes.c_float * len(tabPoint2X)
        arrPoint2X = seq(*tabPoint2X)
        seq = ctypes.c_float * len(tabPoint2Y)
        arrPoint2Y = seq(*tabPoint2Y)
        seq = ctypes.c_float * len(tabPoint3X)
        arrPoint3X = seq(*tabPoint3X)
        seq = ctypes.c_float * len(tabPoint3Y)
        arrPoint3Y = seq(*tabPoint3Y)
        seq = ctypes.c_float * len(tabPoint1Z)
        arrPoint1Z = seq(*tabPoint1Z)
        seq = ctypes.c_float * len(tabPoint2Z)
        arrPoint2Z = seq(*tabPoint2Z)
        seq = ctypes.c_float * len(tabPoint3Z)
        arrPoint3Z = seq(*tabPoint3Z)

        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))
        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
    
    @staticmethod
    def generate_support(context):
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
    
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

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the support object
        bpy.data.objects[nameObject[0] + ".001"].select_set(True)
        bpy.data.objects[nameObject[0]].select_set(False)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        #bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the base object
        bpy.data.objects[nameObject[0] + ".001"].select_set(False)
        bpy.data.objects[nameObject[0]].select_set(True)

        # Delete the base object
        bpy.ops.object.delete(use_global=False, confirm=False)

        # Export the stl file
        bpy.ops.export_mesh.stl(filepath=pathOut)

        # Select the support
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
        bpy.data.objects[nameObject[0] + ".001"].select_set(True)

        print("End Script")

    @staticmethod
    def generate_support_area(context):
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

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Set support as active pbject
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]

        # Delete the base object
        object_to_delete = bpy.data.objects[nameObject[0]]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Unselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # Load mesh
        bm = bmesh.from_edit_mesh(bpy.context.selected_objects[0].data)
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

        # Set final support as active pbject
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".002"]

        # Delete the temp support
        object_to_delete = bpy.data.objects[nameObject[0] + ".001"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Export the stl file
        bpy.ops.export_mesh.stl(filepath=pathOut)

        print("End Script")

    @staticmethod
    def separate_faces(context):
                # Find the stl files
        txtfiles = []
        for file in glob.glob("C:/Gaetan/_Bachelor/blender/blenderScript/test/*.stl"):
            txtfiles.append(file)
        # Choose the first stl file
        pathIn = txtfiles[0]
        print(txtfiles[0])

        # Find the name of the object
        nameTemp = pathIn.split("\\")
        print(nameTemp[1])
        nameObject = nameTemp[1].split(".")
        print(nameObject[0])

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Set support as active pbject
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]

        # Delete the base object
        object_to_delete = bpy.data.objects[nameObject[0]]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

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
        bm = bmesh.from_edit_mesh(bpy.context.selected_objects[0].data)
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
    def generate_support_area_2(context): 
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

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Set final support as active pbject
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".002"]

        # Delete the temp support
        object_to_delete = bpy.data.objects[nameObject[0] + ".001"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True)

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        #bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Export the stl file
        bpy.ops.export_mesh.stl(filepath=pathOut)

        print("End Script")
 
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
    def mold(context): 
        obj = bpy.context.active_object
        moldOffset = obj.offset
    
        nameCopy = "temp_copy"

        nameObject = bpy.context.active_object.name

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        tabSelection = []
        for poly in obj.data.polygons:
            if poly.select:
                tabSelection.append(poly.index)
                print(poly.index)

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

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Cut the faces above the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=False, clear_outer=True, xstart=60, xend=424, ystart=126, yend=224, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select faces below 89°
        ########################
        date_1 = datetime.datetime.now()
        print("Start")

        pi = 3.14159265
        maxAngle = 89

        tabVertices = []
        obj = bpy.context.active_object
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)
           
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]


        tabPoly = []
        tabNormalX = []
        tabNormalY = []
        tabNormalZ = []
        tabFaces = []

        tabPoint1X = []
        tabPoint1Y = []
        tabPoint2X = []
        tabPoint2Y = []
        tabPoint3X = []
        tabPoint3Y = []
        tabPoint1Z = []
        tabPoint2Z = []
        tabPoint3Z = []

        for poly in obj.data.polygons:
            tabPoly.append(poly.index)
            tabNormalX.append(poly.normal[0])
            tabNormalY.append(poly.normal[1])
            tabNormalZ.append(poly.normal[2])
            tabFaces.append(0)
            
            tabPoint1X.append(tabVertices[poly.vertices[0]].x)
            tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
            tabPoint2X.append(tabVertices[poly.vertices[1]].x)
            tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
            tabPoint3X.append(tabVertices[poly.vertices[2]].x)
            tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
            tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
            tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        print(len(tabPoly))  
        maxFacesMold = len(tabPoly)

        functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")


        seq = ctypes.c_int * len(tabPoly)
        arrIndex = seq(*tabPoly)

        seq = ctypes.c_float * len(tabNormalX)
        arrNormalX = seq(*tabNormalX)
        seq = ctypes.c_float * len(tabNormalY)
        arrNormalY = seq(*tabNormalY)
        seq = ctypes.c_float * len(tabNormalZ)
        arrNormalZ = seq(*tabNormalZ)

        seq = ctypes.c_int * len(tabFaces)
        arrFaces = seq(*tabFaces)

        seq = ctypes.c_float * len(tabPoint1X)
        arrPoint1X = seq(*tabPoint1X)
        seq = ctypes.c_float * len(tabPoint1Y)
        arrPoint1Y = seq(*tabPoint1Y)
        seq = ctypes.c_float * len(tabPoint2X)
        arrPoint2X = seq(*tabPoint2X)
        seq = ctypes.c_float * len(tabPoint2Y)
        arrPoint2Y = seq(*tabPoint2Y)
        seq = ctypes.c_float * len(tabPoint3X)
        arrPoint3X = seq(*tabPoint3X)
        seq = ctypes.c_float * len(tabPoint3Y)
        arrPoint3Y = seq(*tabPoint3Y)
        seq = ctypes.c_float * len(tabPoint1Z)
        arrPoint1Z = seq(*tabPoint1Z)
        seq = ctypes.c_float * len(tabPoint2Z)
        arrPoint2Z = seq(*tabPoint2Z)
        seq = ctypes.c_float * len(tabPoint3Z)
        arrPoint3Z = seq(*tabPoint3Z)

        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))

        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
        ########################

        # Extrude the selected faces to the high 
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, 10), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        #bpy.ops.mesh.select_all(action='SELECT')

        # Get the outline at the level of the plane xy
        #bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=True, xstart=201, xend=793, ystart=341, yend=409, flip=False)

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Add the mold
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0),rotation=(3.14159, 0, 0), scale=(1, 1, 1))

        # Margins x and y
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
        #bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Join the object and the mold
        bpy.ops.object.join()

        # Recover the name
        obj.name = nameObject
        
        # Select faces
        ########################
        date_1 = datetime.datetime.now()
        print("Start")

        pi = 3.14159265
        maxAngle = bpy.context.scene.max_angle
        print(maxAngle)

        obj = bpy.context.active_object

        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)
           
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]


        tabPoly = []
        tabNormalX = []
        tabNormalY = []
        tabNormalZ = []
        tabFaces = []

        tabPoint1X = []
        tabPoint1Y = []
        tabPoint2X = []
        tabPoint2Y = []
        tabPoint3X = []
        tabPoint3Y = []
        tabPoint1Z = []
        tabPoint2Z = []
        tabPoint3Z = []
        
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')        
        
        print(len(tabPoly))   

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        for poly in obj.data.polygons:
            #if poly.center[2] == 0:
                #poly.select = True
            #else:
            tabPoly.append(poly.index)
            tabNormalX.append(poly.normal[0])
            tabNormalY.append(poly.normal[1])
            tabNormalZ.append(poly.normal[2])
            tabFaces.append(0)
            
            tabPoint1X.append(tabVertices[poly.vertices[0]].x)
            tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
            tabPoint2X.append(tabVertices[poly.vertices[1]].x)
            tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
            tabPoint3X.append(tabVertices[poly.vertices[2]].x)
            tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
            tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
            tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")

        seq = ctypes.c_int * len(tabPoly)
        arrIndex = seq(*tabPoly)

        seq = ctypes.c_float * len(tabNormalX)
        arrNormalX = seq(*tabNormalX)
        seq = ctypes.c_float * len(tabNormalY)
        arrNormalY = seq(*tabNormalY)
        seq = ctypes.c_float * len(tabNormalZ)
        arrNormalZ = seq(*tabNormalZ)

        seq = ctypes.c_int * len(tabFaces)
        arrFaces = seq(*tabFaces)

        seq = ctypes.c_float * len(tabPoint1X)
        arrPoint1X = seq(*tabPoint1X)
        seq = ctypes.c_float * len(tabPoint1Y)
        arrPoint1Y = seq(*tabPoint1Y)
        seq = ctypes.c_float * len(tabPoint2X)
        arrPoint2X = seq(*tabPoint2X)
        seq = ctypes.c_float * len(tabPoint2Y)
        arrPoint2Y = seq(*tabPoint2Y)
        seq = ctypes.c_float * len(tabPoint3X)
        arrPoint3X = seq(*tabPoint3X)
        seq = ctypes.c_float * len(tabPoint3Y)
        arrPoint3Y = seq(*tabPoint3Y)
        seq = ctypes.c_float * len(tabPoint1Z)
        arrPoint1Z = seq(*tabPoint1Z)
        seq = ctypes.c_float * len(tabPoint2Z)
        arrPoint2Z = seq(*tabPoint2Z)
        seq = ctypes.c_float * len(tabPoint3Z)
        arrPoint3Z = seq(*tabPoint3Z)

        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))
        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
        ########################
        
        tabPlane = []
        tabPlane2 = []
        #tm
        for poly in obj.data.polygons:
            if poly.select:
                tabPlane.append(poly)
                tabPlane2.append(poly.index)
                print(poly.index)
                
        #tm  
                
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #for poly in tabPlane:
        #    poly.select = True
        
        # Second turn
        ########################
        date_1 = datetime.datetime.now()
        print("Start")

        pi = 3.14159265
        maxAngle = bpy.context.scene.max_angle
        print(maxAngle)

        obj = bpy.context.active_object

        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)
           
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]


        tabPoly = []
        tabNormalX = []
        tabNormalY = []
        tabNormalZ = []
        tabFaces = []

        tabPoint1X = []
        tabPoint1Y = []
        tabPoint2X = []
        tabPoint2Y = []
        tabPoint3X = []
        tabPoint3Y = []
        tabPoint1Z = []
        tabPoint2Z = []
        tabPoint3Z = []
        
        #bpy.ops.object.mode_set(mode='EDIT')
        #bpy.ops.mesh.select_all(action='DESELECT')
        #bpy.ops.object.mode_set(mode='OBJECT')        
        
        print(len(tabPoly))   
        
        #bpy.ops.object.mode_set(mode = 'EDIT')
        #bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 
        
        for poly in obj.data.polygons:
            #if poly.center[2] == 0:
                #poly.select = True
            #else:
            if poly.center[2] > (0-0.01) and poly.center[2] < (0+0.01):
                #poly.select = False
                print("SALUT",poly.index)

            else:
                #poly.select = False
                tabPoly.append(poly.index)
                tabNormalX.append(poly.normal[0])
                tabNormalY.append(poly.normal[1])
                tabNormalZ.append(poly.normal[2])
                tabFaces.append(0)
                
                tabPoint1X.append(tabVertices[poly.vertices[0]].x)
                tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
                tabPoint2X.append(tabVertices[poly.vertices[1]].x)
                tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
                tabPoint3X.append(tabVertices[poly.vertices[2]].x)
                tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
                tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
                tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
                tabPoint3Z.append(tabVertices[poly.vertices[2]].z)
        
        functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")

        seq = ctypes.c_int * len(tabPoly)
        arrIndex = seq(*tabPoly)

        seq = ctypes.c_float * len(tabNormalX)
        arrNormalX = seq(*tabNormalX)
        seq = ctypes.c_float * len(tabNormalY)
        arrNormalY = seq(*tabNormalY)
        seq = ctypes.c_float * len(tabNormalZ)
        arrNormalZ = seq(*tabNormalZ)

        seq = ctypes.c_int * len(tabFaces)
        arrFaces = seq(*tabFaces)

        seq = ctypes.c_float * len(tabPoint1X)
        arrPoint1X = seq(*tabPoint1X)
        seq = ctypes.c_float * len(tabPoint1Y)
        arrPoint1Y = seq(*tabPoint1Y)
        seq = ctypes.c_float * len(tabPoint2X)
        arrPoint2X = seq(*tabPoint2X)
        seq = ctypes.c_float * len(tabPoint2Y)
        arrPoint2Y = seq(*tabPoint2Y)
        seq = ctypes.c_float * len(tabPoint3X)
        arrPoint3X = seq(*tabPoint3X)
        seq = ctypes.c_float * len(tabPoint3Y)
        arrPoint3Y = seq(*tabPoint3Y)
        seq = ctypes.c_float * len(tabPoint1Z)
        arrPoint1Z = seq(*tabPoint1Z)
        seq = ctypes.c_float * len(tabPoint2Z)
        arrPoint2Z = seq(*tabPoint2Z)
        seq = ctypes.c_float * len(tabPoint3Z)
        arrPoint3Z = seq(*tabPoint3Z)

        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))
        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End 2")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
        ########################
        
        bpy.ops.object.mode_set(mode = 'OBJECT')
        #tm
        obj = bpy.context.active_object
        for poly in tabPlane:
        #    poly.select = True
            print(poly.index)
            print(tabPlane2[0])
            obj.data.polygons[tabPlane2[0]].select = True
            tabPlane2.pop(0)
        print("TM")
        #tm
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
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

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the support object
        bpy.data.objects[nameObject[0] + ".001"].select_set(True)
        bpy.data.objects[nameObject[0]].select_set(False)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

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

        # Select the base object
        bpy.data.objects[nameObject[0] + ".001"].select_set(False)
        bpy.data.objects[nameObject[0]].select_set(True)

        # Delete the base object
        bpy.ops.object.delete(use_global=False, confirm=False)

        # Export the stl file
        bpy.ops.export_mesh.stl(filepath=pathOut)

        # Select the support
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
        bpy.data.objects[nameObject[0] + ".001"].select_set(True)

        # Add the bottom
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, moldOffset-0.2), scale=(1,1,1))
        bpy.data.objects["Cube"].dimensions = [bpy.data.objects[nameObject[0] + ".001"].dimensions[0], bpy.data.objects[nameObject[0] + ".001"].dimensions[1], 0.4]
        # Align the mold in Z
        #bpy.ops.object.align(align_mode='OPT_3', relative_to='OPT_1', align_axis={'Z'})

        # Select the copy
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject[0] + ".001"]
        bpy.data.objects[nameObject[0] + ".001"].select_set(True)

        # Align the mold in x and y
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_4', align_axis={'Y'})

        bpy.ops.object.join()
        
        print("End Script")
         

    sizeX = 0
    oldResize = 1

    @staticmethod
    def select_resize(context):
        date_1 = datetime.datetime.now()
        print("Start")

        xMax = float('-inf')
        xMin = float('inf')
        
        pi = 3.14159265
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
                    angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))*180/pi
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
        
        global sizeX
        sizeX = xMax-xMin
        global oldResize
        oldResize = 1
                        
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
        
        global sizeX
        sizeX = xMax-xMin
        global oldResize
        oldResize = 1
                        
        bmesh.update_edit_mesh(me)

        print("End Script")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print("Time : ", total_seconds)
        
    @staticmethod
    def resize(context):
        global sizeX
        global oldResize
        print(sizeX)
        print(oldResize)
        scaleX = 1/oldResize
        bpy.ops.transform.resize(value=(scaleX, scaleX, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

        scaleX = 1+(2*bpy.context.scene.resize/sizeX)
        if scaleX < 0:
            scaleX = 1
        print(scaleX)
        oldResize = scaleX
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
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = False

    @staticmethod
    def validate(context):
        bpy.ops.object.apply_all_modifiers()

    @staticmethod
    def manifold(context):
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

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

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

        pi = 3.14159265
        maxAngle = 10

        obj = bpy.context.active_object

        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)
           
        tabDirVec = [[mathutils.Vector((0,0,-1)), mathutils.Vector((0,-1,0)), mathutils.Vector((0,0,1)),mathutils.Vector((0,1,0))], 
                     [mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)), mathutils.Vector((1,0,0)),mathutils.Vector((1,0,0))], 
                     [mathutils.Vector((0,0,1)), mathutils.Vector((0,1,0)), mathutils.Vector((0,0,-1)),mathutils.Vector((0,-1,0))], 
                     [mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)), mathutils.Vector((-1,0,0)),mathutils.Vector((-1,0,0))]]
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)]

        tabPoly = []
        tabNormalX = []
        tabNormalY = []
        tabNormalZ = []
        tabFaces = []

        tabPoint1X = []
        tabPoint1Y = []
        tabPoint2X = []
        tabPoint2Y = []
        tabPoint3X = []
        tabPoint3Y = []
        tabPoint1Z = []
        tabPoint2Z = []
        tabPoint3Z = []

        for poly in obj.data.polygons:
            tabPoly.append(poly.index)
            tabNormalX.append(poly.normal[0])
            tabNormalY.append(poly.normal[1])
            tabNormalZ.append(poly.normal[2])
            tabFaces.append(0)
            
            tabPoint1X.append(tabVertices[poly.vertices[0]].x)
            tabPoint1Y.append(tabVertices[poly.vertices[0]].y)
            tabPoint2X.append(tabVertices[poly.vertices[1]].x)
            tabPoint2Y.append(tabVertices[poly.vertices[1]].y)
            tabPoint3X.append(tabVertices[poly.vertices[2]].x)
            tabPoint3Y.append(tabVertices[poly.vertices[2]].y)
            tabPoint1Z.append(tabVertices[poly.vertices[0]].z)
            tabPoint2Z.append(tabVertices[poly.vertices[1]].z)
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        print(len(tabPoly))   

        functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")


        seq = ctypes.c_int * len(tabPoly)
        arrIndex = seq(*tabPoly)

        seq = ctypes.c_float * len(tabNormalX)
        arrNormalX = seq(*tabNormalX)
        seq = ctypes.c_float * len(tabNormalY)
        arrNormalY = seq(*tabNormalY)
        seq = ctypes.c_float * len(tabNormalZ)
        arrNormalZ = seq(*tabNormalZ)

        seq = ctypes.c_int * len(tabFaces)
        arrFaces = seq(*tabFaces)

        seq = ctypes.c_float * len(tabPoint1X)
        arrPoint1X = seq(*tabPoint1X)
        seq = ctypes.c_float * len(tabPoint1Y)
        arrPoint1Y = seq(*tabPoint1Y)
        seq = ctypes.c_float * len(tabPoint2X)
        arrPoint2X = seq(*tabPoint2X)
        seq = ctypes.c_float * len(tabPoint2Y)
        arrPoint2Y = seq(*tabPoint2Y)
        seq = ctypes.c_float * len(tabPoint3X)
        arrPoint3X = seq(*tabPoint3X)
        seq = ctypes.c_float * len(tabPoint3Y)
        arrPoint3Y = seq(*tabPoint3Y)
        seq = ctypes.c_float * len(tabPoint1Z)
        arrPoint1Z = seq(*tabPoint1Z)
        seq = ctypes.c_float * len(tabPoint2Z)
        arrPoint2Z = seq(*tabPoint2Z)
        seq = ctypes.c_float * len(tabPoint3Z)
        arrPoint3Z = seq(*tabPoint3Z)

        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.object.mode_set(mode = 'OBJECT')

        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))
        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
        
        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        #bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
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

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
      
        # Delete the copy
        object_to_delete = bpy.data.objects["temp_copy"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True) 
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
            
    @staticmethod
    def test_import(context):
        bpy.ops.stl_file.import_file('INVOKE_DEFAULT')   
        
    @staticmethod
    def test_export(context):
        bpy.ops.stl_file.export_file('INVOKE_DEFAULT')

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
        self.filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'} 
 
    def execute(self, context):
        print('Imported file: ', self.filepath)
        
        # Import the stl file
        bpy.ops.import_mesh.stl(filepath = self.filepath)
        
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
            nameSupport =  bpy.context.active_object.name + "_support"
        else:
            nameSupport = "support"
          
        self.filepath = "C://Gaetan//_Bachelor//blender//blenderScript//test//" + nameSupport + ".stl"
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
        
    def execute(self, context):
        print('Exported file: ', self.filepath)
        
        # Export the stl file
        bpy.ops.export_mesh.stl(filepath = self.filepath)
        
        return {'FINISHED'}
 

#get, set methods of the floatproperty
#def get_location(self):
#    return self.get("resize", 0.0)

#scaleOldX = 1
    
#def set_location(self, value):
#    sizeX = 0.6
#    global scaleOldX
    
#    self["resize"] = value
#    scaleX = 1/scaleOldX
#    bpy.ops.transform.resize(value=(scaleX, scaleX, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

#    scaleOldX = value
#    bpy.ops.transform.resize(value=(value, value, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)


    # Switch in the edit mode
#    bpy.ops.object.mode_set(mode = 'EDIT')  
    
def register():
    pi = 3.14159265
    
    # create personal properties
    bpy.types.Scene.max_angle = bpy.props.FloatProperty(name="Max Angle", default = 45, options={'SKIP_SAVE'}, min = 0, max = 90,soft_min = 0, soft_max = 90, step = 100)
    bpy.types.Scene.min_area = bpy.props.FloatProperty(name="Min Area", default = 0.1, options={'SKIP_SAVE'}, min = 0, max = 1, soft_min = 0, soft_max = 1, step = 1)
    bpy.types.Object.offset = bpy.props.FloatProperty(name = "Offset", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 100)
    bpy.types.Scene.resize = bpy.props.FloatProperty(name = "Resize", default = 0, options={'SKIP_SAVE'}, min = -10, max = 10, soft_min = -10, soft_max = 10, step = 1)#,get=get_location, set=set_location)
    bpy.types.Scene.min_angle_z = bpy.props.FloatProperty(name="Min Angle z", default = 90, options={'SKIP_SAVE'}, min = 0, max = 181,soft_min = 0, soft_max = 181, step = 100)
    bpy.types.Scene.max_angle_z = bpy.props.FloatProperty(name="Max Angle z", default = 90, options={'SKIP_SAVE'}, min = 0, max = 181,soft_min = 0, soft_max = 181, step = 100)
    bpy.types.Scene.voxel_size = bpy.props.FloatProperty(name="Voxel Size", default = 0.01, options={'SKIP_SAVE'}, min = 0.01, max = 0.1,soft_min = 0.01, soft_max = 0.1, step = 1)
    bpy.types.Scene.decimate_ratio = bpy.props.FloatProperty(name="Decimate Ratio", default = 0.01, options={'SKIP_SAVE'}, min = 0, max = 1,soft_min = 0, soft_max = 1, step = 1)
    bpy.types.Scene.volume = bpy.props.FloatProperty(name="Volume", default = 0, options={'SKIP_SAVE'}, min = 0, step = 100)
    bpy.types.Scene.level_blocks = bpy.props.IntProperty(name="Level Blocks", default = 5, options={'SKIP_SAVE'}, min = 1, max = 9,soft_min = 1, soft_max = 9, step = 1)
    
    # register all the classes
    register_class(STL_FILE_import)
    register_class(STL_FILE_export)
   
    register_class(BUTTON_OT_button_op)
    register_class(BUTTON_PT_rotation)
    register_class(BUTTON_PT_generation)
    register_class(BUTTON_PT_area)
    register_class(BUTTON_PT_offset)
    register_class(BUTTON_PT_resize)
    register_class(BUTTON_PT_voxel)
    register_class(BUTTON_PT_import_export)
 
 
def unregister():
    # delete personal properties
    del bpy.types.Scene.max_angle
    del bpy.types.Scene.min_area
    del bpy.types.Object.offset
    del bpy.types.Scene.resize
    del bpy.types.Scene.min_angle_z
    del bpy.types.Scene.max_angle_z
    del bpy.types.Scene.voxel_size
    del bpy.types.Scene.decimate_ratio
    del bpy.types.Scene.volume
    del bpy.types.Scene.level_blocks
    
    # unregister all the classes
    unregister_class(STL_FILE_import)
    unregister_class(STL_FILE_export)
    
    unregister_class(BUTTON_OT_button_op)
    unregister_class(BUTTON_PT_rotation)
    unregister_class(BUTTON_PT_generation)
    unregister_class(BUTTON_PT_area)
    unregister_class(BUTTON_PT_offset)
    unregister_class(BUTTON_PT_resize)
    unregister_class(BUTTON_PT_voxel)
    unregister_class(BUTTON_PT_import_export)
 
 
if __name__ == '__main__':
    register()