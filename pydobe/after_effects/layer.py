from __future__ import annotations
from typing import TYPE_CHECKING

from pydobe.core import format_to_extend, create_python_object, PydobeBaseCollection
from .property import Property, PropertyGroup
from pydobe.after_effects.utils import time_to_current_format
from pydobe.after_effects.data import blending_modes_dictionary, frame_blending_dictionary
from pydobe.utils import hex_to_rgb

if TYPE_CHECKING:
    from .item import CompItem, Item


class Layer(PropertyGroup):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The composition that contains this Layer"""

    @property
    def containing_comp(self) -> CompItem:
        kwargs = self._eval_on_object("containingComp")
        return CompItem(**kwargs) if kwargs else None

    """When true, the layer is locked"""

    @property
    def locked(self) -> bool:
        return self._eval_on_object("locked")

    @locked.setter
    def locked(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"locked = {extend_value}")

    """If the layer is shy, it will be hidden when hide shy layers is toggled"""

    @property
    def shy(self) -> bool:
        return self._eval_on_object("shy")

    @shy.setter
    def shy(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"shy = {extend_value}")

    """When true, the layer is soloed"""

    @property
    def solo(self) -> bool:
        return self._eval_on_object("shy")

    @solo.setter
    def solo(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"solo = {extend_value}")

    # FUNCTION

    def remove(self):
        """Remove a layer from a composition"""
        self._eval_on_object("remove()")


class AVLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # AE PROPERTIES

    """The Opacity Property Object"""

    @property
    def anchor_point(self) -> Property:
        kwargs = self._eval_on_object('anchorPoint')
        return Property(**kwargs) if kwargs else None

    """The Opacity Property Object"""

    @property
    def effects(self) -> PropertyGroup:
        kwargs = self._eval_on_object('Effects')
        return PropertyGroup(**kwargs) if kwargs else None

    """The Opacity Property Object"""

    @property
    def opacity(self) -> Property:
        kwargs = self._eval_on_object('opacity')
        return Property(**kwargs) if kwargs else None

    """The Position Property Object"""

    @property
    def position(self) -> Property:
        kwargs = self._eval_on_object('position')
        return Property(**kwargs) if kwargs else None

    """The Rotation Property Object"""

    @property
    def rotation(self) -> Property:
        kwargs = self._eval_on_object('rotation')
        return Property(**kwargs) if kwargs else None

    """The Scale Property Object"""

    @property
    def scale(self) -> Property:
        kwargs = self._eval_on_object('scale')
        return Property(**kwargs) if kwargs else None

    """The X Rotation Property Object"""

    @property
    def x_rotation(self) -> Property:
        kwargs = self._eval_on_object('xRotation')
        return Property(**kwargs) if kwargs else None

    """The Y Rotation Property Object"""

    @property
    def y_rotation(self) -> Property:
        kwargs = self._eval_on_object('yRotation')
        return Property(**kwargs) if kwargs else None


    # PROPERTIES

    """True is the layer is an adjustment Layer"""

    @property
    def adjustment_layer(self) -> str:
        return self._eval_on_object('adjustmentLayer')

    @adjustment_layer.setter
    def adjustment_layer(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'adjustmentLayer = {extend_value}')

    """True if the audio, is active
       Will return False if other layers are solo, or if time is not between layers in and out point"""

    @property
    def audio_active(self) -> bool:
        return self._eval_on_object('audioActive')

    """True if the audio is enabled"""

    @property
    def audio_enabled(self) -> bool:
        return self._eval_on_object('audioEnabled')

    @audio_enabled.setter
    def audio_enabled(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'audioEnabled = {extend_value}')

    """The Blending Mode of the Layer"""

    @property
    def blending_mode(self) -> str:
        value = self._eval_on_object('blendingMode')
        value_as_string = blending_modes_dictionary[value]
        return value_as_string

    @blending_mode.setter
    def blending_mode(self, value: str or int):
        if isinstance(value, str):
            value = blending_modes_dictionary[value]
        self._eval_on_object(f'blendingMode = {value}')

    """True if it is legal to change the value of collapse transformation"""

    @property
    def can_set_collapse_transformation(self) -> bool:
        return self._eval_on_object('canSetCollapseTransformation')

    """True if it is legal to change the value of time remap enabled transformation"""

    @property
    def can_set_time_remap_enabled(self) -> bool:
        return self._eval_on_object('canSetTimeRemapEnabled')

    """True if collapse transformation is on for this layer"""

    @property
    def collapse_transformation(self) -> bool:
        return self._eval_on_object('collapseTransformation')

    @collapse_transformation.setter
    def collapse_transformation(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'collapseTransformation = {extend_value}')

    """True if the layers effects are active"""

    @property
    def effects_active(self) -> bool:
        return self._eval_on_object('effectsActive')

    @effects_active.setter
    def effects_active(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'effectsActive = {extend_value}')

    """True if this is an environment layer in a Ray-traced 3D composition"""

    @property
    def environment_layer(self) -> bool:
        return self._eval_on_object('environmentLayer')

    @environment_layer.setter
    def environment_layer(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'environmentLayer = {extend_value}')

    """True if frame blending is enabled for the layer."""

    @property
    def frame_blending(self) -> bool:
        return self._eval_on_object('frameBlending')

    """The type of frame blending to perform when frame blending is enabled for the layer"""

    @property
    def frame_blending_type(self) -> str:
        value = self._eval_on_object('frameBlendingType')
        value_as_string = frame_blending_dictionary[value]
        return value_as_string

    @frame_blending_type.setter
    def frame_blending_type(self, value: int or str):
        if isinstance(value, str):
            value = frame_blending_dictionary[value]
        self._eval_on_object(f"frameBlendingType = {value}")

    """True if the layer is a guide layer"""

    @property
    def guide_layer(self) -> bool:
        return self._eval_on_object('guideLayer')

    """True if the item has an audio component"""

    @property
    def has_audio(self) -> bool:
        return self._eval_on_object('hasAudio')

    """True if the item has an audio component"""

    @property
    def has_track_matte(self) -> bool:
        return self._eval_on_object('hasTrackMatte')

    """The height of the layer in pixels"""

    @property
    def height(self) -> float:
        return self._eval_on_object('height')

    """True if the layer has no expressly set name, but contains a named source"""

    @property
    def is_name_from_source(self) -> bool:
        return self._eval_on_object('isNameFromSource')

    """True if this layer is being used as a track matte"""

    @property
    def is_track_matte(self) -> bool:
        return self._eval_on_object('isTrackMatte')

    """True if motion blur is enabled for the layer"""

    @property
    def motion_blur(self) -> bool:
        return self._eval_on_object('motionBlur')

    @motion_blur.setter
    def motion_blur(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"motionBlur = {extend_value}")

    """True if preserve transparency is enabled for the layer"""

    @property
    def preserve_transparency(self) -> bool:
        return self._eval_on_object('preserveTransparency')

    @preserve_transparency.setter
    def preserve_transparency(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"preserveTransparency = {extend_value}")

    """The source AVItem for this layer"""

    @property
    def source(self) -> float:
        kwargs = self._eval_on_object('source')
        object_type = kwargs["object_type"]
        return create_python_object(object_type)(**kwargs) if kwargs else None

    """The width of the layer in pixels"""

    @property
    def width(self) -> float:
        return self._eval_on_object('width')


class CameraLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class LightLayer(Layer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class ShapeLayer(AVLayer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class TextLayer(AVLayer):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class LayerCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type, "length")

    def __getitem__(self, index: int):
        index = index + 1
        kwargs = super(LayerCollection, self).__getitem__(index)
        object_type = kwargs["object_type"]
        layer = create_python_object(object_type)(**kwargs)
        return layer

    def __iter__(self):
        value = iter([self.__getitem__(i) for i in range(len(self))])
        return value

    # FUNCTIONS

    def add(self, item: Item, duration: float = None) -> Layer:
        """Creates a new layer containing a specified Item"""
        extend_item_object = format_to_extend(item)
        if duration:
            kwargs = self._eval_on_object(f"add({extend_item_object}, {duration})")
        else:
            kwargs = self._eval_on_object(f"add({extend_item_object})")
        object_type = kwargs["object_type"]
        layer = create_python_object(object_type)(**kwargs)
        return layer

    def add_box_text(self, width: int, height: int) -> TextLayer:
        """Creates a new paragraph text layer"""
        kwargs = self._eval_on_object(f"addBoxText([{width},{height}])")
        return TextLayer(**kwargs) if kwargs else None

    def add_camera(self, name: str, center_point: list) -> CameraLayer:
        """Creates a new camera layer"""
        kwargs = self._eval_on_object(f'addCamera("{name}", {center_point})')
        return CameraLayer(**kwargs) if kwargs else None

    def add_light(self, name: str, center_point: list):
        """Creates a new light layer"""
        kwargs = self._eval_on_object(f'addLight("{name}", {center_point})')
        return LightLayer(**kwargs) if kwargs else None

    def add_null(
            self, duration: float or str, duration_in_current_format: bool = True
    ) -> AVLayer:
        """Creates a new Null layer"""
        if duration_in_current_format:
            frame_rate = self[0].containing_comp.frame_rate
            duration = time_to_current_format(duration, frame_rate)
        kwargs = self._eval_on_object(f"addNull({duration})")
        return AVLayer(**kwargs) if kwargs else None

    def add_shape(self) -> ShapeLayer:
        """Creates a new Shape layer"""
        kwargs = self._eval_on_object("addShape()")
        return ShapeLayer(**kwargs) if kwargs else None

    def add_solid(
            self,
            color: list or str,
            name: str,
            width: int,
            height: int,
            pixel_aspect: float,
    ) -> LightLayer:
        """Creates a new Solid layer"""
        if isinstance(color, str):
            color = hex_to_rgb(color)
        kwargs = self._eval_on_object(
            f'addSolid({color}, "{name}", {width}, {height}, {pixel_aspect})'
        )
        return LightLayer(**kwargs) if kwargs else None

    def add_text(self, source_text: str = "") -> TextLayer:
        """Creates a new Text layer"""
        kwargs = self._eval_on_object(f'addText("{source_text}")')
        return TextLayer(**kwargs) if kwargs else None

    def by_name(self, name: str) -> Layer:
        """Returns the first (topmost) layer found in this collection with the specified name,
        or null if no layer with the given name is found."""
        kwargs = self._eval_on_object(f'byName("{name}")')
        object_type = kwargs["object_type"]
        layer = create_python_object(object_type)(**kwargs)
        return layer

    def precompose(
            self, indices: list, name: str, move_attributes: bool = True
    ) -> CompItem:
        """Creates a new CompItem object and moves the specified layers into its layer collection"""
        if len(indices) != 1 and not move_attributes:
            # coco - technically this is an "AfterEffectsError" not a "ValueError" - discuss in review
            raise ValueError(
                "Cannot set move attributes to false when precomposing with more than one layer"
            )
        indices = [index + 1 for index in indices]
        if not move_attributes:
            extend_move_attributes = format_to_extend(move_attributes)
            kwargs = self._eval_on_object(
                f'precompose({indices}, "{name}", "{extend_move_attributes}")'
            )
        else:
            kwargs = self._eval_on_object(f'precompose({indices}, "{name}")')
        return CompItem(**kwargs) if kwargs else None
