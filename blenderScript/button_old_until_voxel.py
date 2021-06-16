bl_info = {
    "name": "Button",
    "description": "Button",
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

 
class BUTTON_PT_panel(Panel):
    bl_idname = 'BUTTON_PT_panel'
    bl_label = 'Button Controller'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Button'
    test = "Salut"
 
    def draw(self, context):
        layout = self.layout
        layout.operator('btn.btn_op', text='Rotation x').action = 'ROTX'
        layout.operator('btn.btn_op', text='Rotation y').action = 'ROTY'
        layout.operator('btn.btn_op', text='Rotation z').action = 'ROTZ'
        
        layout.separator()
        
        scene = context.scene
        box1 = layout.box()
        row = box1.row()
        row.prop(scene, "max_angle")
        
        layout.operator('btn.btn_op', text='Import object').action = 'IMPORT'
        layout.operator('btn.btn_op', text='Select faces').action = 'SELECT'
        layout.operator('btn.btn_op', text='Select faces fast').action = 'SELECTFAST'
        layout.operator('btn.btn_op', text='Generate support').action = 'GENERATE'
        
        #----------------------------
        layout.separator()
        layout.label(text="Beta area")
        
        box2 = layout.box()
        row = box2.row()
        row.prop(scene, "min_area")
        
        layout.operator('btn.btn_op', text='Generate support (area)').action = 'GENERATE_AREA'
        
        layout.operator('btn.btn_op', text='Separate faces').action = 'SEPARATE'
        layout.operator('btn.btn_op', text='Select faces 2').action = 'SELECT2'
        layout.operator('btn.btn_op', text='Generate support (area2)').action = 'GENERATE_AREA_2'
        
        #----------------------------
        layout.separator()
        layout.label(text="Beta offset")
        
        box3 = layout.box()
        row = box3.row()
        row.prop(context.object, "offset")
        layout.operator('btn.btn_op', text='Offset').action = 'OFFSET'
        
        #----------------------------
        layout.separator()
        layout.label(text="Beta resize")

        layout.operator('btn.btn_op', text='Select resize').action = 'SELECT_RESIZE'
        box4 = layout.box()
        row = box4.row()
        row.prop(scene, "min_angle_z")  
        row.prop(scene, "max_angle_z")  
        layout.operator('btn.btn_op', text='Select resize all').action = 'SELECT_RESIZE_ALL'        

        box5 = layout.box()
        row = box5.row()
        row.prop(scene, "resize")  
        layout.operator('btn.btn_op', text='Resize').action = 'RESIZE' 
        
        #----------------------------
        layout.separator()
        layout.label(text="Beta voxel")
        
        layout.operator('btn.btn_op', text='Voxel').action = 'VOXEL'
        layout.operator('btn.btn_op', text='Decimate').action = 'DECIMATE'
        layout.operator('btn.btn_op', text='Manifold').action = 'MANIFOLD'

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
            ('SELECT_RESIZE', 'Select resize', 'Select resize'),
            ('SELECT_RESIZE_ALL', 'Select resize all', 'Select resize all'),
            ('RESIZE', 'Resize', 'Resize'),
            ('VOXEL', 'Voxel', 'Voxel'),
            ('DECIMATE', 'Decimate', 'Decimate'),
            ('MANIFOLD', 'Manifold', 'Manifold')
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
        elif self.action == 'SELECT_RESIZE':   
            self.select_resize(context=context) 
        elif self.action == 'SELECT_RESIZE_ALL':   
            self.select_resize_all(context=context) 
        elif self.action == 'RESIZE':   
            self.resize(context=context) 
        elif self.action == 'VOXEL':   
            self.voxel(context=context)
        elif self.action == 'DECIMATE':   
            self.decimate(context=context)
        elif self.action == 'MANIFOLD':   
            self.manifold(context=context)
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

        # Select faces visible from camera
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

        # Select the support object
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

        scaleX = 1-(2*bpy.context.scene.resize/sizeX)
        if scaleX < 0:
            scaleX = 1
        print(scaleX)
        oldResize = scaleX
        bpy.ops.transform.resize(value=(scaleX, scaleX, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

    @staticmethod
    def voxel(context):
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Remesh the object with voxels
        bpy.ops.object.modifier_add(type='REMESH')
        bpy.context.object.modifiers["Remesh"].mode = 'VOXEL'
        bpy.context.object.modifiers["Remesh"].voxel_size = 0.01
        bpy.context.object.modifiers["Remesh"].adaptivity = 0
        bpy.context.object.modifiers["Remesh"].use_smooth_shade = False
        bpy.ops.object.apply_all_modifiers()
        
    @staticmethod
    def decimate(context):
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Decimate the faces of the object
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].decimate_type = 'COLLAPSE'
        bpy.context.object.modifiers["Decimate"].ratio = 0.01
        bpy.context.object.modifiers["Decimate"].use_symmetry = False
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = False
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

    #scaleX = 1 - (2*
#    scaleOldX = value
#    bpy.ops.transform.resize(value=(value, value, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)


    # Switch in the edit mode
#    bpy.ops.object.mode_set(mode = 'EDIT')  
    
def register():
    pi = 3.14159265
    bpy.types.Scene.max_angle = bpy.props.FloatProperty(name="Max Angle", default = 45, options={'SKIP_SAVE'}, min = 0, max = 90,soft_min = 0, soft_max = 90, step = 100)
    bpy.types.Scene.min_area = bpy.props.FloatProperty(name="Min Area", default = 0.1, options={'SKIP_SAVE'}, min = 0, max = 1, soft_min = 0, soft_max = 1, step = 1)
    bpy.types.Object.offset = bpy.props.FloatProperty(name = "Offset", default = 0, options={'SKIP_SAVE'}, min = 0, max = 10, soft_min = 0, soft_max = 10, step = 100)
    bpy.types.Scene.resize = bpy.props.FloatProperty(name = "Resize", default = 0, options={'SKIP_SAVE'}, min = 0, max = 10, soft_min = 0, soft_max = 10, step = 1)#,get=get_location, set=set_location)
    bpy.types.Scene.min_angle_z = bpy.props.FloatProperty(name="Min Angle z", default = 90, options={'SKIP_SAVE'}, min = 0, max = 181,soft_min = 0, soft_max = 181, step = 100)
    bpy.types.Scene.max_angle_z = bpy.props.FloatProperty(name="Max Angle z", default = 90, options={'SKIP_SAVE'}, min = 0, max = 181,soft_min = 0, soft_max = 181, step = 100)
     
    register_class(BUTTON_OT_button_op)
    register_class(BUTTON_PT_panel)
 
 
def unregister():
    del bpy.types.Scene.max_angle
    del bpy.types.Scene.min_area
    del bpy.types.Object.offset
    del bpy.types.Scene.resize
    del bpy.types.Scene.min_angle_z
    del bpy.types.Scene.max_angle_z
    
    unregister_class(BUTTON_OT_button_op)
    unregister_class(BUTTON_PT_panel)
 
 
if __name__ == '__main__':
    register()