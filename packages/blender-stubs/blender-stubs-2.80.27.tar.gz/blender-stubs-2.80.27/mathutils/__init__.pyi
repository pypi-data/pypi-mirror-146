"""


Math Types & Utilities (mathutils)
**********************************

This module provides access to math operations.

Note: Classes, methods and attributes that accept vectors also accept other numeric sequences,
such as tuples, lists.

Submodules:

The :mod:`mathutils` module provides the following classes:

* :class:`Color`,

* :class:`Euler`,

* :class:`Matrix`,

* :class:`Quaternion`,

* :class:`Vector`,

.. code::

  import mathutils
  from math import radians

  vec = mathutils.Vector((1.0, 2.0, 3.0))

  mat_rot = mathutils.Matrix.Rotation(radians(90.0), 4, 'X')
  mat_trans = mathutils.Matrix.Translation(vec)

  mat = mat_trans @ mat_rot
  mat.invert()

  mat3 = mat.to_3x3()
  quat1 = mat.to_quaternion()
  quat2 = mat3.to_quaternion()

  quat_diff = quat1.rotation_difference(quat2)

  print(quat_diff.angle)

:class:`Color`

:class:`Euler`

:class:`Matrix`

:class:`Quaternion`

:class:`Vector`

"""

from . import noise

from . import kdtree

from . import interpolate

from . import geometry

from . import bvhtree

import typing

class Color:

  """

  This object gives access to Colors in Blender.

  .. code::

    import mathutils

    # color values are represented as RGB values from 0 - 1, this is blue
    col = mathutils.Color((0.0, 0.0, 1.0))

    # as well as r/g/b attribute access you can adjust them by h/s/v
    col.s *= 0.5

    # you can access its components by attribute or index
    print("Color R:", col.r)
    print("Color G:", col[1])
    print("Color B:", col[-1])
    print("Color HSV: %.2f, %.2f, %.2f", col[:])


    # components of an existing color can be set
    col[:] = 0.0, 0.5, 1.0

    # components of an existing color can use slice notation to get a tuple
    print("Values: %f, %f, %f" % col[:])

    # colors can be added and subtracted
    col += mathutils.Color((0.25, 0.0, 0.0))

    # Color can be multiplied, in this example color is scaled to 0-255
    # can printed as integers
    print("Color: %d, %d, %d" % (col * 255.0)[:])

    # This example prints the color as hexadecimal
    print("Hexadecimal: %.2x%.2x%.2x" % (int(col.r * 255), int(col.g * 255), int(col.b * 255)))

  """

  def __init__(self, rgb: Vector) -> None:

    """

    :param rgb:       
      (r, g, b) color values

    :type rgb:        
      3d vector

    """

    ...

  def copy(self) -> Color:

    """

    Returns a copy of this color.

    Note: use this to get a copy of a wrapped color with
no reference to the original data.

    """

    ...

  def freeze(self) -> None:

    """

    Make this object immutable.

    After this the object can be hashed, used in dictionaries & sets.

    """

    ...

  b: float = ...

  """

  Blue color channel.

  """

  g: float = ...

  """

  Green color channel.

  """

  h: float = ...

  """

  HSV Hue component in [0, 1].

  """

  hsv: float = ...

  """

  HSV Values in [0, 1].

  """

  is_frozen: bool = ...

  """

  True when this object has been frozen (read-only).

  """

  is_wrapped: bool = ...

  """

  True when this object wraps external data (read-only).

  """

  owner: typing.Any = ...

  """

  The item this is wrapping or None  (read-only).

  """

  r: float = ...

  """

  Red color channel.

  """

  s: float = ...

  """

  HSV Saturation component in [0, 1].

  """

  v: float = ...

  """

  HSV Value component in [0, 1].

  """

