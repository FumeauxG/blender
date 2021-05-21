import bpy
import mathutils

pi = 3.14159265
maxAngle = 30
maxAngleRad = maxAngle*pi/180

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')
    
for poly in obj.data.polygons:
    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
    if angle < maxAngleRad:
        poly.select = True
        print(poly.index)
        #v = obj.data.vertices[poly.vertices[0]]
        #vectorA1 = obj.matrix_world @ v.co
        #v = obj.data.vertices[poly.vertices[1]]
        #vectorA2 = obj.matrix_world @ v.co
        #v = obj.data.vertices[poly.vertices[2]]
        #vectorA3 = obj.matrix_world @ v.co
        vectorA1 = obj.matrix_world @ obj.data.vertices[poly.vertices[0]].co
        vectorA2 = obj.matrix_world @ obj.data.vertices[poly.vertices[1]].co
        vectorA3 = obj.matrix_world @ obj.data.vertices[poly.vertices[2]].co
        
        triangleCenter = (vectorA1+vectorA2+vectorA3)/3
                
        for comparePoly in obj.data.polygons:
            #v = obj.data.vertices[comparePoly.vertices[0]]
            #vectorB1 = obj.matrix_world @ v.co
            #v = obj.data.vertices[comparePoly.vertices[1]]
            #vectorB2 = obj.matrix_world @ v.co
            #v = obj.data.vertices[comparePoly.vertices[2]]
            #vectorB3 = obj.matrix_world @ v.co
            vectorB1 = obj.matrix_world @ obj.data.vertices[comparePoly.vertices[0]].co
            vectorB2 = obj.matrix_world @ obj.data.vertices[comparePoly.vertices[1]].co
            vectorB3 = obj.matrix_world @ obj.data.vertices[comparePoly.vertices[2]].co
            #inter = mathutils.geometry.intersect_ray_tri(vectorB1, vectorB2, vectorB3, mathutils.Vector((0,0,-1)), triangleCenter, True)
            #print(vectorA1)
            if  (mathutils.geometry.intersect_ray_tri(vectorB1, vectorB2, vectorB3, mathutils.Vector((0,0,-1)), triangleCenter, True)) != None and (poly.index != comparePoly.index):
                poly.select = False
                break
                
            
   
bpy.ops.object.mode_set(mode = 'EDIT')
print("Endscript")