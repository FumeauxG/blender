import ctypes
import bpy
import mathutils
import datetime

date_1 = datetime.datetime.now()
print("Start")

pi = 3.14159265
maxAngle = 89

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

testlib = ctypes.CDLL("C:\\Gaetan\\_Bachelor\\blender\\blenderScript\\TestCtypes\\testlib.dll")


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

testlib.myprint(arrIndex,len(tabPoly),arrNormalX,arrNormalY,arrNormalZ,ctypes.c_float(maxAngle),ctypes.c_float(vecDir.x),ctypes.c_float(vecDir.y),ctypes.c_float(vecDir.z),arrFaces,arrPoint1X,arrPoint1Y,arrPoint2X,arrPoint2Y,arrPoint3X,arrPoint3Y,arrPoint1Z,arrPoint2Z,arrPoint3Z)

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