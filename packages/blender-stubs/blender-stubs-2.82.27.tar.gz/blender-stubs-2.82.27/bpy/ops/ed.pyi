"""


Ed Operators
************

:func:`flush_edits`

:func:`redo`

:func:`undo`

:func:`undo_history`

:func:`undo_push`

:func:`undo_redo`

"""

import typing

def flush_edits() -> None:

  """

  Flush edit data from active editing modes

  """

  ...

def redo() -> None:

  """

  Redo previous action

  """

  ...

def undo() -> None:

  """

  Undo previous action

  """

  ...

def undo_history(item: int = 0) -> None:

  """

  Redo specific action in history

  """

  ...

def undo_push(message: str = 'Add an undo step *argsfunction may be moved*args') -> None:

  """

  Add an undo state (internal use only)

  """

  ...

def undo_redo() -> None:

  """

  Undo and redo previous action

  """

  ...
