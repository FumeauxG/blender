###########################
# Test automatized Blender
# Author : Fumeaux Gaëtan
# v1.0
###########################

import glob
import bpy

# Check edit mode activate
if bpy.context.active_object.mode == 'EDIT':
    bpy.ops.object.editmode_toggle()

# Delete the existing cube
bpy.ops.object.delete(use_global=False, confirm=False)

# set the camera position
tx = 0.0
ty = 0.0
tz = -10.0
rx = 180.0
ry = 0.0
rz = 0.0
fov = 90.0
pi = 3.14159265
scene = bpy.data.scenes["Scene"]
# Set render resolution
scene.render.resolution_x = 480
scene.render.resolution_y = 359
# Set camera fov in degrees
#scene.camera.data.angle = fov*(pi/180.0)
# Set camera rotation in euler angles
scene.camera.rotation_mode = 'XYZ'
scene.camera.rotation_euler[0] = rx*(pi/180.0)
scene.camera.rotation_euler[1] = ry*(pi/180.0)
scene.camera.rotation_euler[2] = rz*(pi/180.0)
# Set camera translation
scene.camera.location.x = tx
scene.camera.location.y = ty
scene.camera.location.z = tz


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

# Import the stl file
bpy.ops.import_mesh.stl(filepath=pathIn)

# Align the object on the xy plane
bpy.ops.object.align(align_mode='OPT_1', relative_to='OPT_1', align_axis={'Z'})

# Switch in the edit mode
bpy.ops.object.editmode_toggle()

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
############################################################################################

# Separate the selected faces
bpy.ops.mesh.separate(type='SELECTED')

# Switch in object mode
bpy.ops.object.editmode_toggle()

# Select the support object
bpy.data.objects[nameObject[0] + ".001"].select_set(True)
bpy.data.objects[nameObject[0]].select_set(False)

# Select faces visible from camera
doStuff()

# Extrude the support
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0, -10), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, True), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})

# Select all
bpy.ops.mesh.select_all(action='SELECT')

# Bissect and delete the element under the xy plane
bpy.ops.mesh.bisect(plane_co=(0, 0, 0.01), plane_no=(0, 0, 1), use_fill=True, clear_inner=True, xstart=942, xend=1489, ystart=872, yend=874, flip=False)

# Switch in object mode
bpy.ops.object.editmode_toggle()

# Select the support object
bpy.data.objects[nameObject[0] + ".001"].select_set(False)
bpy.data.objects[nameObject[0]].select_set(True)

# Delete the base object
bpy.ops.object.delete(use_global=False, confirm=False)

# Export the stl file
bpy.ops.export_mesh.stl(filepath=pathOut)

print("End Script")
