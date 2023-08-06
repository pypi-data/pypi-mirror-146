"""


GPU Shader (gpu.shader)
***********************

This module provides access to GPUShader internal functions.


Built-in shaders
================

All built-in shaders have the ``mat4 ModelViewProjectionMatrix`` uniform.
The value of it can only be modified using the :class:`gpu.matrix` module.

2D_UNIFORM_COLOR:
  attributes: vec3 pos
uniforms: vec4 color

2D_FLAT_COLOR:
  attributes: vec3 pos, vec4 color
uniforms: -

2D_SMOOTH_COLOR:
  attributes: vec3 pos, vec4 color
uniforms: -

2D_IMAGE:
  attributes: vec3 pos, vec2 texCoord
uniforms: sampler2D image

3D_UNIFORM_COLOR:
  attributes: vec3 pos
uniforms: vec4 color

3D_FLAT_COLOR:
  attributes: vec3 pos, vec4 color
uniforms: -

3D_SMOOTH_COLOR:
  attributes: vec3 pos, vec4 color
uniforms: -

:func:`code_from_builtin`

:func:`from_builtin`

:func:`unbind`

"""

import typing

import bpy

def code_from_builtin(shader_name: str) -> typing.Dict[str, typing.Any]:

  """

  Exposes the internal shader code for query.

  """

  ...

def from_builtin(shader_name: str) -> bpy.types.GPUShader:

  """

  Shaders that are embedded in the blender internal code.
They all read the uniform 'mat4 ModelViewProjectionMatrix', which can be edited by the 'gpu.matrix' module.
For more details, you can check the shader code with the function 'gpu.shader.code_from_builtin';

  """

  ...

def unbind() -> None:

  """

  Unbind the bound shader object.

  """

  ...
