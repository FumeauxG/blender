bl_info = {
    "name": "Rotation Object",
    "description": "Rotate the selected object",
    "author": "Fumeaux Gaëtan",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "category": "Object",
}

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
 
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

class ROTATION_OT_rotation_op(Operator):
    bl_idname = 'rot.rot_op'
    bl_label = 'Rotation'
    bl_description = 'Rotation'
    bl_options = {'REGISTER', 'UNDO'}
 
    action: EnumProperty(
        items=[
            ('ROTX', 'rotation x', 'rotation x'),
            ('ROTY', 'rotation y', 'rotation y'),
            ('ROTZ', 'rotation z', 'rotation z')
        ]
    )
 
    def execute(self, context):
        if self.action == 'ROTX':
            self.rot_x(context=context)
        elif self.action == 'ROTY':
            self.rot_y(context=context)
        elif self.action == 'ROTZ':
            self.rot_z(context=context)
        return {'FINISHED'}
    
    
    @staticmethod
    def rot_x(context):
        pi = 3.14159265

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
 
    @staticmethod
    def rot_y(context):
        pi = 3.14159265

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
 
    @staticmethod
    def rot_z(context):
        pi = 3.14159265

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
 
def register():
    register_class(ROTATION_OT_rotation_op)
    register_class(ROTATION_PT_panel)
 
 
def unregister():
    unregister_class(ROTATION_OT_rotation_op)
    unregister_class(ROTATION_PT_panel)
 
 
if __name__ == '__main__':
    register()