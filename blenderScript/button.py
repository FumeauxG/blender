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
 
class ROTATION_PT_panel(Panel):
    bl_idname = 'Rotation_PT_panel'
    bl_label = 'Rotation Object'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Rotation'
 
    def draw(self, context):
        layout = self.layout
        layout.operator('rot.rot_op', text='Rotation x').action = 'ROTX'
        layout.operator('rot.rot_op', text='Rotation y').action = 'ROTY'
        layout.operator('rot.rot_op', text='Rotation z').action = 'ROTZ'
        
        scene = context.scene
        box = layout.box()
        row = box.row()
        row.prop(scene, "max_angle")
        
        layout.operator('rot.rot_op', text='Import object').action = 'IMPORT'
        layout.operator('rot.rot_op', text='Select faces').action = 'SELECT'
        layout.operator('rot.rot_op', text='Generate support').action = 'GENERATE'

class ROTATION_OT_rotation_op(Operator):
    bl_idname = 'rot.rot_op'
    bl_label = 'Rotation'
    bl_description = 'Rotation'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('ROTX', 'rotation x', 'rotation x'),
            ('ROTY', 'rotation y', 'rotation y'),
            ('ROTZ', 'rotation z', 'rotation z'),
            ('IMPORT', 'Import object', 'Import object'),
            ('SELECT', 'Select faces', 'Select faces'),
            ('GENERATE', 'Generate support', 'Generate support')
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
        elif self.action == 'GENERATE':   
            self.generate_support(context=context)
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
        vecDir = tabDirVec[int((bpy.context.selected_objects[0].rotation_euler[0]) * 180/pi/90)][int((bpy.context.selected_objects[0].rotation_euler[1]) * 180/pi/90)]
        
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
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

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

def updateAngle(self, context):
    maxAngle = self.max_angle
    print(maxAngle)

 
def register():
    pi = 3.14159265
    bpy.types.Scene.max_angle = bpy.props.FloatProperty(name="Max Angle", default = 45, options={'SKIP_SAVE'}, min = 0, max = 90, step = 100)#, update = updateAngle)

    register_class(ROTATION_OT_rotation_op)
    register_class(ROTATION_PT_panel)
 
 
def unregister():
    del bpy.types.Scene.max_angle
    unregister_class(ROTATION_OT_rotation_op)
    unregister_class(ROTATION_PT_panel)
 
 
if __name__ == '__main__':
    register()