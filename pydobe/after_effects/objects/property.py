from __future__ import annotations

from pydobe.core import PydobeBaseObject, format_to_extend


class PropertyBase(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """True if the layer, property, or effect is active
        Will return False if other layers are solo, or if time is not between layers in and out point"""

    @property
    def active(self) -> bool:
        return self._eval_on_object("active")

    """True if you can set the enabled attribute value"""

    @property
    def can_set_enabled(self) -> bool:
        return self._eval_on_object("canSetEnabled")

    """True if the layer, property, or effect is enabled"""

    @property
    def enabled(self) -> bool:
        return self._eval_on_object("enabled")

    @enabled.setter
    def enabled(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"enabled = {extend_value}")

    """When true, this property is an effect property group"""

    @property
    def is_effect(self) -> bool:
        return self._eval_on_object("isEffect")

    """When true, this property is a mask property group"""

    @property
    def is_mask(self) -> bool:
        return self._eval_on_object("isMask")

    """When true, this property has been changed since it's creation"""

    @property
    def is_modified(self) -> bool:
        return self._eval_on_object("isModified")

    """A special name for the property used to build unique naming paths.
    Every property has a unique match-name identifier."""

    @property
    def match_name(self) -> bool:
        return self._eval_on_object("matchName")

    """The name of a layer, or the display name of a property"""

    @property
    def name(self) -> str:
        return self._eval_on_object("name")

    @name.setter
    def name(self, value: str):
        self._eval_on_object(f'name = "{value}"')

    """The property group that is the parent of this property. Null if this is a layer"""

    @property
    def parent_property(self) -> PropertyGroup:
        kwargs = self._eval_on_object("parentProperty")
        return PropertyGroup(**kwargs) if kwargs else None

    """When true, the property is selected"""

    @property
    def selected(self) -> bool:
        return self._eval_on_object("selected")

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"selected = {extend_value}")


class Property(PropertyBase):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """Returns the value of the current property"""

    @property
    def value(self):
        return self._eval_on_object('value')

    # FUNCTIONS

    def set_value(self, value):
        if isinstance(value, type(self.value)):
            self._eval_on_object(f'setValue ({value})')
        else:
            raise ValueError(f"Unable to set '{self.name}', value must be of type '{type(self.value).__name__}'")


class PropertyGroup(PropertyBase):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    @property
    def num_properties(self) -> object:
        return self._eval_on_object('numProperties')
