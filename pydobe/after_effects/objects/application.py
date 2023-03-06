from __future__ import annotations

from pydobe.core import (
    PydobeBaseObject,
    format_to_extend,
)
from pydobe.after_effects.ae_utils import *
from pydobe.adobe_objects import File
from .project import Project


# BASE OBJECTS


class Application(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """Available GPU Acceleration types for the current viewer"""

    @property
    def available_gpu_accel_types(self) -> list[int]:
        return self._eval_on_object("availableGPUAccelTypes")

    """ This is the current active project. """

    @property
    def project(self) -> Project:
        kwargs = self._eval_on_object("project")
        return Project(**kwargs) if kwargs else None

    # FUNCTIONS

    def new_project(self, save: bool = None) -> Project:
        """Create a new empty project."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        kwargs = self._eval_on_object("newProject()")
        return Project(**kwargs) if kwargs else None

    def open(self, path: str = None, save: bool = None) -> Project:
        """A new Project object for the specified project, or null if the user cancels the Open dialog box."""
        if save is None:
            pass
        elif save:
            self.project.close(save=True)
        else:
            self.project.close(save=False)
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            kwargs = self._eval_on_object(f"open({extend_file_object})")
        else:
            kwargs = self._eval_on_object(f"open()")
        return Project(**kwargs) if kwargs else None
