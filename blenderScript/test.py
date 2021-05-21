import bpy
import mathutils

pi = 3.14159265
maxAngle = 45

obj = bpy.context.active_object

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')
    
for poly in obj.data.polygons:
    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
    if angle < (maxAngle*pi/180):
        poly.select = True
        breakFlag = 0
        print(poly.index)
        v = obj.data.vertices[poly.vertices[0]]
        vectorA1 = obj.matrix_world @ v.co
        v = obj.data.vertices[poly.vertices[1]]
        vectorA2 = obj.matrix_world @ v.co
        v = obj.data.vertices[poly.vertices[2]]
        vectorA3 = obj.matrix_world @ v.co
        if vectorA1.z < vectorA2.z:
            if vectorA1.z < vectorA3.z:
                z1 = vectorA1.z
            else:
                z1 = vectorA3.z
        else:
            if vectorA2.z < vectorA3.z:
                z1 = vectorA2.z
            else:
                z1 = vectorA3.z
                
        for comparePoly in obj.data.polygons:
            v = obj.data.vertices[comparePoly.vertices[0]]
            vectorB1 = obj.matrix_world @ v.co
            v = obj.data.vertices[comparePoly.vertices[1]]
            vectorB2 = obj.matrix_world @ v.co
            v = obj.data.vertices[comparePoly.vertices[2]]
            vectorB3 = obj.matrix_world @ v.co
            
            #vectorA1 = obj.data.vertices[poly.vertices[0]].normal
            #vectorA1_2d = mathutils.Vector((vectorA1.x, vectorA1.y))
            #vectorA2 = obj.data.vertices[poly.vertices[1]].normal
            #vectorA2_2d = mathutils.Vector((vectorA2.x, vectorA2.y))
            #vectorA3 = obj.data.vertices[poly.vertices[2]].normal
            #vectorA3_2d = mathutils.Vector((vectorA3.x, vectorA3.y))              
            #vectorB1 = obj.data.vertices[comparePoly.vertices[0]].normal
            #vectorB1_2d = mathutils.Vector((vectorB1.x, vectorB1.y))
            #vectorB2 = obj.data.vertices[comparePoly.vertices[1]].normal
            #vectorB2_2d = mathutils.Vector((vectorB2.x, vectorB2.y))
            #vectorB3 = obj.data.vertices[comparePoly.vertices[2]].normal
            #vectorB3_2d = mathutils.Vector((vectorB3.x, vectorB3.y))
            
            
            #print(vectorA1)
            #if mathutils.geometry.intersect_tri_tri_2d(vectorA1_2d, vectorA2_2d, vectorA3_2d, vectorB1_2d, vectorB2_2d, vectorB3_2d) == True:
            if mathutils.geometry.intersect_tri_tri_2d(vectorA1, vectorA2, vectorA3, vectorB1, vectorB2, vectorB3) == True:
                                        
                if vectorB1.z > vectorB2.z:
                    if vectorB1.z > vectorB3.z:
                        z2 = vectorB1.z
                    else:
                        z2 = vectorB3.z
                else:
                    if vectorB2.z > vectorB3.z:
                        z2 = vectorB2.z
                    else:
                        z2 = vectorB3.z
                if z1 > z2 and (poly.index != comparePoly.index):
                    poly.select = False
                    breakFlag = 1 
                if breakFlag == 1:
                    break
                
            
   
bpy.ops.object.mode_set(mode = 'EDIT')
print("Endscript")