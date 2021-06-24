import bpy
import mathutils
import glob
import ctypes
import datetime

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
maxAngle = 89#bpy.context.scene.max_angle
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

functionC = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\functionTestMold.dll")

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

functionC.select_faces(arrIndex,len(tabPoly),maxFacesMold,arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

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
bpy.ops.mesh.bisect(plane_co=(0, 0, -2.5), plane_no=(0, 0, 1), use_fill=False, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

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
bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, -2.5-0.2), scale=(1,1,1))
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