class Euler:

  """

  This object gives access to Eulers in Blender.

  `Euler angles <https://en.wikipedia.org/wiki/Euler_angles>`_ on Wikipedia.

  .. code::

    import mathutils
    import math

    # create a new euler with default axis rotation order
    eul = mathutils.Euler((0.0, math.radians(45.0), 0.0), 'XYZ')

    # rotate the euler
    eul.rotate_axis('Z', math.radians(10.0))

    # you can access its components by attribute or index
    print("Euler X", eul.x)
    print("Euler Y", eul[1])
    print("Euler Z", eul[-1])

    # components of an existing euler can be set
    eul[:] = 1.0, 2.0, 3.0

    # components of an existing euler can use slice notation to get a tuple
    print("Values: %f, %f, %f" % eul[:])

    # the order can be set at any time too
    eul.order = 'ZYX'

    # eulers can be used to rotate vectors
    vec = mathutils.Vector((0.0, 0.0, 1.0))
    vec.rotate(eul)

    # often its useful to convert the euler into a matrix so it can be used as
    # transformations with more flexibility
    mat_rot = eul.to_matrix()
    mat_loc = mathutils.Matrix.Translation((2.0, 3.0, 4.0))
    mat = mat_loc @ mat_rot.to_4x4()

  """

  def __init__(self, angles: Vector, order: str = 'XYZ') -> None:

    """

    :param angles:    
      Three angles, in radians.

    :type angles:     
      3d vector

    :param order:     
      Optional order of the angles, a permutation of ``XYZ``.

    :type order:      
      str

    """

    ...

  def copy(self) -> Euler:

    """

    Returns a copy of this euler.

    Note: use this to get a copy of a wrapped euler with
no reference to the original data.

    """

    ...

  def freeze(self) -> None:

    """

    Make this object immutable.

    After this the object can be hashed, used in dictionaries & sets.

    """

    ...

  def make_compatible(self, other: typing.Any) -> None:

    """

    Make this euler compatible with another,
so interpolating between them works as intended.

    Note: the rotation order is not taken into account for this function.

    """

    ...

  def rotate(self, other: Euler) -> None:

    """

    Rotates the euler by another mathutils value.

    """

    ...

  def rotate_axis(self, axis: str, angle: float) -> None:

    """

    Rotates the euler a certain amount and returning a unique euler rotation
(no 720 degree pitches).

    """

    ...

  def to_matrix(self) -> Matrix:

    """

    Return a matrix representation of the euler.

    """

    ...

  def to_quaternion(self) -> Quaternion:

    """

    Return a quaternion representation of the euler.

    """

    ...

  def zero(self) -> None:

    """

    Set all values to zero.

    """

    ...

  is_frozen: bool = ...

  """

  True when this object has been frozen (read-only).

  """

  is_wrapped: bool = ...

  """

  True when this object wraps external data (read-only).

  """

  order: str = ...

  """

  Euler rotation order.

  """

  owner: typing.Any = ...

  """

  The item this is wrapping or None  (read-only).

  """

  x: float = ...

  """

  Euler axis angle in radians.

  """

  y: float = ...

  """

  Euler axis angle in radians.

  """

  z: float = ...

  """

  Euler axis angle in radians.

  """

  def __getitem__(self, index: int) -> float:

    """

    Get the angle component at index.

    """

    ...

  def __setitem__(self, index: int, value: float) -> None:

    """

    Set the angle component at index.

    """

    ...

