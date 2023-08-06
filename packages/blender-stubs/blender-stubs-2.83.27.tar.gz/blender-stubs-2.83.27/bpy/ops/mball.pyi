"""


Mball Operators
***************

:func:`delete_metaelems`

:func:`duplicate_metaelems`

:func:`duplicate_move`

:func:`hide_metaelems`

:func:`reveal_metaelems`

:func:`select_all`

:func:`select_random_metaelems`

:func:`select_similar`

"""

import typing

def delete_metaelems() -> None:

  """

  Delete selected metaelement(s)

  """

  ...

def duplicate_metaelems() -> None:

  """

  Duplicate selected metaelement(s)

  """

  ...

def duplicate_move(MBALL_OT_duplicate_metaelems: MBALL_OT_duplicate_metaelems = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Make copies of the selected metaelements and move them

  """

  ...

def hide_metaelems(unselected: bool = False) -> None:

  """

  Hide (un)selected metaelement(s)

  """

  ...

def reveal_metaelems(select: bool = True) -> None:

  """

  Reveal all hidden metaelements

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all meta elements

  """

  ...

def select_random_metaelems(percent: float = 50.0, seed: int = 0, action: str = 'SELECT') -> None:

  """

  Randomly select metaelements

  """

  ...

def select_similar(type: str = 'TYPE', threshold: float = 0.1) -> None:

  """

  Select similar metaballs by property types

  """

  ...
