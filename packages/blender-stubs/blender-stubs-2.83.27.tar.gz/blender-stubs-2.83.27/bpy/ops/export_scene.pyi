"""


Export Scene Operators
**********************

:func:`fbx`

:func:`gltf`

they're pushed onto NLA tracks with the same name.
When off, all the currently assigned actions become one glTF animation

  :type export_nla_strips:
    boolean, (optional)

  :arg export_def_bones:
    Export Deformation Bones Only, Export Deformation bones only (and needed bones for hierarchy)

  :type export_def_bones:
    boolean, (optional)

  :arg export_current_frame:
    Use Current Frame, Export the scene in the current animation frame

  :type export_current_frame:
    boolean, (optional)

  :arg export_skins:
    Skinning, Export skinning (armature) data

  :type export_skins:
    boolean, (optional)

  :arg export_all_influences:
    Include All Bone Influences, Allow >4 joint vertex influences. Models may appear incorrectly in many viewers

  :type export_all_influences:
    boolean, (optional)

  :arg export_morph:
    Shape Keys, Export shape keys (morph targets)

  :type export_morph:
    boolean, (optional)

  :arg export_morph_normal:
    Shape Key Normals, Export vertex normals with shape keys (morph targets)

  :type export_morph_normal:
    boolean, (optional)

  :arg export_morph_tangent:
    Shape Key Tangents, Export vertex tangents with shape keys (morph targets)

  :type export_morph_tangent:
    boolean, (optional)

  :arg export_lights:
    Punctual Lights, Export directional, point, and spot lights. Uses "KHR_lights_punctual" glTF extension

  :type export_lights:
    boolean, (optional)

  :arg export_displacement:
    Displacement Textures (EXPERIMENTAL), EXPERIMENTAL: Export displacement textures. Uses incomplete "KHR_materials_displacement" glTF extension

  :type export_displacement:
    boolean, (optional)

  :arg will_save_settings:
    Remember Export Settings, Store glTF export settings in the Blender project

  :type will_save_settings:
    boolean, (optional)

  :arg filepath:    
    File Path, Filepath used for exporting the file

  :type filepath:   
    string, (optional, never None)

  :arg check_existing:
    Check Existing, Check and warn on overwriting existing files

  :type check_existing:
    boolean, (optional)

  :arg filter_glob: 
    filter_glob

  :type filter_glob:
    string, (optional, never None)

  :file:            
    `addons/io_scene_gltf2/__init__.py:392 <https://developer.blender.org/diffusion/BA/addons/io_scene_gltf2/__init__.py$392>`_

:func:`obj`

:func:`x3d`

"""

import typing

def fbx(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.fbx', use_selection: bool = False, use_active_collection: bool = False, global_scale: float = 1.0, apply_unit_scale: bool = True, apply_scale_options: str = 'FBX_SCALE_NONE', bake_space_transform: bool = False, object_types: typing.Set[str] = {'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}, use_mesh_modifiers: bool = True, use_mesh_modifiers_render: bool = True, mesh_smooth_type: str = 'OFF', use_subsurf: bool = False, use_mesh_edges: bool = False, use_tspace: bool = False, use_custom_props: bool = False, add_leaf_bones: bool = True, primary_bone_axis: str = 'Y', secondary_bone_axis: str = 'X', use_armature_deform_only: bool = False, armature_nodetype: str = 'NULL', bake_anim: bool = True, bake_anim_use_all_bones: bool = True, bake_anim_use_nla_strips: bool = True, bake_anim_use_all_actions: bool = True, bake_anim_force_startend_keying: bool = True, bake_anim_step: float = 1.0, bake_anim_simplify_factor: float = 1.0, path_mode: str = 'AUTO', embed_textures: bool = False, batch_mode: str = 'OFF', use_batch_own_dir: bool = True, use_metadata: bool = True, axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Write a FBX file

  """

  ...

def gltf(export_format: str = 'GLB', ui_tab: str = 'GENERAL', export_copyright: str = '', export_image_format: str = 'AUTO', export_texture_dir: str = '', export_texcoords: bool = True, export_normals: bool = True, export_draco_mesh_compression_enable: bool = False, export_draco_mesh_compression_level: int = 6, export_draco_position_quantization: int = 14, export_draco_normal_quantization: int = 10, export_draco_texcoord_quantization: int = 12, export_draco_generic_quantization: int = 12, export_tangents: bool = False, export_materials: bool = True, export_colors: bool = True, export_cameras: bool = False, export_selected: bool = False, use_selection: bool = False, export_extras: bool = False, export_yup: bool = True, export_apply: bool = False, export_animations: bool = True, export_frame_range: bool = True, export_frame_step: int = 1, export_force_sampling: bool = True, export_nla_strips: typing.Any = True, export_def_bones: typing.Any = False, export_current_frame: typing.Any = False, export_skins: typing.Any = True, export_all_influences: typing.Any = False, export_morph: typing.Any = True, export_morph_normal: typing.Any = True, export_morph_tangent: typing.Any = False, export_lights: typing.Any = False, export_displacement: typing.Any = False, will_save_settings: typing.Any = False, filepath: typing.Any = '', check_existing: typing.Any = True, filter_glob: typing.Any = '*args.glb;*args.gltf') -> None:

  """

  Export scene as glTF 2.0 file

  """

  ...

def obj(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.obj;*args.mtl', use_selection: bool = False, use_animation: bool = False, use_mesh_modifiers: bool = True, use_edges: bool = True, use_smooth_groups: bool = False, use_smooth_groups_bitflags: bool = False, use_normals: bool = True, use_uvs: bool = True, use_materials: bool = True, use_triangles: bool = False, use_nurbs: bool = False, use_vertex_groups: bool = False, use_blen_objects: bool = True, group_by_object: bool = False, group_by_material: bool = False, keep_vertex_order: bool = False, global_scale: float = 1.0, path_mode: str = 'AUTO', axis_forward: str = '-Z', axis_up: str = 'Y') -> None:

  """

  Save a Wavefront OBJ File

  """

  ...

def x3d(filepath: str = '', check_existing: bool = True, filter_glob: str = '*args.x3d', use_selection: bool = False, use_mesh_modifiers: bool = True, use_triangulate: bool = False, use_normals: bool = False, use_compress: bool = False, use_hierarchy: bool = True, name_decorations: bool = True, use_h3d: bool = False, global_scale: float = 1.0, path_mode: str = 'AUTO', axis_forward: str = 'Z', axis_up: str = 'Y') -> None:

  """

  Export selection to Extensible 3D file (.x3d)

  """

  ...
