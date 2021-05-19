import bpy

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

bpy.ops.view3d.camera_to_view_selected()

#'''
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


print("now ready for splitting")

#bpy.ops.mesh.separate(type='SELECTED')

#bpy.ops.object.mode_set(mode="OBJECT")