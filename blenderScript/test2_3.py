import datetime

import bpy
import mathutils

date_1 = datetime.datetime.now()
print("Start")

pi = 3.14159265
maxAngle = 5
maxAngleRad = maxAngle*pi/180

# Switch in object mode 
bpy.ops.object.mode_set(mode='OBJECT')
# set the camera position
tx = 0.0
ty = 0.0
tz = -10.0
rx = 180.0
ry = 0.0
rz = 0.0
fov = 20.4
pi = 3.14159265
scene = bpy.data.scenes["Scene"]
# Set render resolution
scene.render.resolution_x = 480
scene.render.resolution_y = 480
# Set camera fov in degrees
scene.camera.data.angle = fov*(pi/180.0)
# Set camera rotation in euler angles
scene.camera.rotation_mode = 'XYZ'
scene.camera.rotation_euler[0] = rx*(pi/180.0)
scene.camera.rotation_euler[1] = ry*(pi/180.0)
scene.camera.rotation_euler[2] = rz*(pi/180.0)
# Set camera translation
scene.camera.location.x = tx
scene.camera.location.y = ty
scene.camera.location.z = tz

# Reframe the camera
bpy.ops.view3d.camera_to_view_selected()

# Switch in camera view
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].region_3d.view_perspective = 'CAMERA'

# Zoom camera 1:1
for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type == 'VIEW_3D':
            override = {'window': window, 'screen': screen, 'area': area}
            bpy.ops.view3d.zoom_camera_1_to_1(override)
            break

# Update the informations of the scene
bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

# Switch in edit mode 
bpy.ops.object.mode_set(mode='EDIT')

# Select all
bpy.ops.mesh.select_all(action='DESELECT')

###########################################################################
# Select faces visible from camera
# Script found here : https://blenderartists.org/t/select-all-faces-visible-from-camera/1210826
###################################

def view3d_find():
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    return region, rv3d
    return None, None

def view3d_camera_border(scene):
    obj = scene.camera
    cam = obj.data

    #frame = cam.view_frame(scene)
    frame = bpy.context.scene.camera.data.view_frame(scene=bpy.context.scene)

    # move from object-space into world-space 
    frame = [obj.matrix_world @ v for v in frame]

    # move into pixelspace
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    region, rv3d = view3d_find()
    print(region, rv3d)
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
    return frame_px
#'''

def getView3dAreaAndRegion(context):
    for area in context.screen.areas:
        if area.type == "VIEW_3D":
            for region in area.regions:
                if region.type == "WINDOW":
                    return area, region

def select_border(context, corners, extend=True):
    bpy.ops.view3d.select_box(getOverride(context),
            wait_for_input=False,
            xmin=corners[0],
            xmax=corners[1],
            ymin=corners[2],
            ymax=corners[3],
            mode='SET')
    
    return True


def getOverride(context):
    view3dArea, view3dRegion = getView3dAreaAndRegion(context)
    override = context.copy()
    override['area'] = view3dArea
    override['region'] = view3dRegion
    return override

def getCorners(cam_corners):
    '''
    returns xmin,xmax,ymin,ymax
    '''
    print(cam_corners)
    return [cam_corners[2][0],cam_corners[0][0],cam_corners[2][1],cam_corners[0][1]]


def doStuff():
    
    print("--")
    # go to editmode
    bpy.ops.object.mode_set(mode="EDIT")
    vertex, edge, face = False, False, True
    bpy.context.tool_settings.mesh_select_mode = (vertex, edge, face)

    # set camera view (both approaches do the same)
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    area.spaces[0].region_3d.view_perspective = 'CAMERA'
    #bpy.ops.view3d.view_camera(getOverride(bpy.context))

    # get camera borders in view coordinates
    cam_corners = getCorners(view3d_camera_border(bpy.context.scene))
    print(cam_corners)
    
    # select stuff in borders
    select_border(bpy.context, cam_corners, extend = False)

doStuff()

obj = bpy.context.active_object

tabSelected = []
for poly in obj.data.polygons:
    if poly.select == True:
        tabSelected.append(poly.index) 

bpy.ops.object.mode_set(mode = 'EDIT')

bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.object.mode_set(mode = 'OBJECT')

tabVertices = []
for vertex in obj.data.vertices:
   tabVertices.append(obj.matrix_world @ vertex.co) 
   
#tabPoly = []
#for poly in obj.data.polygons:
#    tabPoly.append(poly)

print("Start for loop")    
for poly in obj.data.polygons:
    angle = mathutils.Vector(poly.normal).angle(mathutils.Vector((0,0,-1)))
    if angle < maxAngleRad:
        poly.select = True
        
        print(poly.index)
        
        triangleCenter = (tabVertices[poly.vertices[0]]+tabVertices[poly.vertices[1]]+tabVertices[poly.vertices[2]])/3
        flagVisible = False
        for indexPoly in tabSelected:    
            if poly.index ==  indexPoly: 
                flagVisible = True
                break
        if flagVisible == False:                   
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