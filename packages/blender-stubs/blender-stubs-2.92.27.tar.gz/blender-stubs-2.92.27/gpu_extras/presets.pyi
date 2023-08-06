"""


gpu_extras submodule (gpu_extras.presets)
*****************************************

:func:`draw_circle_2d`

:func:`draw_texture_2d`

"""

import typing

import mathutils

def draw_circle_2d(position: mathutils.Vector, color: typing.Tuple[typing.Any, ...], radius: float, segments: int = 32) -> None:

  """

  Draw a circle.

  """

  ...

def draw_texture_2d(texture_id: int, position: mathutils.Vector, width: float, height: float) -> None:

  """

  Draw a 2d texture.

  """

  ...