class Matrix:

  """

  This object gives access to Matrices in Blender, supporting square and rectangular
matrices from 2x2 up to 4x4.

  .. code::

    import mathutils
    import math

    # create a location matrix
    mat_loc = mathutils.Matrix.Translation((2.0, 3.0, 4.0))

    # create an identitiy matrix
    mat_sca = mathutils.Matrix.Scale(0.5, 4, (0.0, 0.0, 1.0))

    # create a rotation matrix
    mat_rot = mathutils.Matrix.Rotation(math.radians(45.0), 4, 'X')

    # combine transformations
    mat_out = mat_loc @ mat_rot @ mat_sca
    print(mat_out)

    # extract components back out of the matrix
    loc, rot, sca = mat_out.decompose()
    print(loc, rot, sca)

    # it can also be useful to access components of a matrix directly
    mat = mathutils.Matrix()
    mat[0][0], mat[1][0], mat[2][0] = 0.0, 1.0, 2.0

    mat[0][0:3] = 0.0, 1.0, 2.0

    # each item in a matrix is a vector so vector utility functions can be used
    mat[0].xyz = 0.0, 1.0, 2.0

  """

  def __init__(self, rows: typing.Any = None) -> None:

    """

    :param rows:      
      Sequence of rows.
When omitted, a 4x4 identity matrix is constructed.

    :type rows:       
      2d number sequence

    """

    ...

  @classmethod

  def Diagonal(cls, vector: Vector) -> Matrix:

    """

    Create a diagonal (scaling) matrix using the values from the vector.

    """

    ...

  @classmethod

  def Identity(cls, size: int) -> Matrix:

    """

    Create an identity matrix.

    """

    ...

  @classmethod

  def OrthoProjection(cls, axis: typing.Union[str, Vector], size: int) -> Matrix:

    """

    Create a matrix to represent an orthographic projection.

    """

    ...

  @classmethod

  def Rotation(cls, angle: float, size: int, axis: typing.Union[str, Vector]) -> Matrix:

    """

    Create a matrix representing a rotation.

    """

    ...

  @classmethod

  def Scale(cls, factor: float, size: int, axis: Vector) -> Matrix:

    """

    Create a matrix representing a scaling.

    """

    ...

  @classmethod

  def Shear(cls, plane: str, size: int, factor: float) -> Matrix:

    """

    Create a matrix to represent an shear transformation.

    """

    ...

  @classmethod

  def Translation(cls, vector: Vector) -> Matrix:

    """

    Create a matrix representing a translation.

    """

    ...

  def adjugate(self) -> None:

    """

    Set the matrix to its adjugate.

    Note: When the matrix cannot be adjugated a :exc:`ValueError` exception is raised.

    *Adjugate matrix <https://en.wikipedia.org/wiki/Adjugate_matrix>* on Wikipedia.

    """

    ...

  def adjugated(self) -> Matrix:

    """

    Return an adjugated copy of the matrix.

    Note: When the matrix cant be adjugated a :exc:`ValueError` exception is raised.

    """

    ...

  def copy(self) -> Matrix:

    """

    Returns a copy of this matrix.

    """

    ...

  def decompose(self) -> typing.Any:

    """

    Return the translation, rotation, and scale components of this matrix.

    """

    ...

  def determinant(self) -> float:

    """

    Return the determinant of a matrix.

    *Determinant <https://en.wikipedia.org/wiki/Determinant>* on Wikipedia.

    """

    ...

  def freeze(self) -> None:

    """

    Make this object immutable.

    After this the object can be hashed, used in dictionaries & sets.

    """

    ...

  def identity(self) -> None:

    """

    Set the matrix to the identity matrix.

    Note: An object with a location and rotation of zero, and a scale of one
will have an identity matrix.

    *Identity matrix <https://en.wikipedia.org/wiki/Identity_matrix>* on Wikipedia.

    """

    ...

  def invert(self, fallback: Matrix = None) -> None:

    """

    Set the matrix to its inverse.

    *Inverse matrix <https://en.wikipedia.org/wiki/Inverse_matrix>* on Wikipedia.

    """

    ...

  def invert_safe(self) -> None:

    """

    Set the matrix to its inverse, will never error.
If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
If tweaked matrix is still degenerated, set to the identity matrix instead.

    *Inverse Matrix <https://en.wikipedia.org/wiki/Inverse_matrix>* on Wikipedia.

    """

    ...

  def inverted(self, fallback: typing.Any = None) -> Matrix:

    """

    Return an inverted copy of the matrix.

    """

    ...

  def inverted_safe(self) -> Matrix:

    """

    Return an inverted copy of the matrix, will never error.
If degenerated (e.g. zero scale on an axis), add some epsilon to its diagonal, to get an invertible one.
If tweaked matrix is still degenerated, return the identity matrix instead.

    """

    ...

  def lerp(self, other: Matrix, factor: float) -> Matrix:

    """

    Returns the interpolation of two matrices. Uses polar decomposition, see   "Matrix Animation and Polar Decomposition", Shoemake and Duff, 1992.

    """

    ...

  def normalize(self) -> None:

    """

    Normalize each of the matrix columns.

    """

    ...

  def normalized(self) -> Matrix:

    """

    Return a column normalized matrix

    """

    ...

  def resize_4x4(self) -> None:

    """

    Resize the matrix to 4x4.

    """

    ...

  def rotate(self, other: Euler) -> None:

    """

    Rotates the matrix by another mathutils value.

    Note: If any of the columns are not unit length this may not have desired results.

    """

    ...

  def to_3x3(self) -> Matrix:

    """

    Return a 3x3 copy of this matrix.

    """

    ...

  def to_4x4(self) -> Matrix:

    """

    Return a 4x4 copy of this matrix.

    """

    ...

  def to_euler(self, order: str, euler_compat: Euler) -> Euler:

    """

    Return an Euler representation of the rotation matrix
(3x3 or 4x4 matrix only).

    """

    ...

  def to_quaternion(self) -> Quaternion:

    """

    Return a quaternion representation of the rotation matrix.

    """

    ...

  def to_scale(self) -> Vector:

    """

    Return the scale part of a 3x3 or 4x4 matrix.

    Note: This method does not return a negative scale on any axis because it is not possible to obtain this data from the matrix alone.

    """

    ...

  def to_translation(self) -> Vector:

    """

    Return the translation part of a 4 row matrix.

    """

    ...

  def transpose(self) -> None:

    """

    Set the matrix to its transpose.

    *Transpose <https://en.wikipedia.org/wiki/Transpose>* on Wikipedia.

    """

    ...

  def transposed(self) -> Matrix:

    """

    Return a new, transposed matrix.

    """

    ...

  def zero(self) -> Matrix:

    """

    Set all the matrix values to zero.

    """

    ...

  col: Matrix = ...

  """

  Access the matrix by columns, 3x3 and 4x4 only, (read-only).

  """

  is_frozen: bool = ...

  """

  True when this object has been frozen (read-only).

  """

  is_negative: bool = ...

  """

  True if this matrix results in a negative scale, 3x3 and 4x4 only, (read-only).

  """

  is_orthogonal: bool = ...

  """

  True if this matrix is orthogonal, 3x3 and 4x4 only, (read-only).

  """

  is_orthogonal_axis_vectors: bool = ...

  """

  True if this matrix has got orthogonal axis vectors, 3x3 and 4x4 only, (read-only).

  """

  is_wrapped: bool = ...

  """

  True when this object wraps external data (read-only).

  """

  median_scale: float = ...

  """

  The average scale applied to each axis (read-only).

  """

  owner: typing.Any = ...

  """

  The item this is wrapping or None  (read-only).

  """

  row: Matrix = ...

  """

  Access the matrix by rows (default), (read-only).

  """

  translation: Vector = ...

  """

  The translation component of the matrix.

  """

  def __add__(self, value: Matrix) -> Matrix:

    """

    Add another matrix to this one.

    """

    ...

  def __sub__(self, value: Matrix) -> Matrix:

    """

    Subtract another matrix from this one.

    """

    ...

  def __mul__(self, value: typing.Union[Matrix, float]) -> Matrix:

    """

    Multiply this matrix with another one or a scala value.

    """

    ...

  def __rmul__(self, value: float) -> Matrix:

    """

    Multiply this matrix with a scala value.

    """

    ...

  def __imul__(self, value: typing.Union[Matrix, float]) -> Matrix:

    """

    Multiply this matrix by another one or a scala value.

    """

    ...

  def __matmul__(self, value: typing.Union[Matrix, Vector, Quaternion]) -> typing.Union[Matrix, Vector, Quaternion]:

    """

    Multiply this matrix with another matrix, a vector, or quaternion.

    """

    ...

  def __imatmul__(self, value: typing.Union[Matrix, Vector, Quaternion]) -> typing.Union[Matrix, Vector, Quaternion]:

    """

    Multiply this matrix with another matrix, a vector, or quaternion.

    """

    ...

  def __invert__(self) -> Matrix:

    """

    Invert this matrix.

    """

    ...

  def __truediv__(self, value: float) -> Matrix:

    """

    Divide this matrix by a float value.

    """

    ...

  def __itruediv__(self, value: float) -> Matrix:

    """

    Divide this matrix by a float value.

    """

    ...

  def __getitem__(self, index: int) -> Vector:

    """

    Get the row at given index.

    """

    ...

  def __setitem__(self, index: int, value: typing.Union[Vector, typing.Tuple[float, ...]]) -> None:

    """

    Set the row at given index.

    """

    ...

