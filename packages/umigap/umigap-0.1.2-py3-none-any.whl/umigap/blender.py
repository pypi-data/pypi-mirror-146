"""
umigap:
Use a yaml file and instructions from the user to add animated characters to The Beat


# run from glamrig.sh

# common tests
# ./glamrig.sh -- countrykid import none

"""
import logging
import shutil
import sys
from math import radians
from pathlib import Path
from random import uniform

import yaml
from bvh import Bvh
from mathutils import Vector
from pygltflib import ANIM_LINEAR, GLTF2, Animation, AnimationChannel, AnimationSampler
from pygltflib.utils import find_node_index_by_name

try:
    import bpy  # blender
except ModuleNotFoundError:
    print("Unable to find blender python module")
    print(
        "Run from a script with something like: blender -b -P godotrig.py -- infile character -b bvh -d"
    )

logger = logging.getLogger(__name__)

working_dir = "/home/luke/Projects/thebeat-client/animations"
publish_dir = "/home/luke/Projects/thebeat-client/thebeat/Animations"


# def centre_pivot():
#     """move pivot to centre of volume"""
#     bpy.ops.object.origin_set(type="ORIGIN_CENTER_OF_VOLUME")
#
#
# def origin_to_bottom(ob):
#     """drop pivot point to bottom of active object"""
#     bpy.context.view_layer.objects.active = ob  # blender 2.8x
#     saved_location = bpy.context.scene.cursor.location  # returns a vector
#
#     # give 3dcursor new coordinates
#     bpy.context.scene.cursor.location = Vector((0.0, 0.0, 0.0))
#
#     # set the origin on the current object to the 3dcursor location
#     bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
#
#     # set 3dcursor location back to the stored location
#     bpy.context.scene.cursor.location = saved_location
#
#
# def drop_pivot(drop_pivot_details=None):
#     """Drop all the pivots for the requested meshes to the floor"""
#     if drop_pivot_details is None:
#         drop_pivot_details = []
#     for o in bpy.context.scene.objects:
#         if o.type == "MESH":
#             origin_to_bottom(o)
#
#
# def decimate_scene(decimate_details):
#     """
#     Reduce a mesh collection to the amount in decimate (0-1.0)
#     """
#     object_list = bpy.data.objects
#     print("\n preparing for decimate...")
#     original_num_vertices = 0
#     new_num_vertices = 0
#     for obj in object_list:
#         if obj.type == "MESH":
#             me = obj.data
#             vs = len(me.vertices)
#             original_num_vertices += vs
#             es = len(me.edges)
#             ps = len(me.polygons)  # faces
#             ratio = decimate_details.get(obj.name, decimate_details.get("default"))
#             print(
#                 f" decimate {obj.name} verts: {vs}, edges:{es}, polygons: {ps}, ratio: {ratio}"
#             )
#
#     print("\n beginning decimate...")
#     for obj in object_list:
#         if obj.type == "MESH":
#             me = obj.data
#             vs = len(me.vertices)
#             es = len(me.edges)
#             ps = len(me.polygons)  # faces
#             print(f" decimate {obj.name} verts: {vs}, edges:{es}, polygons: {ps}")
#             # bpy.ops.object.modifier_add(type='DECIMATE')
#
#             modifier_name = "DecimateMod"
#             modifier = obj.modifiers.new(modifier_name, "DECIMATE")
#
#             modifier.ratio = decimate_details.get(
#                 obj.name, decimate_details.get("default")
#             )
#             print(f"  add {modifier.ratio} decimate ratio to {obj.name}")
#
#             modifier.use_collapse_triangulate = True
#             #            bpy.context.scene.objects.active = obj  # blender 2.7x
#             bpy.context.view_layer.objects.active = obj  # blender 2.8x
#             bpy.ops.object.modifier_apply(modifier=modifier_name)
#
#             vs = len(me.vertices)
#             es = len(me.edges)
#             ps = len(me.polygons)  # faces
#             new_num_vertices += vs
#             print(
#                 f"  after decimate {obj.name} verts: {vs}, edges:{es}, polygons: {ps}"
#             )
#
#             # bpy.context.object.modifiers["Decimate"].use_collapse_triangulate=True
#             # bpy.context.object.modifiers["Decimate"].ratio = decimate
#     print(
#         f" Finished decimate. Reduced from {original_num_vertices} vertices to {new_num_vertices}."
#     )
#
#
# def scale_scene(scale_factor=1.0):
#     """scale meshes"""
#     object_list = bpy.data.objects
#
#     for obj in object_list:
#         if obj.type == "MESH":
#             obj.scale *= scale_factor
#             # bpy.ops.transform
#
#
# def rotate_scene(x=0, y=0, z=0):
#     """rotate meshes"""
#     object_list = bpy.data.objects
#     ov = bpy.context.copy()
#     ov["area"] = [a for a in bpy.context.screen.areas if a.type == "VIEW_3D"][0]
#     bpy.ops.transform.rotate(ov)
#     for obj in object_list:
#         if obj.type == "MESH":
#             if x:
#                 bpy.ops.transform.rotate(ov, value=radians(x), orient_axis="X")
#             if y:
#                 bpy.ops.transform.rotate(ov, value=radians(y), orient_axis="Y")
#             if z:
#                 bpy.ops.transform.rotate(ov, value=radians(z), orient_axis="Z")
#
#
# def translate_scene(x=0, y=0, z=0):
#     """translate meshes"""
#     object_list = bpy.data.objects
#
#     for obj in object_list:
#         if obj.type == "MESH":
#             obj.location[0] += x
#             obj.location[1] += y
#             obj.location[2] += z
#
#             # bpy.ops.transform.translate(value=(x, y, z))
#
#
# def hide_layers(layers):
#     """
#     Hide layers
#     Courtesy https://blenderartists.org/t/make-layers-invisible-through-python-help/564472
#     """
#     for layer_name in layers:
#         obj = bpy.data.objects[layer_name]
#         layer = [i for i in range(len(obj.layers)) if obj.layers[i] is True]
#         for i in range(len(bpy.context.scene.layers)):
#             if i not in layer:
#                 bpy.context.scene.layers[i] = False
#             else:
#                 bpy.context.scene.layers[i] = True
#
#
# def expand_animations_alias(character, animations_alias):
#     """Get the list of animations we are working on for this character"""
#     character_name = character["name"]
#     animation_names = character["animations"].keys()
#     animations = {}
#
#     # [animations_alias]
#     if animations_alias not in animation_names and animations_alias != "all":
#         logger.warning(
#             f"No animation(s) {animations_alias} in yaml character {character_name} animations {animation_names}"
#         )
#         return animations
#     if animations_alias == "all":
#         # animation
#         animations = character["animations"]
#     else:
#         animations = {animations_alias: character["animations"][animations_alias]}
#     return animations
#
#
# def load_3d(filename):
#     """
#     Load a 3D file into blender. Clears existing scene.
#     """
#     filename = Path(filename)
#     if not filename.exists():
#         logger.warning(f"Unable to load {filename}. File not found")
#         return False
#     print(f"loading {filename}")
#     bpy.ops.wm.read_homefile(use_empty=True)  # clear scene
#     if "fbx" in filename.suffix:
#         bpy.ops.import_scene.fbx(filepath=filename.as_posix())
#     elif "dae" in filename.suffix:
#         bpy.ops.wm.collada_import(filepath=filename.as_posix())
#     elif "blend" in filename.suffix:
#         bpy.ops.wm.open_mainfile(filepath=filename.as_posix())
#     else:
#         logger.warning("File format not recognised. FIle not loaded")
#         return False
#     return True
#
#
# def save_3d(filename):
#     """
#     save a 3D file
#     """
#     filename = Path(filename)
#     if filename.exists():
#         logger.warning(f"{filename} already exists")
#     print(f"saved {filename}")
#     if "escn" in filename.suffix:
#         bpy.ops.export_godot.escn(filepath=filename.as_posix())
#     elif "glb" in filename.suffix:
#         bpy.ops.export_scene.gltf(filepath=filename.as_posix())
#     elif "fbx" in filename.suffix:
#         bpy.ops.export_scene.fbx(filepath=filename.as_posix())
#     elif "dae" in filename.suffix:
#         bpy.ops.wm.collada_export(filepath=filename.as_posix())
#     elif "blend" in filename.suffix:
#         bpy.ops.wm.save_as_mainfile(filepath=filename.as_posix())
#     else:
#         logger.warning("File format not recognised. FIle not saved")
#         return False
#     return True
#
#
# def import_character(character):
#     """Import raw character"""
#     details = character["raw"]
#
#     """
#     decimate_only = {'file': 'CountryKid/CountryKid.fbx',
#                      'decimate': {'default': 0.07, 'Country_Kid_R_3_ForFBX2': 0.01, 'Shoes_005__vrag6_2': 0.1,
#                                   'Pants': 0.1, 'Jocks_SeamsColor': 0.2, 'Eye_Brow': 0.1}, }
#     scale_only = {'file': 'countrykid_test.blend', 'scale': 8.5134, }
#     rotate_only = {'file': 'countrykid_test.blend', 'rotate': {'x': 0, 'y': 0, 'z': 180}, }
#     rotate_and_translate_only = {
#         'file': 'countrykid_test.blend',
#         'rotate': {'x': 0, 'y': 0, 'z': 180},
#         'translate': {
#             'x': 0,
#             'z': 0.18429,
#             'y': 0,
#         }
#     }
#
#     scale_rotate_and_translate_only = {
#         'file': 'countrykid_test.blend',
#         'rotate': {'x': 0, 'y': 0, 'z': 180},
#         'translate': {
#             'x': 0,
#             'z': 0.18429,
#             'y': 0,
#         },
#         'scale': 8.5134
#     }
#
#     scale_rotate_and_translate_droppivot_only = {
#         "drop-pivot": True,
#         'file': 'countrykid_test.blend',
#         'rotate': {'x': 0, 'y': 0, 'z': 180},
#         'translate': {
#             'x': 0,
#             'z': 0.18429,
#             'y': 0,
#         },
#         'scale': 8.5134
#     }
#     details = scale_rotate_and_translate_droppivot_only
#     """
#
#     raw_filename = Path(working_dir) / "raw" / Path(details["file"])
#     loaded = load_3d(raw_filename)
#     if not loaded:
#         return False
#
#     logger.info(f"Finished loading file {raw_filename}")
#
#     export_name = "ready_to_rig" / Path(character["imported"])
#     if export_name.exists():
#         logger.warning(f"{export_name} already exists.")
#
#     # reduce poly count
#     if details.get("decimate", {}):
#         print("decimate")
#         decimate_scene(details["decimate"])
#
#     # rotate
#     rotate_details = details.get("rotate", {})
#     if rotate_details:
#         print("rotate", rotate_details)
#         rotate_scene(**rotate_details)
#
#     # translate
#     translate_details = details.get("translate", {})
#     if translate_details:
#         print("translate")
#         translate_scene(**translate_details)
#
#     # drop pivots
#     if details.get("drop-pivot", False):
#         print("dropping pivot")
#         drop_pivot_details = []
#         drop_pivot(drop_pivot_details)
#
#     # volume pivots
#     if details.get("volume-pivot", False):
#         print("ignoring volume-pivot request")
#
#     # scale
#     scale_factor = details.get("scale", 1.0)
#     if scale_factor != 1.0:
#         print("scaling")
#         scale_scene(scale_factor)
#
#     # hide layers
#     layers = details.get("disable-layers", [])
#     if layers:
#         print("disabling layers")
#         hide_layers(layers)
#
#     # bpy.ops.export_scene.gltf(filepath=export_name)
#     save_3d(export_name)
#     return True
#
#
# def autorig_character(character):
#     """Autorig a character"""
#     print("autorig . Best to load the imported file into blender and manually do it.")
#     raw_filename = "ready_to_rig" / Path(character["imported"])
#     loaded = load_3d(raw_filename)
#     if not loaded:
#         return False
#
#     rig_data = character.get("rig", {})
#     if not rig_data:
#         print("No rig data.")
#         return
#
#     # Choose a rig preset, Human rig. (Only needed if not doing smart autorig?)
#     # bpy.ops.arp.append_arp(rig_presets='human')
#
#     # Select the requested mess and then add smart rig
#     bpy.ops.object.select_all(action="DESELECT")
#     select_by_names([rig_data["layer"]])
#
#     bpy.context.view_layer.objects.active = bpy.context.scene.objects.get(
#         rig_data["layer"]
#     )
#
#     ov = bpy.context.copy()
#     ov["area"] = [a for a in bpy.context.screen.areas if a.type == "VIEW_3D"][0]
#     bpy.ops.id.get_selected_objects()
#
#     # then the markers need to be done by hand
#     autorig_map = {
#         "neck": "neck_loc",
#         "chin": "chin_loc",
#         "shoulder-left": "shoulder_loc",
#         "shoulder-right": "shoulder_loc_sym",
#         "wrist-left": "hand_loc",
#         "wrist-right": "hand_loc_sym",
#         "spine-root": "root_loc",
#         "ankle-left": "foot_loc",
#         "ankle-right": "foot_loc_sym",
#     }
#     import pdb
#
#     pdb.set_trace()
#
#     for marker in ["neck", "chin", "shoulder", "hand", "root", "foot"]:
#         autorig_marker_name = autorig_map[marker]
#         bpy.ops.id.add_maker(body_part=marker)
#
#     # in metres
#
#     # auto detect
#     bpy.ops.id.go_select()
#
#     # set spine number to 5
#
#     # generate The Rig (Click Match to Rig)
#     bpy.ops.arp.match_to_rig()
#
#     # Adjust Bone Shapes need to be done by hand
#
#     # Binding to mesh
#     ## Select all meshes
#     bpy.ops.object.select_all(action="DESELECT")
#     for obj in bpy.context.scene.objects:
#         obj.select_set(obj.type == "MESH")
#
#     ## also select the armature
#     for obj in bpy.context.scene.objects:
#         obj.select_set(obj.type == "ARMATURE")
#
#     ## TODO: use these settings
#     ## without preserve volume
#     ## with voxelise and scale fix
#
#     bpy.ops.arp.bind_to_rig()
#
#     # Now it should be done!
#     return True
#
#
# def get_bone(name):
#     """find a bone in blender"""
#     for bone in bpy.data.scenes["Scene"].bones_map:
#         if bone.source_bone == name:
#             print("found bone", name)
#             return bone
#     return None
#
#
# def get_bone_index(name):
#     """get a bone map index in blender"""
#     for i, bone in enumerate(bpy.data.scenes["Scene"].bones_map):
#         if bone.source_bone == name:
#             print("found bone", name, "at", i)
#             return i
#     return None
#
#
# def select_bones_by_names(armature, names):
#     """select bones by names in blender"""
#     print("select bones by names")
#     found = []
#     armature = [
#         x for x in bpy.data.objects if x.type == "ARMATURE" and x.name == armature
#     ][0]
#     pose_bones = armature.pose.bones
#     for pose_bone in pose_bones:
#         if pose_bone.name in names:
#             pose_bone.bone.select = True
#             # pose_bone.bone.active = True
#             found.append(pose_bone.name)
#             print("found bone", pose_bone.name)
#     if len(found) < len(names):
#         print("unable to find all names", [item for item in names if item not in found])
#
#
# def get_bone_by_name(armature, name):
#     """get bone by name in blender"""
#     armature = [
#         x for x in bpy.data.objects if x.type == "ARMATURE" and x.name == armature
#     ][0]
#     pose_bones = armature.pose.bones
#     for pose_bone in pose_bones:
#         if pose_bone.name == name:
#             return pose_bone.bone
#     return None
#
#
# def select_armature(name):
#     """select armature by name in blender"""
#     for obj in bpy.context.scene.objects:
#         found = (obj.type == "ARMATURE") and (obj.name == name)
#         if found:
#             print("selected", name)
#             obj.select_set(True)
#             return
#     print("Unable to find", name, "to select")
#
#
# def select_by_names(names):
#     """select objects by name in blender"""
#     found = []
#
#     for obj in bpy.context.scene.objects:
#         print("compared", obj.name, names)
#         if obj.name in names:
#             obj.select_set(True)
#             found.append(obj.name)
#             print("found", obj.name)
#     if len(found) < len(names):
#         print("unable to find all names", [item for item in names if item not in found])
#
#
# def deselect_all():
#     """deselect everything in blender"""
#     bpy.ops.object.select_all(action="DESELECT")
#
#
# def select_source_armature(armature_name):
#     """Select an armature (eg a track of bvh data)"""
#     deselect_all()
#     select_armature(armature_name)
#     bpy.ops.arp.pick_object(action="pick_source")
#
#
# def select_target_armature(name):
#     """Select the character armature we want to apply bvh data to"""
#     deselect_all()
#     select_armature(name)
#     # bpy.ops.arp.pick_object(action="pick_target")  # Doesn't appear to work, trying again Nov 2021
#     bpy.data.scenes["Scene"].target_rig = name
#
#
# def set_root_bone_mapping():
#     """
#     set the root bone mapping, eg which bone controls the motion of the skeleton (needed for moving across floors)
#     """
#     bone_index = get_bone_index("Hips")
#     # bone = bpy.data.scenes["Scene"].bones_map[bone_index]
#     select_bones_by_names("rig", ["c_root_master.x"])
#     bpy.ops.arp.pick_object(action="pick_bone")
#
#     scn = bpy.context.scene
#     # bones_map = scn.bones_map
#     scn.bones_map_index = bone_index
#     bpy.data.scenes["Scene"].bones_map[bone_index].set_as_root = True
#
#
# def redefine_rest_pose(source_armature_name):
#     """make the target mesh and the bvh skeleton bones match up better"""
#     bpy.ops.arp.redefine_rest_pose()
#     # select Head, Neck, LeftArm, LeftForeArm, RightArm, RightForeArm, RightUpLeg, LeftUpLeg, RightLeg, LeftLeg
#     # deselect_all()
#     select_bones_by_names(
#         source_armature_name,
#         [
#             "Head",
#             "Neck",
#             "LeftArm",
#             "LeftForeArm",
#             "RightArm",
#             "RightForeArm",
#             "RightUpLeg",
#             "LeftUpLeg",
#             "RightLeg",
#             "LeftLeg",
#             "LeftFoot",
#             "RightFoot",
#         ],
#     )
#
#     # Maybe need to do feet?
#     bpy.ops.arp.copy_bone_rest()  # copy selected bones
#     bpy.ops.arp.copy_raw_coordinates()  # apply
#
#
# def get_final_path(character, anim):
#     """Get path of the output mocap autorigged mesh from glamrig"""
#     p = Path("final", character["name"], character["name"] + "_" + anim)
#     p.parent.mkdir(parents=True, exist_ok=True)
#     return p.with_suffix(".glb")
#
#
# def get_publish_path(character, anim):
#     """Get path of the output mocap autorigged mesh from glamrig into godot"""
#     p = Path(publish_dir, character["name"], character["name"] + "_" + anim)
#     p.parent.mkdir(parents=True, exist_ok=True)
#     return p.with_suffix(".glb")
#
#
# def apply_mocap_character(character, animations, glamrig):
#     """Apply multiple mocap data to a character"""
#     print("start mocap apply")
#
#     raw_filename = "manual_rigged" / Path(character["rigged"])
#     loaded = load_3d(raw_filename)
#     if not loaded:
#         return False
#
#     print("import bvh", animations)
#     if len(animations.items()) > 1:
#         print("XXX: can only do one anim per model at the moment. Abort.")
#         return False
#     for anim, anim_details in animations.items():
#         if anim_details.get("rig"):
#             print(
#                 "XXX: Can not set per anim rig at the moment (have not implemented). Using global."
#             )
#         bvh_filename = "mocap_data" / Path(anim_details["mocap"])
#
#         # get some details of the bvh
#         with open(bvh_filename) as f:
#             mocap = Bvh(f.read())
#             bvh_frame_time = mocap.frame_time
#             bvh_fps = 1 / bvh_frame_time
#
#         bpy.ops.import_anim.bvh(
#             filepath=bvh_filename.as_posix(), use_fps_scale=True
#         )  # , global_scale=0.01)
#
#         # animation length (bvh length and also final blender animation length)
#         start = anim_details.get("start", None)
#         end = anim_details.get("end", None)
#         raw_mocap = Path(anim_details.get("mocap")).stem
#         raw_mocap_data = glamrig["mocap"]["raw"].get(raw_mocap)
#         if raw_mocap_data:
#             start = 0
#             end = raw_mocap_data.get("end") - raw_mocap_data.get("start")
#
#         # Frames: 251
#         # Frame Time: 0.008
#
#         blender_fps = bpy.context.scene.render.fps
#
#         bvh_duration = end / bvh_fps
#
#         new_frame_end = bvh_duration * blender_fps
#         print(
#             " old blender frame end",
#             bpy.data.scenes["Scene"].frame_end,
#             " new frame_end:",
#             new_frame_end,
#         )
#         # bpy.data.scenes["Scene"].frame_end = new_frame_end
#         scn = bpy.context.scene
#         scn.frame_start = 0
#         scn.frame_end = new_frame_end
#
#         # select source armature (bvh)
#         select_source_armature(bvh_filename.stem)
#
#         # select target armature (autorig)
#         select_target_armature("rig")
#
#         # auto-scale
#         print("auto-scale")
#         bpy.ops.arp.auto_scale()
#
#         print("building bones list...")
#         bpy.ops.arp.build_bones_list()
#
#         print("set the root bone mapping...")
#         set_root_bone_mapping()
#
#         print("redefine armatures rest pose...")
#         redefine_rest_pose(bvh_filename.stem)
#
#         # retarget!
#         print(f"retarget mocap data to character... ({0}:{new_frame_end})")
#         bpy.ops.arp.retarget(frame_start=start, frame_end=new_frame_end)
#
#     #    export_name = Path("final/countrykid_flourish_autotest-2021-11-6-1836.blend")
#     #    export_name = Path("final/countrykid_flourish_test.glb")
#     export_name = get_final_path(character, anim)
#     if export_name.exists():
#         logger.warning(f"{export_name} already exists.")
#     # bpy.ops.export_scene.gltf(filepath=export_name)
#     save_3d(export_name)
#     save_3d(export_name.with_suffix(".blend"))
#
#     print("done remap")
#     return True
#
#
# def add_animation_gltf(gltf: GLTF2):
#     """add a head turning animation"""
#     anim = Animation()
#     anim.name = "Look Left"
#
#     sampler = AnimationSampler()
#     sampler.input = 2
#     sampler.interpolation = ANIM_LINEAR
#     sampler.output = 3
#
#     channel = AnimationChannel()
#     channel.sampler = 0
#     channel.target = {"node": 0, "path": "rotation"}
#     anim.samplers.append(sampler)
#     anim.channels.append(channel)
#
#     gltf.animations.append(anim)
#
#     return gltf
#
#
# def add_animation_character_gltf(character, animations):
#     """Add some head turn animations to the GLB file (post mocap apply)
#     NOT USED
#     """
#     print("start mocap apply")
#     # character["rigged"] = "countrykid_rigged.blend"
#     if len(animations.items()) > 1:
#         print("XXX: can only do one anim per model at the moment. Abort.")
#         return False
#     for anim, anim_details in animations.items():
#         raw_filename = get_final_path(character, anim)
#         gltf = GLTF2.load(raw_filename)
#         if not gltf:
#             return False
#         gltf = add_animation_gltf(gltf)
#         output_filename = raw_filename.with_name(
#             raw_filename.stem + "_animated"
#         ).with_suffix(".glb")
#         gltf.save(output_filename)
#
#         import pdb
#
#         pdb.set_trace()
#
#
# def create_turn_head_animation(name, d):
#     """Create a new action with <name> and add a keyframe for the neck/head to turn <d> degrees."""
#     obj = bpy.context.active_object
#     obj.animation_data_create()
#
#     action = bpy.data.actions.new(name)
#     obj.animation_data.action = action
#
#     # select the bone
#     select_bones_by_names("rig", ["c_head.x"])
#
#     bpy.ops.object.mode_set(mode="POSE")
#     thebone = bpy.context.object.pose.bones["c_head.x"]
#     thebone.rotation_euler = (0.0, radians(d), 0.0)
#     thebone.keyframe_insert(data_path="rotation_euler", frame=0)
#     return action
#
#
# def create_animation_bpy():
#     """Add several animations to the blender file to make it easier to do animation tree blends in godot"""
#     bpy.context.view_layer.objects.active = bpy.data.objects["rig"]
#
#     create_turn_head_animation("TurnLeft", 45)
#     create_turn_head_animation("TurnRight", -45)
#
#
# def add_animation_character(character):
#     """Add some head turn animations to the blend file (pre mocap apply)"""
#     print("start animation apply")
#     raw_filename = "manual_rigged" / Path(character["rigged"])
#
#     loaded = load_3d(raw_filename)
#     if not loaded:
#         return False
#
#     create_animation_bpy()
#
#     output_filename = raw_filename.with_name(
#         raw_filename.stem + "_animated"
#     ).with_suffix(".blend")
#     save_3d(output_filename)
#
#
# def publish(character, animations):
#     """Move the character animations to the publish directory (ie into the game itself)"""
#     print("publish file")
#     character_name = character["name"]
#
#     for animation in animations:
#         import_path = get_final_path(character, animation)
#         export_name = get_publish_path(character, animation)
#         tscn_name = export_name.with_suffix(".tscn")
#
#         disabled = animations[animation].get("disabled-layers")
#         disabled = f"disabled_layers = {disabled}" if disabled else ""
#         autoplay = animations[animation].get("autoplay", False)
#
#         force = not tscn_name.exists()
#         force = True
#         if force:
#             # base_gd = Path(publish_dir, "character.gd")
#             script_gd = export_name.with_suffix(".gd")
#             # shutil.copy(base_gd, script_gd)
#             with open(script_gd, "w") as f:
#                 f.write(
#                     f"""extends "res://Animations/character.gd"
#
# func _ready():
#     object_name = "{character_name}_{animation}"
#     character_name = "{character_name}"
#     autoplay = "{autoplay}"
#     {disabled}
#     if autoplay:
#         loop_animation()
# """
#                 )
#
#             with open(tscn_name, "w") as f:
#                 f.write(
#                     f"""
#     [gd_scene load_steps=3 format=2]
#
#     [ext_resource path="res://Animations/{character_name}/{script_gd.stem}.gd" type="Script" id=1]
#     [ext_resource path="res://Animations/{character_name}/{character_name}_{animation}.glb" type="PackedScene" id=2]
#
#     [node name="Spatial" type="Spatial"]
#     script = ExtResource( 1 )
#
#     [node name="{character_name}_{animation}" parent="." instance=ExtResource( 2 )]
#                 """
#                 )
#
#         shutil.copy(import_path, export_name)  # For Python 3.8+.
#         print("published")
#     return True
#
#
# def process_character(character, stages, animations, glamrig):
#     """Execute the requested actions on this character
#     character: details about current character
#     stages: the stages to run
#     glamrig: the raw yaml data (ie the complete project)
#     """
#     character_name = character["name"]
#     if not animations:
#         logger.warning(f"No animations available for {character_name}")
#         return
#     logger.info(
#         f"Going to {character['name']}->stages {stages}->animations {animations}"
#     )
#     success = True
#     for stage in stages:
#         if stage == "import":
#             print("import")
#             success = import_character(character)
#         elif stage == "rig":
#             print("rig")
#             success = autorig_character(character)
#         elif stage == "mocap":
#             print("mocap", animations)
#             success = apply_mocap_character(character, animations, glamrig)
#         elif stage == "animation":
#             print("animation", character)
#             success = add_animation_character(character)
#         elif stage == "publish":
#             print("publish")
#             success = publish(character, animations)
#         if not success:
#             logger.error("Failed. Aborting.")
#
#
# def main(yamlname, characters_alias, stages_alias, animations_alias):
#     """Expand aliases into trees and execute"""
#     logger.info(f"Loading yaml file {yamlname}.")
#     with open(yamlname) as file:
#         # The FullLoader parameter handles the conversion from YAML
#         # scalar values to Python the dictionary format
#         glamrig = yaml.load(file, Loader=yaml.FullLoader)
#
#     if characters_alias not in glamrig["characters"]:
#         logger.warning(
#             f"No character(s) {characters_alias} in yaml stages {glamrig['characters'].keys()}"
#         )
#         return
#     if stages_alias not in glamrig["stages"]:
#         logger.warning(
#             f"No stage(s) {stages_alias} in yaml stages {glamrig['stages'].keys()}"
#         )
#         return
#
#     characters = glamrig["characters"][characters_alias]
#     logger.info("Will operate on", characters)
#     stages = glamrig["stages"][stages_alias]
#     for character_name in characters:
#         character = glamrig[character_name]
#         animations = expand_animations_alias(character, animations_alias)
#         process_character(character, stages, animations, glamrig)
#
#
# if __name__ == "__main__":
#     args = sys.argv[-4:]
#     logger.info(
#         "Starting glamrig with the following arguments: ", sys.argv, args, len(args)
#     )
#     if len(args) != 4:
#         print("Usage: python3 -m glamrig <characters> <stages> <animations>")
#     else:
#         yaml_name = Path("/home/luke/Projects/thebeat-client/animations/thebeat.yaml")
#         app, sys_characters, sys_stages, sys_animations = args
#         main(yaml_name, sys_characters, sys_stages, sys_animations)
