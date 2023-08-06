"""


Application Icons (bpy.app.icons)
*********************************

:func:`new_triangles`

:func:`new_triangles_from_file`

:func:`release`

"""

import typing

def new_triangles(range: typing.Tuple[typing.Any, ...], coords: typing.Any, colors: typing.Any) -> int:

  ...

def new_triangles_from_file(filename: str) -> int:

  ...

def release(icon_id: typing.Any) -> None:

  ...