class Quaternion:

  """

  This object gives access to Quaternions in Blender.

  The constructor takes arguments in various forms:

  (), *no args*
    Create an identity quaternion

  (*wxyz*)
    Create a quaternion from a ``(w, x, y, z)`` vector.

  (*exponential_map*)
    Create a quaternion from a 3d exponential map vector.

    :meth:`to_exponential_map`

  (*axis, angle*)
    Create a quaternion representing a rotation of *angle* radians over *axis*.

    :meth:`to_axis_angle`

  .. code::

    import mathutils
    import math

    # a new rotation 90 degrees about the Y axis
    quat_a = mathutils.Quaternion((0.7071068, 0.0, 0.7071068, 0.0))

    # passing values to Quaternion's directly can be confusing so axis, angle
    # is supported for initializing too
    quat_b = mathutils.Quaternion((0.0, 1.0, 0.0), math.radians(90.0))

    print("Check quaternions match", quat_a == quat_b)

    # like matrices, quaternions can be multiplied to accumulate rotational values
    quat_a = mathutils.Quaternion((0.0, 1.0, 0.0), math.radians(90.0))
    quat_b = mathutils.Quaternion((0.0, 0.0, 1.0), math.radians(45.0))
    quat_out = quat_a @ quat_b

    # print the quat, euler degrees for mere mortals and (axis, angle)
    print("Final Rotation:")
    print(quat_out)
    print("%.2f, %.2f, %.2f" % tuple(math.degrees(a) for a in quat_out.to_euler()))
    print("(%.2f, %.2f, %.2f), %.2f" % (quat_out.axis[:] +
                                        (math.degrees(quat_out.angle), )))

    # multiple rotations can be interpolated using the exponential map
    quat_c = mathutils.Quaternion((1.0, 0.0, 0.0), math.radians(15.0))
    exp_avg = (quat_a.to_exponential_map() +
               quat_b.to_exponential_map() +
               quat_c.to_exponential_map()) / 3.0
    quat_avg = mathutils.Quaternion(exp_avg)
    print("Average rotation:")
    print(quat_avg)

  """

  def __init__(self, seq: Vector, angle: float = None) -> None:

    """

    :param seq:       
      size 3 or 4

    :type seq:        
      :class:`Vector`

    :param angle:     
      rotation angle, in radians

    :type angle:      
      float

    """

    ...

  def conjugate(self) -> None:

    """

    Set the quaternion to its conjugate (negate x, y, z).

    """

    ...

  def conjugated(self) -> Quaternion:

    """

    Return a new conjugated quaternion.

    """

    ...

  def copy(self) -> Quaternion:

    """

    Returns a copy of this quaternion.

    Note: use this to get a copy of a wrapped quaternion with
no reference to the original data.

    """

    ...

  def cross(self, other: Quaternion) -> Quaternion:

    """

    Return the cross product of this quaternion and another.

    """

    ...

  def dot(self, other: Quaternion) -> float:

    """

    Return the dot product of this quaternion and another.

    """

    ...

  def freeze(self) -> None:

    """

    Make this object immutable.

    After this the object can be hashed, used in dictionaries & sets.

    """

    ...

  def identity(self) -> Quaternion:

    """

    Set the quaternion to an identity quaternion.

    """

    ...

  def invert(self) -> None:

    """

    Set the quaternion to its inverse.

    """

    ...

  def inverted(self) -> Quaternion:

    """

    Return a new, inverted quaternion.

    """

    ...

  def negate(self) -> Quaternion:

    """

    Set the quaternion to its negative.

    """

    ...

  def normalize(self) -> None:

    """

    Normalize the quaternion.

    """

    ...

  def normalized(self) -> Quaternion:

    """

    Return a new normalized quaternion.

    """

    ...

  def rotate(self, other: Euler) -> None:

    """

    Rotates the quaternion by another mathutils value.

    """

    ...

  def rotation_difference(self, other: Quaternion) -> Quaternion:

    """

    Returns a quaternion representing the rotational difference.

    """

    ...

  def slerp(self, other: Quaternion, factor: float) -> Quaternion:

    """

    Returns the interpolation of two quaternions.

    """

    ...

  def to_axis_angle(self) -> typing.Any:

    """

    Return the axis, angle representation of the quaternion.

    """

    ...

  def to_euler(self, order: str, euler_compat: Euler) -> Euler:

    """

    Return Euler representation of the quaternion.

    """

    ...

  def to_exponential_map(self) -> Vector:

    """

    Return the exponential map representation of the quaternion.

    This representation consist of the rotation axis multiplied by the rotation angle.   Such a representation is useful for interpolation between multiple orientations.

    To convert back to a quaternion, pass it to the :class:`Quaternion` constructor.

    """

    ...

  def to_matrix(self) -> Matrix:

    """

    Return a matrix representation of the quaternion.

    """

    ...

  angle: float = ...

  """

  Angle of the quaternion.

  """

  axis: Vector = ...

  """

  Quaternion axis as a vector.

  """

  is_frozen: bool = ...

  """

  True when this object has been frozen (read-only).

  """

  is_wrapped: bool = ...

  """

  True when this object wraps external data (read-only).

  """

  magnitude: float = ...

  """

  Size of the quaternion (read-only).

  """

  owner: typing.Any = ...

  """

  The item this is wrapping or None  (read-only).

  """

  w: float = ...

  """

  Quaternion axis value.

  """

  x: float = ...

  """

  Quaternion axis value.

  """

  y: float = ...

  """

  Quaternion axis value.

  """

  z: float = ...

  """

  Quaternion axis value.

  """

  def __add__(self, value: Quaternion) -> Quaternion:

    """

    Add another quaternion to this one.

    """

    ...

  def __sub__(self, value: Quaternion) -> Quaternion:

    """

    Subtract another quaternion from this one.

    """

    ...

  def __mul__(self, value: typing.Union[Quaternion, float]) -> Quaternion:

    """

    Multiply this quaternion with another one or a scala value.

    """

    ...

  def __rmul__(self, value: float) -> Quaternion:

    """

    Multiply this quaternion with a scala value.

    """

    ...

  def __imul__(self, value: typing.Union[Quaternion, float]) -> Quaternion:

    """

    Multiply this quaternion with another one or a scala value.

    """

    ...

  def __matmul__(self, value: typing.Union[Quaternion, Vector]) -> typing.Union[Quaternion, Vector]:

    """

    Multiply with another quaternion or a vector.

    """

    ...

  def __imatmul__(self, value: typing.Union[Quaternion, Vector]) -> typing.Union[Quaternion, Vector]:

    """

    Multiply with another quaternion or a vector.

    """

    ...

  def __truediv__(self, value: float) -> Quaternion:

    """

    Divide this quaternion by a float value.

    """

    ...

  def __itruediv__(self, value: float) -> Quaternion:

    """

    Divide this quaternion by a float value.

    """

    ...

  def __getitem__(self, index: int) -> float:

    """

    Get quaternion component at index.

    """

    ...

  def __setitem__(self, index: int, value: float) -> None:

    """

    Set quaternion component at index.

    """

    ...

