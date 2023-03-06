from __future__ import annotations

from pydobe.core import PydobeBaseObject, format_to_extend


class Viewer(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """When true, indicates if the viewer panel is focused."""

    @property
    def active(self) -> bool:
        return self._eval_on_object("active")

    """When true, indicates if the viewer panel is at its maximized size."""

    @property
    def maximised(self) -> bool:
        return self._eval_on_object("maximized")

    @maximised.setter
    def maximised(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"maximized = {extend_value}")

    # FUNCTIONS

    def set_active(self) -> bool:
        """Moves the viewer panel to the front and places focus on it, making it active."""
        return self._eval_on_object("setActive()")
