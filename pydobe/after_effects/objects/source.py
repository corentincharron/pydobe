from __future__ import annotations

from pydobe.adobe_objects import File
from pydobe.after_effects.data import alpha_dictionary, field_separation_dictionary, pulldown_dictionary
from pydobe.core import PydobeBaseObject, format_to_extend
from pydobe.utils import hex_to_rgb


class FootageSource(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """Defines how the alpha information in the footage is interpreted."""

    @property
    def alpha_mode(self) -> str:
        value = self._eval_on_object("alphaMode")
        value_as_string = alpha_dictionary[value]
        return value_as_string

    @alpha_mode.setter
    def alpha_mode(self, value: str or int):
        if isinstance(value, str):
            value = alpha_dictionary[value]
        self._eval_on_object(f"alphaMode = {value}")

    """A frame rate to use instead of the native frame rate value."""

    @property
    def conform_frame_rate(self) -> float:
        return self._eval_on_object("conformFrameRate")

    @conform_frame_rate.setter
    def conform_frame_rate(self, value: float):
        self._eval_on_object(f'conformFrameRate = "{value}"')

    """The effective frame rate as displayed and rendered in compositions by After Effects."""

    @property
    def display_frame_rate(self) -> float:
        return self._eval_on_object("displayFrameRate")

    """How the fields are to be separated in non-still footage."""

    @property
    def field_separation_type(self) -> str:
        value = self._eval_on_object("fieldSeparationType")
        value_as_string = field_separation_dictionary[value]
        return value_as_string

    @field_separation_type.setter
    def field_separation_type(self, value: int or str):
        if isinstance(value, str):
            value = field_separation_dictionary[value]
        self._eval_on_object(f"fieldSeparationType = {value}")

    """When true, the footage has an alpha component."""

    @property
    def has_alpha(self) -> bool:
        return self._eval_on_object("hasAlpha")

    """When true, After Effects performs high-quality field separation."""

    @property
    def high_quality_field_separation(self) -> bool:
        return self._eval_on_object("highQualityFieldSeparation")

    @high_quality_field_separation.setter
    def high_quality_field_separation(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"highQualityFieldSeparation = {extend_value}")

    """When true, the footage has an alpha component."""

    @property
    def invert_alpha(self) -> bool:
        return self._eval_on_object("invertAlpha")

    @invert_alpha.setter
    def invert_alpha(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"invertAlpha = {extend_value}")

    """When true the footage is still; when false, it has a time-based component."""

    @property
    def is_still(self) -> bool:
        return self._eval_on_object("isStill")

    """The number of times that the footage is to be played consecutively when used in a composition."""

    @property
    def loop(self) -> int:
        return self._eval_on_object("loop")

    @loop.setter
    def loop(self, value: int):
        self._eval_on_object(f"loop = {value}")

    """The native frame rate of the footage."""

    @property
    def native_frame_rate(self) -> float:
        return self._eval_on_object("nativeFrameRate")

    """The color to be premultiplied."""

    @property
    def premul_color(self) -> int:
        return self._eval_on_object("premulColor")

    @premul_color.setter
    def premul_color(self, value: list or str):
        if isinstance(value, str):
            value = hex_to_rgb(value)
        self._eval_on_object(f"premulColor = {value}")

    """How the pulldowns are to be removed when field separation is used"""

    @property
    def remove_pulldown(self) -> str:
        value = self._eval_on_object("removePulldown")
        value_as_string = pulldown_dictionary[value]
        return value_as_string

    @remove_pulldown.setter
    def remove_pulldown(self, value: int or str):
        if isinstance(value, str):
            value = pulldown_dictionary[value]
        self._eval_on_object(f"removePulldown = {value}")

    # FUNCTIONS

    def guess_alpha_mode(self):
        """Sets alphaMode, premulColor, and invertAlpha to the best estimates for this footage source"""
        self._eval_on_object("guessAlphaMode()")

    def guess_pulldown(self, advance_24p=False):
        """Sets fieldSeparationType and removePulldown to the best estimates for this footage source."""
        if advance_24p:
            self._eval_on_object(f"guessPulldown(PulldownMethod.ADVANCE_24P)")
        else:
            self._eval_on_object(f"guessPulldown(PulldownMethod.PULLDOWN_3_2)")


class FileSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The file"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    """The path and filename of footage that is missing from this asset."""

    @property
    def missing_footage_path(self) -> str:
        return self._eval_on_object("missingFootagePath")

    # FUNCTIONS

    def reload(self):
        """Reloads the asset from the file."""
        self._eval_on_object("reload()")


class PlaceholderSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)


class SolidSource(FootageSource):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The color of the solid"""

    @property
    def color(self) -> float:
        return self._eval_on_object("color")

    @color.setter
    def color(self, value: list or str):
        if isinstance(value, str):
            value = hex_to_rgb(value)
        self._eval_on_object(f"color = {value}")
