"""


Sculpt Operators
****************

:func:`brush_stroke`

:func:`detail_flood_fill`

:func:`dirty_mask`

:func:`dynamic_topology_toggle`

:func:`face_set_change_visibility`

:func:`face_sets_create`

:func:`face_sets_init`

:func:`face_sets_randomize_colors`

:func:`mask_expand`

:func:`mask_filter`

:func:`mesh_filter`

:func:`optimize`

:func:`sample_detail_size`

:func:`sculptmode_toggle`

:func:`set_detail_size`

:func:`set_persistent_base`

:func:`set_pivot_position`

:func:`symmetrize`

:func:`uv_sculpt_stroke`

"""

import typing

def brush_stroke(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, mode: str = 'NORMAL', ignore_background_click: bool = False) -> None:

  """

  Sculpt a stroke into the geometry

  """

  ...

def detail_flood_fill() -> None:

  """

  Flood fill the mesh with the selected detail setting

  """

  ...

def dirty_mask(dirty_only: bool = False) -> None:

  """

  Generates a mask based on the geometry cavity and pointiness

  """

  ...

def dynamic_topology_toggle() -> None:

  """

  Dynamic topology alters the mesh topology while sculpting

  """

  ...

def face_set_change_visibility(mode: str = 'TOGGLE') -> None:

  """

  Change the visibility of the Face Sets of the sculpt

  """

  ...

def face_sets_create(mode: str = 'MASKED') -> None:

  """

  Create a new Face Set

  """

  ...

def face_sets_init(mode: str = 'LOOSE_PARTS', threshold: float = 0.5) -> None:

  """

  Initializes all Face Sets in the mesh

  """

  ...

def face_sets_randomize_colors() -> None:

  """

  Generates a new set of random colors to render the Face Sets in the viewport

  """

  ...

def mask_expand(invert: bool = True, use_cursor: bool = True, update_pivot: bool = True, smooth_iterations: int = 2, mask_speed: int = 5, use_normals: bool = True, keep_previous_mask: bool = False, edge_sensitivity: int = 300, create_face_set: bool = False) -> None:

  """

  Expands a mask from the initial active vertex under the cursor

  """

  ...

def mask_filter(filter_type: str = 'SMOOTH', iterations: int = 1, auto_iteration_count: bool = False) -> None:

  """

  Applies a filter to modify the current mask

  """

  ...

def mesh_filter(type: str = 'INFLATE', strength: float = 1.0, deform_axis: typing.Set[str] = {'X', 'Y', 'Z'}, use_face_sets: bool = False, surface_smooth_shape_preservation: float = 0.5, surface_smooth_current_vertex: float = 0.5, sharpen_smooth_ratio: float = 0.35) -> None:

  """

  Applies a filter to modify the current mesh

  """

  ...

def optimize() -> None:

  """

  Recalculate the sculpt BVH to improve performance

  """

  ...

def sample_detail_size(location: typing.Tuple[int, int] = (0, 0), mode: str = 'DYNTOPO') -> None:

  """

  Sample the mesh detail on clicked point

  """

  ...

def sculptmode_toggle() -> None:

  """

  Toggle sculpt mode in 3D view

  """

  ...

def set_detail_size() -> None:

  """

  Set the mesh detail (either relative or constant one, depending on current dyntopo mode)

  """

  ...

def set_persistent_base() -> None:

  """

  Reset the copy of the mesh that is being sculpted on

  """

  ...

def set_pivot_position(mode: str = 'UNMASKED', mouse_x: float = 0.0, mouse_y: float = 0.0) -> None:

  """

  Sets the sculpt transform pivot position

  """

  ...

def symmetrize(merge_tolerance: float = 0.001) -> None:

  """

  Symmetrize the topology modifications

  """

  ...

def uv_sculpt_stroke(mode: str = 'NORMAL') -> None:

  """

  Sculpt UVs using a brush

  """

  ...
