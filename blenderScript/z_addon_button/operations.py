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
    def select_faces(maxAngle):
        date_1 = datetime.datetime.now()
        print("Start")

        print(maxAngle, maxAngle*180/pi)

        obj = bpy.context.active_object

        # Add the vertices location in an array
        tabVertices = []
        for vertex in obj.data.vertices:
           tabVertices.append(obj.matrix_world @ vertex.co)

        #matrix_new = obj.matrix_world.to_3x3().inverted().transposed()
        matrix_new = obj.matrix_world.to_3x3().inverted()
        no_world = matrix_new @ mathutils.Vector((0,0,-1))
        no_world.normalize() 
        
        #vecDir = mathutils.Vector((0,0,-1))
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
            tabPoint3Z.append(tabVertices[poly.vertices[2]].z)

        print(len(tabPoly))   

        # Get the C function
        #functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\function.dll")
        print(os.path.dirname(__file__))
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
        # Switch in edit mode 
        bpy.ops.object.mode_set(mode='EDIT')
        
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
        bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

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
        
        print("End Script")   
        
    def manifold_and_triangulate():
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