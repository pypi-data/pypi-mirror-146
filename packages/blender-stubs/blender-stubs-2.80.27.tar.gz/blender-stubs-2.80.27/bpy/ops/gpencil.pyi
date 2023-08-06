"""


Gpencil Operators
*****************

:func:`active_frame_delete`

:func:`active_frames_delete_all`

:func:`annotate`

:func:`blank_frame_add`

:func:`brush_presets_create`

:func:`color_hide`

:func:`color_isolate`

:func:`color_lock_all`

:func:`color_reveal`

:func:`color_select`

:func:`color_unlock_all`

:func:`convert`

:func:`convert_old_files`

:func:`copy`

:func:`data_add`

:func:`data_unlink`

:func:`delete`

:func:`dissolve`

:func:`draw`

:func:`duplicate`

:func:`duplicate_move`

:func:`editmode_toggle`

:func:`extrude`

:func:`extrude_move`

:func:`fill`

:func:`frame_clean_fill`

:func:`frame_clean_loose`

:func:`frame_duplicate`

:func:`generate_weights`

:func:`guide_rotate`

:func:`hide`

:func:`interpolate`

:func:`interpolate_reverse`

:func:`interpolate_sequence`

:func:`layer_add`

:func:`layer_change`

:func:`layer_duplicate`

:func:`layer_duplicate_object`

:func:`layer_isolate`

:func:`layer_merge`

:func:`layer_move`

:func:`layer_remove`

:func:`lock_all`

:func:`lock_layer`

:func:`move_to_layer`

:func:`paintmode_toggle`

:func:`paste`

:func:`primitive`

:func:`reproject`

:func:`reveal`

:func:`sculpt_paint`

:func:`sculptmode_toggle`

:func:`select`

:func:`select_all`

:func:`select_alternate`

:func:`select_box`

:func:`select_circle`

:func:`select_first`

:func:`select_grouped`

:func:`select_lasso`

:func:`select_last`

:func:`select_less`

:func:`select_linked`

:func:`select_more`

:func:`selection_opacity_toggle`

:func:`selectmode_toggle`

:func:`snap_cursor_to_selected`

:func:`snap_to_cursor`

:func:`snap_to_grid`

:func:`stroke_apply_thickness`

:func:`stroke_arrange`

:func:`stroke_caps_set`

:func:`stroke_change_color`

:func:`stroke_cutter`

:func:`stroke_cyclical_set`

:func:`stroke_flip`

:func:`stroke_join`

:func:`stroke_lock_color`

:func:`stroke_merge`

:func:`stroke_separate`

:func:`stroke_simplify`

:func:`stroke_simplify_fixed`

:func:`stroke_smooth`

:func:`stroke_split`

:func:`stroke_subdivide`

:func:`stroke_trim`

:func:`unlock_all`

:func:`vertex_group_assign`

:func:`vertex_group_deselect`

:func:`vertex_group_invert`

:func:`vertex_group_normalize`

:func:`vertex_group_normalize_all`

:func:`vertex_group_remove_from`

:func:`vertex_group_select`

:func:`vertex_group_smooth`

:func:`weightmode_toggle`

"""

import typing

def active_frame_delete() -> None:

  """

  Delete the active frame for the active Grease Pencil Layer

  """

  ...

def active_frames_delete_all() -> None:

  """

  Delete the active frame(s) of all editable Grease Pencil layers

  """

  ...

