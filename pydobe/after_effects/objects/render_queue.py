from __future__ import annotations

from pydobe.core import PydobeBaseObject


class RenderQueue(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)
