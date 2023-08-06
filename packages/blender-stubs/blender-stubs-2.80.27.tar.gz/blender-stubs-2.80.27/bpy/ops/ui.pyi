"""


Ui Operators
************

:func:`assign_default_button`

:func:`button_execute`

:func:`copy_data_path_button`

:func:`copy_python_command_button`

:func:`copy_to_selected_button`

:func:`drop_color`

:func:`editsource`

:func:`edittranslation_init`

:func:`eyedropper_color`

:func:`eyedropper_colorramp`

:func:`eyedropper_colorramp_point`

:func:`eyedropper_depth`

:func:`eyedropper_driver`

:func:`eyedropper_id`

:func:`jump_to_target_button`

:func:`override_remove_button`

:func:`override_type_set_button`

:func:`reloadtranslation`

:func:`reports_to_textblock`

:func:`reset_default_button`

:func:`unset_property_button`

"""

import typing

def assign_default_button() -> None:

  """

  Set this property's current value as the new default

  """

  ...

def button_execute(skip_depressed: bool = False) -> None:

  """

  Presses active button

  """

  ...

def copy_data_path_button(full_path: bool = False) -> None:

  """

  Copy the RNA data path for this property to the clipboard

  """

  ...

def copy_python_command_button() -> None:

  """

  Copy the Python command matching this button

  """

  ...

def copy_to_selected_button(all: bool = True) -> None:

  """

  Copy property from this object to selected objects or bones

  """

  ...

def drop_color(color: typing.Tuple[float, float, float] = (0.0, 0.0, 0.0), gamma: bool = False) -> None:

  """

  Drop colors to buttons

  """

  ...

def editsource() -> None:

  """

  Edit UI source code of the active button

  """

  ...

def edittranslation_init() -> None:

  """

  Edit i18n in current language for the active button

  """

  ...

def eyedropper_color(use_accumulate: bool = True) -> None:

  """

  Sample a color from the Blender Window to store in a property

  """

  ...

def eyedropper_colorramp() -> None:

  """

  Sample a color band

  """

  ...

def eyedropper_colorramp_point() -> None:

  """

  Point-sample a color band

  """

  ...

def eyedropper_depth() -> None:

  """

  Sample depth from the 3D view

  """

  ...

def eyedropper_driver(mapping_type: str = 'SINGLE_MANY') -> None:

  """

  Pick a property to use as a driver target

  """

  ...

def eyedropper_id() -> None:

  """

  Sample a data-block from the 3D View to store in a property

  """

  ...

def jump_to_target_button() -> None:

  """

  Switch to the target object or bone

  """

  ...

def override_remove_button(all: bool = True) -> None:

  """

  Remove an override operation

  """

  ...

def override_type_set_button(all: bool = True, type: str = 'REPLACE') -> None:

  """

  Create an override operation, or set the type of an existing one

  """

  ...

def reloadtranslation() -> None:

  """

  Force a full reload of UI translation

  """

  ...

def reports_to_textblock() -> None:

  """

  Write the reports

  """

  ...

def reset_default_button(all: bool = True) -> None:

  """

  Reset this property's value to its default value

  """

  ...

def unset_property_button() -> None:

  """

  Clear the property and use default or generated value in operators

  """

  ...
