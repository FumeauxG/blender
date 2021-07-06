import bpy

class Get_And_Set_Rotation():
    def get_angle_x(self):
        return self.get("angle_x", 0.0)    
    def set_angle_x(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        obj = bpy.context.active_object

        # Save the old value of the angle
        oldValue = bpy.context.scene.angle_x
        
        # Update the value of the angle
        self["angle_x"] = value
     
        # Modify the angle
        obj.rotation_euler[0] = value-oldValue
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})

        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT') 

    def get_angle_y(self):
        return self.get("angle_y", 0.0)  
    def set_angle_y(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        obj = bpy.context.active_object

        # Save the old value of the angle
        oldValue = bpy.context.scene.angle_y
        
        # Update the value of the angle
        self["angle_y"] = value
     
        # Modify the angle
        obj.rotation_euler[1] = value-oldValue
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})
        
        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

    def get_angle_z(self):
        return self.get("angle_z", 0.0)       
    def set_angle_z(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        obj = bpy.context.active_object

        # Save the old value of the angle
        oldValue = bpy.context.scene.angle_z
        
        # Update the value of the angle
        self["angle_z"] = value
     
        # Modify the angle
        obj.rotation_euler[2] = value-oldValue
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})

        # Apply rotation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True) 

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        


class Get_And_Set_Lattice():
    def get_lattice_size_x(self):
        return self.get("lattice_size_x", 0.0)    
    def set_lattice_size_x(self, value):
        self["lattice_size_x"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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
                
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     
    def get_lattice_size_y(self):
        return self.get("lattice_size_y", 0.0)   
    def set_lattice_size_y(self, value):
        self["lattice_size_y"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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
                
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     
    def get_lattice_size_z(self):
        return self.get("lattice_size_z", 0.0)
    def set_lattice_size_z(self, value):
        self["lattice_size_z"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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
                
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     

    def get_lattice_offset_x(self):
        return self.get("lattice_offset_x", 0.0)
    def set_lattice_offset_x(self, value):
        self["lattice_offset_x"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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

        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)

    def get_lattice_offset_y(self):
        return self.get("lattice_offset_y", 0.0)
    def set_lattice_offset_y(self, value):
        self["lattice_offset_y"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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

        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
        
    def get_lattice_offset_z(self):
        return self.get("lattice_offset_z", 0.0)
    def set_lattice_offset_z(self, value):
        self["lattice_offset_z"] = value

        obj = bpy.context.active_object

        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')   
        for vertex in obj.data.vertices:
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

        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     