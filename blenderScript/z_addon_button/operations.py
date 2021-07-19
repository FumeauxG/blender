from .getter_and_setter import *

import bpy
import mathutils
import bmesh

from math import pi
from math import radians
from math import sqrt

import datetime
import ctypes
import os


class Button_Operations():
    """      
    Class containin the action of the blender buttons
    """
    def m_to_mm():
        """      
        Change the Blender scale from metre to milimetre

        Note:
            None
        Args:
            None
        Returns:
            None
        """  
        # Set blender unit in mm
        bpy.context.scene.unit_settings.scale_length = 0.001
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'        

    def volume():
        """      
        Calculate the volume of the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Get the active object
        obj = bpy.context.active_object
        
        scene = bpy.context.scene
        unit = scene.unit_settings
        
        # Set blender unit in mm
        unit.scale_length = 0.001
        bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'       
        
        # Get the scale
        scale = 1.0 if unit.system == 'NONE' else unit.scale_length
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Load mesh
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

    def triangulate():
        """      
        Triangulate all the faces of the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')    
        
        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Triangulate the faces
        bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED_ALTERNATE', ngon_method='CLIP')

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')         


    def select_faces(maxAngle):
        """      
        Select the faces where the angle between the 
        downward vector and the normal is under the max angle value
        Then check there is no face under those faces

        Note:
            A mesh must be selected
        Args:
            maxAngle: float angle under the face is selected in radians
        Returns:
            None
        """
        date_1 = datetime.datetime.now()
        print("Start")

        print(maxAngle, maxAngle*180/pi)

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Get the active object
        obj = bpy.context.active_object

        # Add the vertices location in an array
        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)

        # Find the downward vector in function of the angles of the mesh
        matrix_new = obj.matrix_world.to_3x3().inverted()
        no_world = matrix_new @ mathutils.Vector((0,0,-1))
        no_world.normalize() 
        print(no_world)
        vecDir = no_world


        # Arrays for the function C parameters
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

        # Fill the arrays
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
            #tabPoint1Z.append(min(tabVertices[poly.vertices[0]].z, tabVertices[poly.vertices[1]].z,tabVertices[poly.vertices[2]].z))
            #tabPoint2Z.append(max(tabVertices[poly.vertices[0]].z, tabVertices[poly.vertices[1]].z,tabVertices[poly.vertices[2]].z))
            
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        print(len(tabPoly))   

        print(os.path.dirname(__file__))
        # Get the filepath of the dll file
        functionC = ctypes.CDLL(os.path.dirname(__file__) + "\\function.dll")

        # Create array for C function
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

        date_3 = datetime.datetime.now()
        
        # Call the C function
        functionC.select_faces(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

        date_4 = datetime.datetime.now()

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        # Deselect all the faces
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.mesh.select_mode(type="FACE")
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select all the faces needed support
        for i in range(len(arrFaces)):
            if arrFaces[i] == 1:
                obj.data.polygons[tabPoly[i]].select = True
        print(len(arrFaces))
        
        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        print("End")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print(total_seconds)
        
        time_delta = (date_4 - date_3)
        total_seconds = time_delta.total_seconds()
        print("C time : ", total_seconds)
    
    def generate_support():
        """ 
        Generate support for the selected faces:
        Separate and extrude selected faces
        Then bissect and cut faces under the plane xy 
        and delete the base object

        Note:
            Some faces must be selected
        Args:
            None
        Returns:
            None
        """
    
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')    # Allow to update the mesh if it has been modified
    
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get the active object
        obj = bpy.context.active_object
        
        # Get the name of the object
        nameObject = obj.name

        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the support object
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]
        bpy.data.objects[nameObject + ".001"].select_set(True)
        bpy.data.objects[nameObject].select_set(False)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        '''
        # Create new edit mode bmesh to easily acces mesh data
        me = bpy.context.object.data  # Get selected object's mesh
        bm = bmesh.from_edit_mesh(me) 

        # Select all vertices that have 1 or 2 links and deselect the others
        for v in bm.verts:
            v.select_set(len(v.link_edges) in (1,2))

        # Transfer the data back to the object's mesh
        bmesh.update_edit_mesh(me)
        '''
        # Delete the selected vertices
        bpy.ops.mesh.delete(type='VERT')
        
        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Select the base object
        bpy.data.objects[nameObject + ".001"].select_set(False)
        bpy.data.objects[nameObject].select_set(True)

        # Delete the base object
        bpy.ops.object.delete(use_global=False, confirm=False)

        # Select the support
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject + ".001"]
        bpy.data.objects[nameObject + ".001"].select_set(True)
        
        # Rename the support
        bpy.context.active_object.name = nameObject + "_support"

        # Apply location
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Init properties of angles and offset
        bpy.context.scene.angle_x = 0
        bpy.context.scene.angle_y = 0
        bpy.context.scene.angle_z = 0
        bpy.context.scene.offset = 0  

        print("End Script")         

    def manifold():
        """      
        Find the non manifold vertices and add edges and faces to fill the hole

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Deselect everything
        bpy.ops.mesh.select_all(action="DESELECT")

        # Pass in vertices selection
        bpy.ops.mesh.select_mode(type="VERT")

        # Select non manifold vertices
        bpy.ops.mesh.select_non_manifold()

        # Add an edge or face to selected vertices
        bpy.ops.mesh.edge_face_add()

        # Pass in faces selection
        bpy.ops.mesh.select_mode(type="FACE")

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')        

    def regenerate_bottom():
        """      
        Regenerate bottom if the bottom is bad generated

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Get the name of the object
        nameObject = bpy.context.active_object.name

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Delete the actual bottom
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), clear_inner=True, xstart=187, xend=982, ystart=219, yend=247, flip=False)

        # Init the offset
        bpy.context.scene.offset = 0

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object
        obj = bpy.context.active_object

        # Get the min and max location in x and y of the mesh
        xMax = float('-inf')
        xMin = float('inf')
        yMax = float('-inf')
        yMin = float('inf')
        for poly in obj.data.polygons:
            xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
            xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
            yMax = max(yMax, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
            yMin = min(yMin, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)

        # Add the new bottom
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.001),rotation=(3.14159, 0, 0), scale=(1, 1, 1))

        # Resize the bottom
        bpy.data.objects["Plane"].dimensions = [bpy.data.objects[nameObject].dimensions[0], bpy.data.objects[nameObject].dimensions[1], 0]

        # Select the mesh and the bottom
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
        bpy.data.objects[nameObject].select_set(True)
        bpy.data.objects["Plane"].select_set(True)

        # Join the mesh and the bottom
        bpy.ops.object.join()

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Intersect the bottom with the mesh
        bpy.ops.mesh.intersect(mode='SELECT_UNSELECT', separate_mode='NONE', solver='EXACT')

        # Deselect all the faces
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(type="VERT")

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object
        obj = bpy.context.active_object

        # Find the 4 vertices of the original plane
        for v in obj.data.vertices:
            if (v.co.x < xMax + 0.001 and v.co.x > xMax - 0.001) or (v.co.x < xMin + 0.001 and v.co.x > xMin - 0.001):
                if (v.co.y < yMax + 0.001 and v.co.y > yMax - 0.001) or (v.co.y < yMin + 0.001 and v.co.y > yMin - 0.001):
                    v.select = True
                    
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Delete the selected vertices
        bpy.ops.mesh.delete(type='VERT')

        # Select all the faces
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.select_all(action='SELECT')
        
        # Bissect in the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), clear_inner=True, xstart=453, xend=2540, ystart=814, yend=899, flip=False)
  
        # Init the offset
        bpy.context.scene.offset = 0
  
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
        
    def generate_socle(socleSize):
        """      
        Generate a socle to the selected mesh

        Note:
            A mesh must be selected
        Args:
            socleSize: float distance to be extruded horizontally from the vertical faces to create the socle
        Returns:
            None
        """
        # Get the active object
        obj = bpy.context.active_object

        # Name of the copy object
        nameCopy = "temp_copy"

        # Get the object name
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

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Only keep the bottom
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=(0, 0, 1), clear_inner=True, clear_outer=True, xstart=312, xend=839, ystart=150, yend=104, flip=False)

        # Select all the faces
        bpy.ops.mesh.select_all(action='SELECT')

        # Extrude the bottom
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(-0, -0, -0.1), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Deselect all the faces
        bpy.ops.mesh.select_all(action='DESELECT')

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the active object
        obj = bpy.context.active_object

        # Find the mondial matrix of the mesh for the rotation of the mesh
        matrix_new = obj.matrix_world.to_3x3().inverted().transposed()

        # Find and select all the vertical faces
        for poly in obj.data.polygons:
            # Find the normal vector in function of the angles of the mesh               
            no_world = matrix_new @ poly.normal
            no_world.normalize()
            print(no_world)

            # Calculate the angle between the normal and the downward vector if the normal vector is no null
            if no_world != mathutils.Vector((0,0,0)):
                angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))
            else:
                angle = 0

            # Check if the angle is between the wanted value
            if angle < radians(91) and angle >  radians(89):
                # Select the faces
                poly.select = True
              
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')  
             
        # Extrude vertical faces along normal to make the socle
        bpy.ops.mesh.extrude_region_shrink_fatten(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_shrink_fatten={"value":socleSize, "use_even_offset":False, "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "release_confirm":False, "use_accurate":False})

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT') 
            
        # Select the object and the socle
        bpy.data.objects[nameObject].select_set(True)
        bpy.data.objects[nameCopy].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[nameObject] 

        # Join the mesh and the socle
        bpy.ops.object.join()

   
    def separate_faces():
        """      
        Separate selected faces in a new mesh 
        and delete the base object

        Note:
            Some faces must be selected
        Args:
            None
        Returns:
            None
        """
        
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
         
    def select_area(minArea):
        """      
        Find all the separated pieces of the mesh
        and select the pieces where the area is higher
        than the minimum area value

        Note:
            A mesh must be selected
        Args:
            minArea: float minimum value of the area for select the faces of a piece of a mesh
        Returns:
            None
        """     
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Deselect everything
        bpy.ops.mesh.select_all(action="DESELECT")
        
        # Load mesh
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        # Ensure internal data needed for int subscription is initialized
        bm.faces.ensure_lookup_table()

        # Array containing the different areas
        loops = []
        faces = bm.faces

        # Loop for detect multiple areas
        while faces:
            faces[0].select_set(True)                   # Select 1st face
            bpy.ops.mesh.select_linked()                # Select all linked faces makes a full loop
            loops.append([f.index for f in faces if f.select])
            bpy.ops.mesh.hide(unselected=False)         # Hide the detected loop
            faces = [f for f in bm.faces if not f.hide] # Update faces

        # Unhide all faces
        bpy.ops.mesh.reveal()
        print("Mesh has {} parts".format(len(loops)))

        print("\nThe face lists are:")
        for loop in loops:
            print(loop)
            
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        # Deselect everything
        bpy.ops.mesh.select_all(action="DESELECT")
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Loop to select areas are higher than the area min
        area = 0 
        for rows in range(len(loops)):
            area = 0
            for columns in loops[rows]:
                # Calculate the area
                area = area + bpy.context.active_object.data.polygons[columns].area
            print(rows)
            print(area)
            print(minArea)
            # Compare the area with the area min
            if area > minArea:
                for columns in loops[rows]:
                    # Select all the faces of the area
                    bpy.context.active_object.data.polygons[columns].select = True

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')


    def select_resize_all():
        """      
        Select all the faces connected to the selected faces

        Note:
            Some faces must be selected
        Args:
            None
        Returns:
            None
        """
        date_1 = datetime.datetime.now()
        print("Start")

        # Get the active object
        obj = bpy.context.active_object

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the selected faces and their min and max location in x and y
        tabSelectedFaces = []
        xMax = float('-inf')
        xMin = float('inf')
        yMax = float('-inf')
        yMin = float('inf')
        for poly in obj.data.polygons:
            if poly.select == True:
                tabSelectedFaces.append(poly)
                xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                yMax = max(yMax, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
                yMin = min(yMin, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)

        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')

        # Load mesh
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        # Ensure internal data needed for int subscription is initialized
        bm.faces.ensure_lookup_table()

        # While all connected faces are not selected
        while bm.faces:
            # Find connected faces to the selection
            grow_faces = set(f for f in bm.verts if f.select for f in f.link_faces if not f.select)

            # If no more faces, leave the loop
            if grow_faces == set():
                break;

            # Select the faces and update min and max x and y location
            for f in grow_faces:
                f.select = True
                xMax = max(xMax, f.verts[0].co.x, f.verts[1].co.x, f.verts[2].co.x)
                xMin = min(xMin, f.verts[0].co.x, f.verts[1].co.x, f.verts[2].co.x)
                yMax = max(yMax, f.verts[0].co.y, f.verts[1].co.y, f.verts[2].co.y)
                yMin = min(yMin, f.verts[0].co.y, f.verts[1].co.y, f.verts[2].co.y)
                
        print(xMax,xMin,xMax-xMin) 
        print(yMax,yMin,yMax-yMin)         

        # Update the information for the resize action
        bpy.context.scene.sizeX = xMax-xMin
        bpy.context.scene.oldResizeX = 1
        bpy.context.scene.sizeY = yMax-yMin
        bpy.context.scene.oldResizeY = 1

        # Transfer the data back to the object's mesh               
        bmesh.update_edit_mesh(me)

        print("End Script")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print("Time : ", total_seconds)
           
    def select_resize(minAngleZ, maxAngleZ):
        """      
        Select all the faces connected to the selected faces between a min and max angle between the normal and the downward vector

        Note:
            Some faces must be selected
        Args:
            minAngleZ: float min angle between the normal and downward vector where the connected faces is selected in radians
            maxAngleZ: float max angle between the normal and downward vector where the connected faces is selected in radians
        Returns:
            None
        """
        date_1 = datetime.datetime.now()
        print("Start")
       
        # Get the active object
        obj = bpy.context.active_object
        
        # Find the mondial matrix of the mesh for the rotation of the mesh
        matrix_new = obj.matrix_world.to_3x3()#.inverted().transposed()

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Get the selected faces and their min and max location in x and y
        tabSelectedFaces = []
        xMax = float('-inf')
        xMin = float('inf')
        yMax = float('-inf')
        yMin = float('inf')
        for poly in obj.data.polygons:
            if poly.select == True:
                tabSelectedFaces.append(poly)
                xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                yMax = max(yMax, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
                yMin = min(yMin, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)

        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')

        # Load mesh
        me = bpy.context.edit_object.data
        bm = bmesh.from_edit_mesh(me)
        # Ensure internal data needed for int subscription is initialized
        bm.faces.ensure_lookup_table()

        # While all connected faces between the angles are not selected
        while bm.faces:
            # Find connected not hide faces to the selection
            grow_faces = set(f for f in bm.verts if f.select for f in f.link_faces if (not f.select and not f.hide))

            # If no more faces, leave the loop
            if grow_faces == set():
                break;

            for f in grow_faces:
                # Find the normal vector in function of the angles of the mesh               
                no_world = matrix_new @ f.normal
                no_world.normalize()
                print("no_world ",no_world,"matrix_new ",matrix_new,"f.normal ", f.normal)
                
                # Calculate the angle between the normal and the downward vector if the normal vector is no null
                if no_world != mathutils.Vector((0,0,0)):
                    angle = mathutils.Vector(no_world).angle(mathutils.Vector((0,0,-1)))
                else:
                    angle = 0
            
                # Check if the angle is between the min and max angles z
                if angle < maxAngleZ and angle >  minAngleZ:
                    # Select the faces and update min and max x and y location
                    f.select = True
                    xMax = max(xMax, f.verts[0].co.x, f.verts[1].co.x, f.verts[2].co.x)
                    xMin = min(xMin, f.verts[0].co.x, f.verts[1].co.x, f.verts[2].co.x)
                    yMax = max(yMax, f.verts[0].co.y, f.verts[1].co.y, f.verts[2].co.y)
                    yMin = min(yMin, f.verts[0].co.y, f.verts[1].co.y, f.verts[2].co.y)                    
                else:
                    # Hide the face
                    f.hide = True
         
        print(xMax,xMin,xMax-xMin) 
        print(yMax,yMin,yMax-yMin) 
        
        # Update the information for the resize action
        bpy.context.scene.sizeX = xMax-xMin
        bpy.context.scene.oldResizeX = 1
        bpy.context.scene.sizeY = yMax-yMin
        bpy.context.scene.oldResizeY = 1
         
        # Unhide all faces
        bpy.ops.mesh.reveal(select = False)
        
        # Transfer the data back to the object's mesh
        bmesh.update_edit_mesh(me)

        print("End Script")

        date_2 = datetime.datetime.now()
        time_delta = (date_2 - date_1)
        total_seconds = time_delta.total_seconds()
        print("Time : ", total_seconds)
        
    def resize():
        """      
        Resize the selection

        Note:
            Some faces must be selected
            When the selection doesn't change it is possible to modify the value of the resize
        Args:
            None
        Returns:
            None
        """
        # If the resize is not validate, cancel the last resize
        scaleX = 1/bpy.context.scene.oldResizeX
        scaleY = 1/bpy.context.scene.oldResizeY
        bpy.ops.transform.resize(value=(scaleX, scaleY, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

        # Calculate the new scale for resize with the value in mm
        scaleX = 1+(2*bpy.context.scene.resize/bpy.context.scene.sizeX)
        scaleY = 1+(2*bpy.context.scene.resize/bpy.context.scene.sizeY)
        # If negative resize, cancel the resize
        if scaleX <= 0 or scaleY <= 0:
            scaleX = 1
            scaleY = 1
        print(scaleX)

        # Apply the resize to the selection
        bpy.context.scene.oldResizeX = scaleX
        bpy.context.scene.oldResizeY = scaleY
        bpy.ops.transform.resize(value=(scaleX, scaleY, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=0.811, use_proportional_connected=False, use_proportional_projected=False)

    def invert_selection():
        """      
        Invert the selection

        Note:
            Some faces must be selected
        Args:
            None
        Returns:
            None
        """
        bpy.ops.mesh.select_all(action='INVERT')

    def delete_selection():
        """      
        Delete the selection

        Note:
            Some faces must be selected
        Args:
            None
        Returns:
            None
        """
        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        # Separate the selected faces
        bpy.ops.mesh.separate(type='SELECTED')

        # Switch in object mode
        bpy.ops.object.mode_set(mode = 'OBJECT')

        # Delete selected objects who don't have the name of the active object
        for obj in bpy.context.selected_objects:
            if obj.name != bpy.context.view_layer.objects.active.name:
                # Delete the object
                object_to_delete = obj
                bpy.data.objects.remove(object_to_delete, do_unlink=True) 

        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
                
        print("End Script")
        
    def fill():
        """      
        Fill hole for the selection

        Note:
            Some faces must be selected
            Faces must be on the same plane
        Args:
            None
        Returns:
            None
        """
        # Switch in edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        
        # Fill hole
        bpy.ops.mesh.fill() 

        
    def add_lattice():
        """      
        Add a lattice object with the size and location of the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """    
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT') 
    
        # Get the active object
        obj = bpy.context.active_object
        
        # Check if there is a lattice object
        flagLattice = False
        for o in bpy.data.objects:
            if o.type == 'LATTICE':
                flagLattice = True
        
        # Add a lattice if there is not
        if flagLattice == False:
            # Get the name of the object
            nameObject = obj.name
            
            # Add the lattice
            bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            
            # Select the object
            bpy.context.view_layer.objects.active = bpy.data.objects[nameObject]
            bpy.data.objects[nameObject].select_set(True)
            bpy.data.objects["Lattice"].select_set(False)
            


        # Add the vertices location in an array and find the max and min coordinates of the mesh
        tabVertices = []
        xPlus = float('-inf')
        xMoins = float('inf')
        yPlus = float('-inf')
        yMoins = float('inf')
        zPlus = float('-inf')
        zMoins = float('inf')
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

        # Set the size and the location of the lattice
        bpy.data.objects["Lattice"].scale = (obj.dimensions[0], obj.dimensions[1], obj.dimensions[2])
        bpy.data.objects["Lattice"].location = ((xPlus+xMoins)/2, (yPlus+yMoins)/2,(zPlus+zMoins)/2)

        # Update the float properties of the lattice and init them
        bpy.types.Scene.lattice_size_x = bpy.props.FloatProperty(name = "Size X", description="Size x of the lattice",  min = 0, max = 2*obj.dimensions[0], soft_min = 0, soft_max = 2*obj.dimensions[0], step = 10, get=Get_And_Set_Lattice.get_lattice_size_x, set=Get_And_Set_Lattice.set_lattice_size_x, unit = 'LENGTH')
        bpy.types.Scene.lattice_size_y = bpy.props.FloatProperty(name = "Size Y", description="Size y of the lattice",  min = 0, max = 2*obj.dimensions[1], soft_min = 0, soft_max = 2*obj.dimensions[1], step = 10, get=Get_And_Set_Lattice.get_lattice_size_y, set=Get_And_Set_Lattice.set_lattice_size_y, unit = 'LENGTH')
        bpy.types.Scene.lattice_size_z = bpy.props.FloatProperty(name = "Size Z", description="Size z of the lattice",  min = 0, max = 2*obj.dimensions[2], soft_min = 0, soft_max = 2*obj.dimensions[2], step = 10, get=Get_And_Set_Lattice.get_lattice_size_z, set=Get_And_Set_Lattice.set_lattice_size_z, unit = 'LENGTH')
        
        bpy.context.scene.lattice_size_x = obj.dimensions[0]
        bpy.context.scene.lattice_size_y = obj.dimensions[1]
        bpy.context.scene.lattice_size_z = obj.dimensions[2]
        
        bpy.types.Scene.lattice_offset_x = bpy.props.FloatProperty(name = "Offset X", description="Offset x of the lattice",  min = -obj.dimensions[0], max = obj.dimensions[0], soft_min = -obj.dimensions[0], soft_max = obj.dimensions[0], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_x, set=Get_And_Set_Lattice.set_lattice_offset_x, unit = 'LENGTH')
        bpy.types.Scene.lattice_offset_y = bpy.props.FloatProperty(name = "Offset Y", description="Offset y of the lattice",  min = -obj.dimensions[1], max = obj.dimensions[1], soft_min = -obj.dimensions[1], soft_max = obj.dimensions[1], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_y, set=Get_And_Set_Lattice.set_lattice_offset_y, unit = 'LENGTH')
        bpy.types.Scene.lattice_offset_z = bpy.props.FloatProperty(name = "Offset Z", description="Offset z of the lattice",  min = -obj.dimensions[2], max = obj.dimensions[2], soft_min = -obj.dimensions[2], soft_max = obj.dimensions[2], step = 10, get=Get_And_Set_Lattice.get_lattice_offset_z, set=Get_And_Set_Lattice.set_lattice_offset_z, unit = 'LENGTH')
        
        bpy.context.scene.lattice_offset_x = 0
        bpy.context.scene.lattice_offset_y = 0
        bpy.context.scene.lattice_offset_z = 0
        
    def select_lattice():
        """      
        Select faces in the lattice of the selected mesh

        Note:
            A mesh must be selected and a lattice must be present
        Args:
            None
        Returns:
            None
        """      
        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get the active object
        obj = bpy.context.active_object
        
        # Deselect all the faces
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Switch in object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select the faces in the lattice and get the min and max location of these faces in x and y     
        xMax = float('-inf')
        xMin = float('inf')
        yMax = float('-inf')
        yMin = float('inf')
        for poly in obj.data.polygons:
            if (obj.matrix_world @ poly.center)[0]>=(bpy.data.lattices['Lattice'].points[0].co[0]*bpy.data.objects["Lattice"].scale[0]+bpy.data.objects["Lattice"].location[0]) and (obj.matrix_world @ poly.center)[0]<=(bpy.data.lattices['Lattice'].points[1].co[0]*bpy.data.objects["Lattice"].scale[0]+bpy.data.objects["Lattice"].location[0]):
                if (obj.matrix_world @ poly.center)[1]>=(bpy.data.lattices['Lattice'].points[0].co[1]*bpy.data.objects["Lattice"].scale[1]+bpy.data.objects["Lattice"].location[1]) and (obj.matrix_world @ poly.center)[1]<=(bpy.data.lattices['Lattice'].points[2].co[1]*bpy.data.objects["Lattice"].scale[1]+bpy.data.objects["Lattice"].location[1]):
                    if (obj.matrix_world @ poly.center)[2]>=(bpy.data.lattices['Lattice'].points[0].co[2]*bpy.data.objects["Lattice"].scale[2]+bpy.data.objects["Lattice"].location[2]) and (obj.matrix_world @ poly.center)[2]<=(bpy.data.lattices['Lattice'].points[4].co[2]*bpy.data.objects["Lattice"].scale[2]+bpy.data.objects["Lattice"].location[2]):
                        poly.select = True
                        xMax = max(xMax, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                        xMin = min(xMin, obj.data.vertices[poly.vertices[0]].co.x, obj.data.vertices[poly.vertices[1]].co.x, obj.data.vertices[poly.vertices[2]].co.x)
                        yMax = max(yMax, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
                        yMin = min(yMin, obj.data.vertices[poly.vertices[0]].co.y, obj.data.vertices[poly.vertices[1]].co.y, obj.data.vertices[poly.vertices[2]].co.y)
                        
        # Update the information for the resize action
        bpy.context.scene.sizeX = xMax-xMin
        bpy.context.scene.oldResizeX = 1
        bpy.context.scene.sizeY = yMax-yMin
        bpy.context.scene.oldResizeY = 1
                        
        # Switch in edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
    def delete_lattice():
        """      
        Delete the existing lattice

        Note:
            None
        Args:
            None
        Returns:
            None
        """  
        # Delete the existing lattice
        for o in bpy.data.objects:
            if o.type == 'LATTICE':
                # Delete the existing lattice
                object_to_delete = bpy.data.objects["Lattice"]
                bpy.data.objects.remove(object_to_delete, do_unlink=True) 
 
 
    def voxel():
        """      
        Add a voxel remesh to the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """  
        # Get the active object
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
        
    def decimate():
        """      
        Decrease the number of the faces to the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """  
        # Get the active object
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
    
    def validate():
        """      
        Apply modifier to the selected mesh

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')
    
        # Apply modifier
        bpy.ops.object.apply_all_modifiers()
        
        # Get the active objec
        obj = bpy.context.active_object
        print("Number of faces", len(obj.data.polygons))
        
    def remesh_blocks():
        """      
        Add a blocks remesh to the selected mesh, then make an intersection with the mesh to keep the same occupied surface

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        
        # Get the active object
        obj = bpy.context.active_object
        
        nameCopy = "temp_copy"

        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        # Remove all modifiers from the object
        obj.modifiers.clear()

        # Delete the existing copy 
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

    def validate_blocks():
        """      
        Apply blocks modifier to the selected mesh, then extrude the bottom on the xy plane

        Note:
            A mesh must be selected
        Args:
            None
        Returns:
            None
        """
        # Validate the remesh blocks modifiers
        bpy.ops.object.apply_all_modifiers()
        
        date_1 = datetime.datetime.now()
        print("Start")
        
        # Select the bottom faces
        Button_Operations.select_faces(radians(10))

        # Extrude the support
        bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -20), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

        # Select all
        bpy.ops.mesh.select_all(action='SELECT')

        # Bissect and delete the element under the xy plane
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.001), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False) 

        # Fill the hole and triangulate faces
        Button_Operations.manifold()
      
        # Delete the copy
        object_to_delete = bpy.data.objects["temp_copy"]
        bpy.data.objects.remove(object_to_delete, do_unlink=True) 
        
        # Switch in object mode 
        bpy.ops.object.mode_set(mode='OBJECT')

        
    def measure_distance():
        """      
        Calculate the distance between two selected vertices

        Note:
            Only two vertices must be selected
        Args:
            None
        Returns:
            None
        """
        # Get the active object
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
        
        # Calculate the distance between the two points
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