class Vector:

  """

  This object gives access to Vectors in Blender.

  .. code::

    import mathutils

    # zero length vector
    vec = mathutils.Vector((0.0, 0.0, 1.0))

    # unit length vector
    vec_a = vec.normalized()

    vec_b = mathutils.Vector((0.0, 1.0, 2.0))

    vec2d = mathutils.Vector((1.0, 2.0))
    vec3d = mathutils.Vector((1.0, 0.0, 0.0))
    vec4d = vec_a.to_4d()

    # other mathutuls types
    quat = mathutils.Quaternion()
    matrix = mathutils.Matrix()

    # Comparison operators can be done on Vector classes:

    # (In)equality operators == and != test component values, e.g. 1,2,3 != 3,2,1
    vec_a == vec_b
    vec_a != vec_b

    # Ordering operators >, >=, > and <= test vector length.
    vec_a > vec_b
    vec_a >= vec_b
    vec_a < vec_b
    vec_a <= vec_b


    # Math can be performed on Vector classes
    vec_a + vec_b
    vec_a - vec_b
    vec_a @ vec_b
    vec_a * 10.0
    matrix @ vec_a
    quat @ vec_a
    -vec_a


    # You can access a vector object like a sequence
    x = vec_a[0]
    len(vec)
    vec_a[:] = vec_b
    vec_a[:] = 1.0, 2.0, 3.0
    vec2d[:] = vec3d[:2]


    # Vectors support 'swizzle' operations
    # See https://en.wikipedia.org/wiki/Swizzling_(computer_graphics)
    vec.xyz = vec.zyx
    vec.xy = vec4d.zw
    vec.xyz = vec4d.wzz
    vec4d.wxyz = vec.yxyx

  """

  def __init__(self, seq: typing.Sequence[typing.Any]) -> None:

    """

    :param seq:       
      Components of the vector, must be a sequence of at least two

    :type seq:        
      sequence of numbers

    """

    ...

  @classmethod

  def Fill(cls, size: int, fill: float = 0.0) -> None:

    """

    Create a vector of length size with all values set to fill.

    """

    ...

  @classmethod

  def Linspace(cls, start: int, stop: int, size: int) -> None:

    """

    Create a vector of the specified size which is filled with linearly spaced values between start and stop values.

    """

    ...

  @classmethod

  def Repeat(cls, vector: typing.Any, size: int) -> None:

    """

    Create a vector by repeating the values in vector until the required size is reached.

    """

    ...

  def angle(self, other: Vector, fallback: typing.Any = None) -> float:

    """

    Return the angle between two vectors.

    """

    ...

  def angle_signed(self, other: Vector, fallback: typing.Any) -> float:

    """

    Return the signed angle between two 2D vectors (clockwise is positive).

    """

    ...

  def copy(self) -> Vector:

    """

    Returns a copy of this vector.

    Note: use this to get a copy of a wrapped vector with
no reference to the original data.

    """

    ...

  def cross(self, other: Vector) -> typing.Union[Vector, float]:

    """

    Return the cross product of this vector and another.

    Note: both vectors must be 2D or 3D

    """

    ...

  def dot(self, other: Vector) -> Vector:

    """

    Return the dot product of this vector and another.

    """

    ...

  def freeze(self) -> None:

    """

    Make this object immutable.

    After this the object can be hashed, used in dictionaries & sets.

    """

    ...

  def lerp(self, other: Vector, factor: float) -> Vector:

    """

    Returns the interpolation of two vectors.

    """

    ...

  def negate(self) -> None:

    """

    Set all values to their negative.

    """

    ...

  def normalize(self) -> None:

    """

    Normalize the vector, making the length of the vector always 1.0.

    Warning: Normalizing a vector where all values are zero has no effect.

    Note: Normalize works for vectors of all sizes,
however 4D Vectors w axis is left untouched.

    """

    ...

  def normalized(self) -> Vector:

    """

    Return a new, normalized vector.

    """

    ...

  def orthogonal(self) -> Vector:

    """

    Return a perpendicular vector.

    Note: the axis is undefined, only use when any orthogonal vector is acceptable.

    """

    ...

  def project(self, other: Vector) -> Vector:

    """

    Return the projection of this vector onto the *other*.

    """

    ...

  def reflect(self, mirror: Vector) -> Vector:

    """

    Return the reflection vector from the *mirror* argument.

    """

    ...

  def resize(self, size: typing.Any = 3) -> None:

    """

    Resize the vector to have size number of elements.

    """

    ...

  def resize_2d(self) -> None:

    """

    Resize the vector to 2D  (x, y).

    """

    ...

  def resize_3d(self) -> None:

    """

    Resize the vector to 3D  (x, y, z).

    """

    ...

  def resize_4d(self) -> None:

    """

    Resize the vector to 4D (x, y, z, w).

    """

    ...

  def resized(self, size: typing.Any = 3) -> Vector:

    """

    Return a resized copy of the vector with size number of elements.

    """

    ...

  def rotate(self, other: Euler) -> None:

    """

    Rotate the vector by a rotation value.

    """

    ...

  def rotation_difference(self, other: Vector) -> Quaternion:

    """

    Returns a quaternion representing the rotational difference between this
vector and another.

    Note: 2D vectors raise an :exc:`AttributeError`.

    """

    ...

  def slerp(self, other: Vector, factor: float, fallback: typing.Any = None) -> Vector:

    """

    Returns the interpolation of two non-zero vectors (spherical coordinates).

    """

    ...

  def to_2d(self) -> Vector:

    """

    Return a 2d copy of the vector.

    """

    ...

  def to_3d(self) -> Vector:

    """

    Return a 3d copy of the vector.

    """

    ...

  def to_4d(self) -> Vector:

    """

    Return a 4d copy of the vector.

    """

    ...

  def to_track_quat(self, track: str, up: str) -> Quaternion:

    """

    Return a quaternion rotation from the vector and the track and up axis.

    """

    ...

  def to_tuple(self, precision: int = -1) -> typing.Tuple[typing.Any, ...]:

    """

    Return this vector as a tuple with.

    """

    ...

  def zero(self) -> None:

    """

    Set all values to zero.

    """

    ...

  is_frozen: bool = ...

  """

  True when this object has been frozen (read-only).

  """

  is_wrapped: bool = ...

  """

  True when this object wraps external data (read-only).

  """

  length: float = ...

  """

  Vector Length.

  """

  length_squared: float = ...

  """

  Vector length squared (v.dot(v)).

  """

  magnitude: float = ...

  """

  Vector Length.

  """

  owner: typing.Any = ...

  """

  The item this is wrapping or None  (read-only).

  """

  w: float = ...

  """

  Vector W axis (4D Vectors only).

  """

  ww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  www: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wwzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wxzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wywx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wywy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wywz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wyzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  wzzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  x: float = ...

  """

  Vector X axis.

  """

  xw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xwzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xxzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xywx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xywy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xywz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xyzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  xzzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  y: float = ...

  """

  Vector Y axis.

  """

  yw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  ywzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yxzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yywx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yywy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yywz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yyzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  yzzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  z: float = ...

  """

  Vector Z axis (3D Vectors only).

  """

  zw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zwzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zxzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zywx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zywy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zywz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zyzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzww: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzwx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzwy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzwz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzxw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzxx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzxy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzxz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzyw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzyx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzyy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzyz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzzw: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzzx: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzzy: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  zzzz: typing.Any = ...

  """

  Undocumented *contribute <https://developer.blender.org/T51061>*

  """

  def __add__(self, value: Vector) -> Vector:

    """

    Add another vector to this one.

    """

    ...

  def __sub__(self, value: Vector) -> Vector:

    """

    Subtract another vector from this one.

    """

    ...

  def __mul__(self, value: typing.Union[Vector, float]) -> Vector:

    """

    Multiply this vector with another one or a scala value.

    """

    ...

  def __rmul__(self, value: float) -> Vector:

    """

    Multiply this vector with a scala value.

    """

    ...

  def __imul__(self, value: typing.Union[Vector, float]) -> Vector:

    """

    Multiply this vector with another one or a scala value.

    """

    ...

  def __matmul__(self, value: typing.Union[Matrix, Vector]) -> typing.Union[Vector, float]:

    """

    Multiply this vector with a matrix or another vector.

    """

    ...

  def __imatmul__(self, value: typing.Union[Matrix, Vector]) -> typing.Union[Vector, float]:

    """

    Multiply this vector with a matrix or another vector.

    """

    ...

  def __truediv__(self, value: float) -> Vector:

    """

    Divide this vector by a float value.

    """

    ...

  def __itruediv__(self, value: float) -> Vector:

    """

    Divide this vector by a float value.

    """

    ...

  def __getitem__(self, index: int) -> float:

    """

    Get vector component at index.

    """

    ...

  def __setitem__(self, index: int, value: float) -> None:

    """

    Set vector component at index.

    """

    ...
