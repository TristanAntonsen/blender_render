import bpy
import bmesh
import time
from os.path import exists



while exists('tmp.txt') == False:
    time.sleep(1)

tmp_file = open('tmp.txt','r')
INPUT_PATHS = tmp_file.read().split(',')

FILE_PATH = INPUT_PATHS[0]
FILE_NAME = FILE_PATH.split('\\')
OBJECT_NAME = FILE_NAME[len(FILE_NAME)-1].replace('.stl','')
EXPORT_PATH = INPUT_PATHS[1]
RENDERER = INPUT_PATHS[2]


obj = bpy.ops.import_mesh.stl(filepath=FILE_PATH)

mesh = bpy.context.object.data
for f in mesh.polygons:
    f.use_smooth = True
 
mat = bpy.data.materials.get("material1")
mesh.materials.append(mat)

#Adding edge split modifier for rendering with smooth shading
bpy.ops.object.modifier_add(type='EDGE_SPLIT')

#Calculating bounding box
xSpan = bpy.data.objects[OBJECT_NAME].dimensions.x
ySpan = bpy.data.objects[OBJECT_NAME].dimensions.y
zSpan = bpy.data.objects[OBJECT_NAME].dimensions.z

bBoxDims = [xSpan,ySpan,zSpan]

object = bpy.context.active_object
vertices = []
[vertices.append(v[:]) for v in object.bound_box]

def Calc_BBox_Centroid(_vertices):
    
    x = 0
    y = 0
    z = 0
    
    for vertex in _vertices:
#        print(vertex)
        x += vertex[0]
        y += vertex[1]
        z += vertex[2]
    x /= 8
    y /= 8
    z /= 8
    
    return [x,y,z]


bBoxCentroid = Calc_BBox_Centroid(vertices)

cameraField = 2.25
scaleFactor =  cameraField / max(xSpan,ySpan,zSpan)

translationVector = [-1 * element for element in bBoxCentroid]

##Front view
bpy.ops.transform.translate(value=(translationVector[0],translationVector[1],translationVector[2]))
bpy.ops.transform.resize(value=(scaleFactor,scaleFactor,scaleFactor),center_override = (0,0,0))

##Top view
#bpy.ops.transform.rotate(value= -math.pi/2, orient_axis = 'X', center_override = (0,0,0))

###Side view
#bpy.ops.transform.rotate(value= math.pi/2, orient_axis = 'X', center_override = (0,0,0))
#bpy.ops.transform.rotate(value= math.pi/2, orient_axis = 'Z', center_override = (0,0,0))


###Iso view
##bpy.ops.transform.rotate(value=0, orient_axis = 'Z')


scene = bpy.context.scene
# scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.engine = RENDERER
scene.render.image_settings.file_format='PNG'
scene.render.filepath=EXPORT_PATH
bpy.ops.render.render(write_still=1)