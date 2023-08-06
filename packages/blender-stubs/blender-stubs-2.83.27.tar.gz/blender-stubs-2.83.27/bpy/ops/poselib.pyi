"""


Poselib Operators
*****************

:func:`action_sanitize`

:func:`apply_pose`

:func:`browse_interactive`

:func:`new`

:func:`pose_add`

:func:`pose_move`

:func:`pose_remove`

:func:`pose_rename`

:func:`unlink`

"""

import typing

def action_sanitize() -> None:

  """

  Make action suitable for use as a Pose Library

  """

  ...

def apply_pose(pose_index: int = -1) -> None:

  """

  Apply specified Pose Library pose to the rig

  """

  ...

def browse_interactive(pose_index: int = -1) -> None:

  """

  Interactively browse poses in 3D-View

  """

  ...

def new() -> None:

  """

  Add New Pose Library to active Object

  """

  ...

def pose_add(frame: int = 1, name: str = 'Pose') -> None:

  """

  Add the current Pose to the active Pose Library

  """

  ...

def pose_move(pose: str = '', direction: str = 'UP') -> None:

  """

  Move the pose up or down in the active Pose Library

  """

  ...

def pose_remove(pose: str = '') -> None:

  """

  Remove nth pose from the active Pose Library

  """

  ...

def pose_rename(name: str = 'RenamedPose', pose: str = '') -> None:

  """

  Rename specified pose from the active Pose Library

  """

  ...

def unlink() -> None:

  """

  Remove Pose Library from active Object

  """

  ...
