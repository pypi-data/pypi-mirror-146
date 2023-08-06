"""


Sculpt Operators
****************

:func:`brush_stroke`

:func:`detail_flood_fill`

:func:`dynamic_topology_toggle`

:func:`optimize`

:func:`sample_detail_size`

:func:`sculptmode_toggle`

:func:`set_detail_size`

:func:`set_persistent_base`

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

def dynamic_topology_toggle() -> None:

  """

  Dynamic topology alters the mesh topology while sculpting

  """

  ...

def optimize() -> None:

  """

  Recalculate the sculpt BVH to improve performance

  """

  ...

def sample_detail_size(location: typing.Tuple[int, int] = (0, 0)) -> None:

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

def symmetrize() -> None:

  """

  Symmetrize the topology modifications

  """

  ...

def uv_sculpt_stroke(mode: str = 'NORMAL') -> None:

  """

  Sculpt UVs using a brush

  """

  ...
