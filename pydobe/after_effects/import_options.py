from __future__ import annotations

from pydobe.shared.file_ import File
from pydobe.core import PydobeBaseObject, format_to_extend


class ImportOptions(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    """The file object to be imported"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    @file.setter
    def file(self, value: File):
        extend_object = format_to_extend(value)
        self._eval_on_object(f"file = {extend_object}")

    """Creates sequence from available files in alphabetical order with no gaps"""

    @property
    def force_alphabetical(self) -> bool:
        return self._eval_on_object("forceAlphabetical")

    @force_alphabetical.setter
    def force_alphabetical(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"forceAlphabetical = {extend_value}")

    """Import as sequence"""

    @property
    def sequence(self) -> bool:
        return self._eval_on_object("sequence")

    @sequence.setter
    def sequence(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"sequence = {extend_value}")
