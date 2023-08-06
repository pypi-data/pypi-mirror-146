"""


Cycles Operators
****************

:func:`add_aov`

:func:`denoise_animation`

:func:`merge_images`

:func:`remove_aov`

:func:`use_shading_nodes`

"""

import typing

def add_aov() -> None:

  """

  Add an AOV pass

  """

  ...

def denoise_animation(input_filepath: str = '', output_filepath: str = '') -> None:

  """

  Denoise rendered animation sequence using current scene and view layer settings. Requires denoising data passes and output to OpenEXR multilayer files

  """

  ...

def merge_images(input_filepath1: str = '', input_filepath2: str = '', output_filepath: str = '') -> None:

  """

  Combine OpenEXR multilayer images rendered with different sampleranges into one image with reduced noise

  """

  ...

def remove_aov() -> None:

  """

  Remove an AOV pass

  """

  ...

def use_shading_nodes() -> None:

  """

  Enable nodes on a material, world or light

  """

  ...
