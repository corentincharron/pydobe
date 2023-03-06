from pydobe.core import PydobeBaseObject


class Folder(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    """The name of the folder"""

    @property
    def name(self) -> str:
        return self._eval_on_object("name")

    "The path portion of the absolute URI, without the folder name"

    @property
    def path(self) -> str:
        return self._eval_on_object("path")