def annotate(mode: str = 'DRAW', stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Make annotations on the active data

  """

  ...

def blank_frame_add(all_layers: bool = False) -> None:

  """

  Insert a blank frame on the current frame (all subsequently existing frames, if any, are shifted right by one frame)

  """

  ...

def brush_presets_create() -> None:

  """

  Create a set of predefined Grease Pencil drawing brushes

  """

  ...

def color_hide(unselected: bool = False) -> None:

  """

  Hide selected/unselected Grease Pencil colors

  """

  ...

def color_isolate(affect_visibility: bool = False) -> None:

  """

  Toggle whether the active color is the only one that is editable and/or visible

  """

  ...

def color_lock_all() -> None:

  """

  Lock all Grease Pencil colors to prevent them from being accidentally modified

  """

  ...

def color_reveal() -> None:

  """

  Unhide all hidden Grease Pencil colors

  """

  ...

def color_select(deselect: bool = False) -> None:

  """

  Select all Grease Pencil strokes using current color

  """

  ...

def color_unlock_all() -> None:

  """

  Unlock all Grease Pencil colors so that they can be edited

  """

  ...

def convert(type: str = 'PATH', use_normalize_weights: bool = True, radius_multiplier: float = 1.0, use_link_strokes: bool = False, timing_mode: str = 'FULL', frame_range: int = 100, start_frame: int = 1, use_realtime: bool = False, end_frame: int = 250, gap_duration: float = 0.0, gap_randomness: float = 0.0, seed: int = 0, use_timing_data: bool = False) -> None:

  """

  Convert the active Grease Pencil layer to a new Curve Object

  """

  ...

def convert_old_files(annotation: bool = False) -> None:

  """

  Convert 2.7x grease pencil files to 2.80

  """

  ...

def copy() -> None:

  """

  Copy selected Grease Pencil points and strokes

  """

  ...

def data_add() -> None:

  """

  Add new Grease Pencil data-block

  """

  ...

def data_unlink() -> None:

  """

  Unlink active Annotation data-block

  """

  ...

def delete(type: str = 'POINTS') -> None:

  """

  Delete selected Grease Pencil strokes, vertices, or frames

  """

  ...

def dissolve(type: str = 'POINTS') -> None:

  """

  Delete selected points without splitting strokes

  """

  ...

def draw(mode: str = 'DRAW', stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True, disable_straight: bool = False, disable_fill: bool = False, guide_last_angle: float = 0.0) -> None:

  """

  Draw a new stroke in the active Grease Pencil Object

  """

  ...

def duplicate() -> None:

  """

  Duplicate the selected Grease Pencil strokes

  """

  ...

def duplicate_move(GPENCIL_OT_duplicate: GPENCIL_OT_duplicate = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Make copies of the selected Grease Pencil strokes and move them

  """

  ...

def editmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit edit mode for Grease Pencil strokes

  """

  ...

def extrude() -> None:

  """

  Extrude the selected Grease Pencil points

  """

  ...

def extrude_move(GPENCIL_OT_extrude: GPENCIL_OT_extrude = None, TRANSFORM_OT_translate: TRANSFORM_OT_translate = None) -> None:

  """

  Extrude selected points and move them

  """

  ...

def fill(on_back: bool = False) -> None:

  """

  Fill with color the shape formed by strokes

  """

  ...

def frame_clean_fill(mode: str = 'ACTIVE') -> None:

  """

  Remove 'no fill' boundary strokes

  """

  ...

def frame_clean_loose(limit: int = 1) -> None:

  """

  Remove loose points

  """

  ...

def frame_duplicate(mode: str = 'ACTIVE') -> None:

  """

  Make a copy of the active Grease Pencil Frame

  """

  ...

def generate_weights(mode: str = 'NAME', armature: str = 'DEFAULT', ratio: float = 0.1, decay: float = 0.8) -> None:

  """

  Generate automatic weights for armatures (requires armature modifier)

  """

  ...

def guide_rotate(increment: bool = True, angle: float = 0.0) -> None:

  """

  Rotate guide angle

  """

  ...

def hide(unselected: bool = False) -> None:

  """

  Hide selected/unselected Grease Pencil layers

  """

  ...

def interpolate(shift: float = 0.0) -> None:

  """

  Interpolate grease pencil strokes between frames

  """

  ...

def interpolate_reverse() -> None:

  """

  Remove breakdown frames generated by interpolating between two Grease Pencil frames

  """

  ...

def interpolate_sequence() -> None:

  """

  Generate 'in-betweens' to smoothly interpolate between Grease Pencil frames

  """

  ...

def layer_add() -> None:

  """

  Add new layer or note for the active data-block

  """

  ...

def layer_change(layer: str = 'DEFAULT') -> None:

  """

  Change active Grease Pencil layer

  """

  ...

def layer_duplicate() -> None:

  """

  Make a copy of the active Grease Pencil layer

  """

  ...

def layer_duplicate_object(object: str = '', mode: str = 'ALL') -> None:

  """

  Make a copy of the active Grease Pencil layer to new object

  """

  ...

def layer_isolate(affect_visibility: bool = False) -> None:

  """

  Toggle whether the active layer is the only one that can be edited and/or visible

  """

  ...

def layer_merge() -> None:

  """

  Merge the current layer with the layer below

  """

  ...

def layer_move(type: str = 'UP') -> None:

  """

  Move the active Grease Pencil layer up/down in the list

  """

  ...

def layer_remove() -> None:

  """

  Remove active Grease Pencil layer

  """

  ...

def lock_all() -> None:

  """

  Lock all Grease Pencil layers to prevent them from being accidentally modified

  """

  ...

def lock_layer() -> None:

  """

  Lock and hide any color not used in any layer

  """

  ...

def move_to_layer(layer: str = 'DEFAULT') -> None:

  """

  Move selected strokes to another layer

  """

  ...

def paintmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit paint mode for Grease Pencil strokes

  """

  ...

def paste(type: str = 'COPY') -> None:

  """

  Paste previously copied strokes or copy and merge in active layer

  """

  ...

def primitive(edges: int = 4, type: str = 'BOX', wait_for_input: bool = True) -> None:

  """

  Create predefined grease pencil stroke shapes

  """

  ...

def reproject(type: str = 'VIEW') -> None:

  """

  Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

  """

  ...

def reveal(select: bool = True) -> None:

  """

  Show all Grease Pencil layers

  """

  ...

def sculpt_paint(stroke: typing.Union[typing.Sequence[OperatorStrokeElement], typing.Mapping[str, OperatorStrokeElement], bpy.types.bpy_prop_collection] = None, wait_for_input: bool = True) -> None:

  """

  Apply tweaks to strokes by painting over the strokes

  """

  ...

def sculptmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit sculpt mode for Grease Pencil strokes

  """

  ...

def select(extend: bool = False, deselect: bool = False, toggle: bool = False, deselect_all: bool = False, entire_strokes: bool = False, location: typing.Tuple[int, int] = (0, 0)) -> None:

  """

  Select Grease Pencil strokes and/or stroke points

  """

  ...

def select_all(action: str = 'TOGGLE') -> None:

  """

  Change selection of all Grease Pencil strokes currently visible

  """

  ...

def select_alternate(unselect_ends: bool = True) -> None:

  """

  Select alternative points in same strokes as already selected points

  """

  ...

def select_box(xmin: int = 0, xmax: int = 0, ymin: int = 0, ymax: int = 0, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select Grease Pencil strokes within a rectangular region

  """

  ...

def select_circle(x: int = 0, y: int = 0, radius: int = 25, wait_for_input: bool = True, mode: str = 'SET') -> None:

  """

  Select Grease Pencil strokes using brush selection

  """

  ...

def select_first(only_selected_strokes: bool = False, extend: bool = False) -> None:

  """

  Select first point in Grease Pencil strokes

  """

  ...

def select_grouped(type: str = 'LAYER') -> None:

  """

  Select all strokes with similar characteristics

  """

  ...

def select_lasso(mode: str = 'SET', path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None) -> None:

  """

  Select Grease Pencil strokes using lasso selection

  """

  ...

def select_last(only_selected_strokes: bool = False, extend: bool = False) -> None:

  """

  Select last point in Grease Pencil strokes

  """

  ...

def select_less() -> None:

  """

  Shrink sets of selected Grease Pencil points

  """

  ...

def select_linked() -> None:

  """

  Select all points in same strokes as already selected points

  """

  ...

def select_more() -> None:

  """

  Grow sets of selected Grease Pencil points

  """

  ...

def selection_opacity_toggle() -> None:

  """

  Hide/Unhide selected points for Grease Pencil strokes setting alpha factor

  """

  ...

def selectmode_toggle(mode: int = 0) -> None:

  """

  Set selection mode for Grease Pencil strokes

  """

  ...

def snap_cursor_to_selected() -> None:

  """

  Snap cursor to center of selected points

  """

  ...

def snap_to_cursor(use_offset: bool = True) -> None:

  """

  Snap selected points/strokes to the cursor

  """

  ...

def snap_to_grid() -> None:

  """

  Snap selected points to the nearest grid points

  """

  ...

def stroke_apply_thickness() -> None:

  """

  Apply the thickness change of the layer to its strokes

  """

  ...

def stroke_arrange(direction: str = 'UP') -> None:

  """

  Arrange selected strokes up/down in the drawing order of the active layer

  """

  ...

def stroke_caps_set(type: str = 'TOGGLE') -> None:

  """

  Change Stroke caps mode (rounded or flat)

  """

  ...

def stroke_change_color(material: str = '') -> None:

  """

  Move selected strokes to active material

  """

  ...

def stroke_cutter(path: typing.Union[typing.Sequence[OperatorMousePath], typing.Mapping[str, OperatorMousePath], bpy.types.bpy_prop_collection] = None) -> None:

  """

  Select section and cut

  """

  ...

def stroke_cyclical_set(type: str = 'TOGGLE', geometry: bool = False) -> None:

  """

  Close or open the selected stroke adding an edge from last to first point

  """

  ...

def stroke_flip() -> None:

  """

  Change direction of the points of the selected strokes

  """

  ...

def stroke_join(type: str = 'JOIN', leave_gaps: bool = False) -> None:

  """

  Join selected strokes (optionally as new stroke)

  """

  ...

def stroke_lock_color() -> None:

  """

  Lock any color not used in any selected stroke

  """

  ...

def stroke_merge(mode: str = 'STROKE', back: bool = False, additive: bool = False, cyclic: bool = False, clear_point: bool = False, clear_stroke: bool = False) -> None:

  """

  Create a new stroke with the selected stroke points

  """

  ...

def stroke_separate(mode: str = 'POINT') -> None:

  """

  Separate the selected strokes or layer in a new grease pencil object

  """

  ...

def stroke_simplify(factor: float = 0.0) -> None:

  """

  Simplify selected stroked reducing number of points

  """

  ...

def stroke_simplify_fixed(step: int = 1) -> None:

  """

  Simplify selected stroked reducing number of points using fixed algorithm

  """

  ...

def stroke_smooth(repeat: int = 1, factor: float = 0.5, only_selected: bool = True, smooth_position: bool = True, smooth_thickness: bool = True, smooth_strength: bool = False, smooth_uv: bool = False) -> None:

  """

  Smooth selected strokes

  """

  ...

def stroke_split() -> None:

  """

  Split selected points as new stroke on same frame

  """

  ...

def stroke_subdivide(number_cuts: int = 1, factor: float = 0.0, repeat: int = 1, only_selected: bool = True, smooth_position: bool = True, smooth_thickness: bool = True, smooth_strength: bool = False, smooth_uv: bool = False) -> None:

  """

  Subdivide between continuous selected points of the stroke adding a point half way between them

  """

  ...

def stroke_trim() -> None:

  """

  Trim selected stroke to first loop or intersection

  """

  ...

def unlock_all() -> None:

  """

  Unlock all Grease Pencil layers so that they can be edited

  """

  ...

def vertex_group_assign() -> None:

  """

  Assign the selected vertices to the active vertex group

  """

  ...

def vertex_group_deselect() -> None:

  """

  Deselect all selected vertices assigned to the active vertex group

  """

  ...

def vertex_group_invert() -> None:

  """

  Invert weights to the active vertex group

  """

  ...

def vertex_group_normalize() -> None:

  """

  Normalize weights to the active vertex group

  """

  ...

def vertex_group_normalize_all(lock_active: bool = True) -> None:

  """

  Normalize all weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

  """

  ...

def vertex_group_remove_from() -> None:

  """

  Remove the selected vertices from active or all vertex group(s)

  """

  ...

def vertex_group_select() -> None:

  """

  Select all the vertices assigned to the active vertex group

  """

  ...

def vertex_group_smooth(factor: float = 0.5, repeat: int = 1) -> None:

  """

  Smooth weights to the active vertex group

  """

  ...

def weightmode_toggle(back: bool = False) -> None:

  """

  Enter/Exit weight paint mode for Grease Pencil strokes

  """

  ...
