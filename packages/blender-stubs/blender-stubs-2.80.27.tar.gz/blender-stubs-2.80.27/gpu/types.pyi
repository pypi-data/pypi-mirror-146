"""


GPU Types (gpu.types)
*********************

:class:`GPUBatch`

:class:`GPUIndexBuf`

:class:`GPUOffScreen`

:class:`GPUShader`

:class:`GPUVertBuf`

:class:`GPUVertFormat`

"""

import typing

import mathutils

import bpy

class GPUBatch:

  """

  Reusable container for drawable geometry.

  """

  def __init__(self, type: str, buf: GPUVertBuf, elem: GPUIndexBuf = None) -> None:

    """

    :arg type:        
      One of these primitive types: {
*POINTS*,
*LINES*,
*TRIS*,
*LINE_STRIP*,
*LINE_LOOP*,
*TRI_STRIP*,
*TRI_FAN*,
*LINES_ADJ*,
*TRIS_ADJ*,
*LINE_STRIP_ADJ* }

    :type type:       
      *str*

    :arg buf:         
      Vertex buffer containing all or some of the attributes required for drawing.

    :type buf:        
      :class:`gpu.types.GPUVertBuf`

    :arg elem:        
      An optional index buffer.

    :type elem:       
      :class:`gpu.types.GPUIndexBuf`

    """

    ...

  def draw(self, program: GPUShader = None) -> None:

    """

    Run the drawing program with the parameters assigned to the batch.

    """

    ...

  def program_set(self, program: GPUShader) -> None:

    """

    Assign a shader to this batch that will be used for drawing when not overwritten later.
Note: This method has to be called in the draw context that the batch will be drawn in.
This function does not need to be called when you always set the shader when calling *batch.draw*.

    """

    ...

  def vertbuf_add(self, buf: GPUVertBuf) -> None:

    """

    Add another vertex buffer to the Batch.
It is not possible to add more vertices to the batch using this method.
Instead it can be used to add more attributes to the existing vertices.
A good use case would be when you have a separate
vertex buffer for vertex positions and vertex normals.
Current a batch can have at most 4 vertex buffers.

    """

    ...

class GPUIndexBuf:

  """

  Contains an index buffer.

  """

  def __init__(self, type: str, seq: typing.Any) -> None:

    """

    :param type:      
      One of these primitive types: {
*POINTS*,
*LINES*,
*TRIS*,
*LINE_STRIP_ADJ* }

    :type type:       
      *str*

    :param seq:       
      Indices this index buffer will contain.
Whether a 1D or 2D sequence is required depends on the type.
Optionally the sequence can support the buffer protocol.

    :type seq:        
      1D or 2D sequence

    """

    ...

class GPUOffScreen:

  """

  This object gives access to off screen buffers.

  """

  def __init__(self, width: int, height: int, samples: int = 0) -> None:

    """

    :arg width:       
      Horizontal dimension of the buffer.

    :type width:      
      *int*

    :arg height:      
      Vertical dimension of the buffer.

    :type height:     
      *int*

    :arg samples:     
      OpenGL samples to use for MSAA or zero to disable.

    :type samples:    
      *int*

    """

    ...

  def bind(self, save: bool = True) -> None:

    """

    Bind the offscreen object.
To make sure that the offscreen gets unbind whether an exception occurs or not, pack it into a *with* statement.

    """

    ...

  def draw_view3d(self, scene: bpy.types.Scene, view3d: bpy.types.SpaceView3D, region: bpy.types.Region, view_matrix: mathutils.Matrix, projection_matrix: mathutils.Matrix) -> None:

    """

    Draw the 3d viewport in the offscreen object.

    """

    ...

  def free(self) -> None:

    """

    Free the offscreen object.
The framebuffer, texture and render objects will no longer be accessible.

    """

    ...

  def unbind(self, restore: bool = True) -> None:

    """

    Unbind the offscreen object.

    """

    ...

  color_texture: int = ...

  """

  OpenGL bindcode for the color texture.

  """

  height: int = ...

  """

  Height of the texture.

  """

  width: int = ...

  """

  Width of the texture.

  """

class GPUShader:

  """

  GPUShader combines multiple GLSL shaders into a program used for drawing.
It must contain a vertex and fragment shaders, with an optional geometry shader.

  The GLSL #version directive is automatically included at the top of shaders, and set to 330.
Some preprocessor directives are automatically added according to the Operating System or availability:
``GPU_ATI``, ``GPU_NVIDIA`` and ``GPU_INTEL``.

  The following extensions are enabled by default if supported by the GPU:
``GL_ARB_texture_gather`` and ``GL_ARB_texture_query_lod``.

  To debug shaders, use the --debug-gpu-shaders command line option   to see full GLSL shader compilation and linking errors.

  """

  def __init__(self, vertexcode: str, fragcode: typing.Any, geocode: typing.Any = None, libcode: typing.Any = None, defines: typing.Any = None) -> None:

    """

    :param vertexcode:
      Vertex shader code.

    :type vertexcode: 
      str

    :param fragcode:  
      Fragment shader code.

    :type value:      
      str

    :param geocode:   
      Geometry shader code.

    :type value:      
      str

    :param libcode:   
      Code with functions and presets to be shared between shaders.

    :type value:      
      str

    :param defines:   
      Preprocessor directives.

    :type value:      
      str

    """

    ...

  def attr_from_name(self, name: str) -> int:

    """

    Get attribute location by name.

    """

    ...

  def bind(self) -> None:

    """

    Bind the shader object. Required to be able to change uniforms of this shader.

    """

    ...

  def calc_format(self) -> typing.Any:

    """

    Build a new format based on the attributes of the shader.

    """

    ...

  def uniform_block_from_name(self, name: str) -> int:

    """

    Get uniform block location by name.

    """

    ...

  def uniform_bool(self, name: str, seq: typing.Sequence[bool]) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_float(self, name: str, value: typing.Any) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_from_name(self, name: str) -> int:

    """

    Get uniform location by name.

    """

    ...

  def uniform_int(self, name: str, seq: typing.Sequence[typing.Any]) -> None:

    """

    Specify the value of a uniform variable for the current program object.

    """

    ...

  def uniform_vector_float(self, location: int, buffer: typing.Sequence[float], length: int, count: int) -> None:

    """

    Set the buffer to fill the uniform.

    """

    ...

  def uniform_vector_int(self, location: typing.Any, buffer: typing.Any, length: typing.Any, count: typing.Any) -> None:

    """

    See GPUShader.uniform_vector_float(...) description.

    """

    ...

  program: int = ...

  """

  The name of the program object for use by the OpenGL API (read-only).

  """

class GPUVertBuf:

  """

  Contains a VBO.

  """

  def __init__(self, len: typing.Any, format: typing.Any) -> None:

    """

    :param len:       
      Amount of vertices that will fit into this buffer.

    :type type:       
      *int*

    :param format:    
      Vertex format.

    :type buf:        
      :class:`gpu.types.GPUVertFormat`

    """

    ...

  def attr_fill(self, id: typing.Union[int, str], data: typing.Sequence[typing.Any]) -> None:

    """

    Insert data into the buffer for a single attribute.

    """

    ...

class GPUVertFormat:

  """

  This object contains information about the structure of a vertex buffer.

  """

  def attr_add(self, id: str, comp_type: str, len: int, fetch_mode: str) -> None:

    """

    Add a new attribute to the format.

    """

    ...
