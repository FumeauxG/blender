import bpy

class Get_And_Set_Rotation():
    """      
    Getter and setter for the class of the angle x,y,z of the mesh
    """
    def get_angle_x(self):
        return self.get("angle_x", 0.0)    
    def set_angle_x(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Get the active object
        obj = bpy.context.active_object
        
        # Update the value of the angle
        self["angle_x"] = value
     
        # Set the euler mode
        obj.rotation_mode = 'XYZ'
     
        # Modify the angle
        obj.rotation_euler[0] = value
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'}) 
        # Apply the offset
        obj.location[2] = bpy.context.scene.offset + obj.location[2]
        
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        

    def get_angle_y(self):
        return self.get("angle_y", 0.0)  
    def set_angle_y(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Get the active object
        obj = bpy.context.active_object

        # Set the euler mode
        obj.rotation_mode = 'XYZ'
        
        # Update the value of the angle
        self["angle_y"] = value
     
        # Modify the angle
        obj.rotation_euler[1] = value
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'}) 
        # Apply the offset
        obj.location[2] = bpy.context.scene.offset + obj.location[2]
        
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')

    def get_angle_z(self):
        return self.get("angle_z", 0.0)       
    def set_angle_z(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Get the active object
        obj = bpy.context.active_object

        # Set the euler mode
        obj.rotation_mode = 'XYZ'
        
        # Update the value of the angle
        self["angle_z"] = value
     
        # Modify the angle
        obj.rotation_euler[2] = value
        
        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'}) 
        # Apply the offset
        obj.location[2] = bpy.context.scene.offset + obj.location[2]
        
        # Align in the center
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'X'})
        bpy.ops.object.align(align_mode='OPT_2', relative_to='OPT_1', align_axis={'Y'})

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        

class Get_And_Set_Offset():
    """      
    Getter and setter for the class of the offset of the mesh
    """
    def get_offset(self):
        return self.get("offset", 0.0)  
    def set_offset(self, value):
        # Switch in the object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        # Get the active object
        obj = bpy.context.active_object
        
        # Update the value of the offset
        self["offset"] = value

        # Align the object on the xy plane
        bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'}) 
        
        # Set the offset
        obj.location[2] = value + obj.location[2]

        # Switch in the edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')


class Get_And_Set_Lattice():
    """      
    Getter and setter for the class of the size and location of a lattice
    """  
    def get_lattice_size_x(self):
        return self.get("lattice_size_x", 0.0)    
    def set_lattice_size_x(self, value):
        # Update the value of the size x of the lattice
        self["lattice_size_x"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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
        
        # Set the size and the location of the lattice
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     
    def get_lattice_size_y(self):
        return self.get("lattice_size_y", 0.0)   
    def set_lattice_size_y(self, value):
        # Update the value of the size y of the lattice
        self["lattice_size_y"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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
         
        # Set the size and the location of the lattice         
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     
    def get_lattice_size_z(self):
        return self.get("lattice_size_z", 0.0)
    def set_lattice_size_z(self, value):
        # Update the value of the size z of the lattice
        self["lattice_size_z"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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
        
        # Set the size and the location of the lattice         
        bpy.data.objects["Lattice"].scale = (self["lattice_size_x"], self["lattice_size_y"], self["lattice_size_z"])
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     

    def get_lattice_offset_x(self):
        return self.get("lattice_offset_x", 0.0)
    def set_lattice_offset_x(self, value):
        # Update the value of the offset x of the lattice
        self["lattice_offset_x"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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

        # Set the location of the lattice   
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)

    def get_lattice_offset_y(self):
        return self.get("lattice_offset_y", 0.0)
    def set_lattice_offset_y(self, value):
        # Update the value of the offset y of the lattice 
        self["lattice_offset_y"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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

        # Set the location of the lattice  
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
        
    def get_lattice_offset_z(self):
        return self.get("lattice_offset_z", 0.0)
    def set_lattice_offset_z(self, value):
        # Update the value of the offset y of the lattice 
        self["lattice_offset_z"] = value

        # Get the active object
        obj = bpy.context.active_object

        # Find the max and min coordinate of the mesh
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

        # Set the location of the lattice 
        bpy.data.objects["Lattice"].location = (self["lattice_offset_x"]+xMoins+self["lattice_size_x"]/2, self["lattice_offset_y"]+yMoins+self["lattice_size_y"]/2, self["lattice_offset_z"]+zMoins+self["lattice_size_z"]/2)
     