from __future__ import annotations

import pydobe
from pydobe.core import (
    PydobeBaseObject,
    format_to_extend,
    create_python_object,
)
from pydobe.adobe_objects import File, Folder
from pydobe.logging_ import logger
from pydobe.after_effects.data import *
from pydobe.after_effects.utils import *
from .render_queue import RenderQueue
from .item import Item, FolderItem, FootageItem, ItemCollection
from .import_options import ImportOptions
from .layer import Layer


class Project(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The item that is currently active and is to be acted upon, 
    or a null if no item is currently selected or if multiple items are selected."""

    @property
    def active_item(self) -> Item:
        kwargs = self._eval_on_object("activeItem")
        if not kwargs:
            raise TypeError("'active_item' requires precisely one item to be selected")
        object_type = kwargs["object_type"]
        item = create_python_object(object_type)(**kwargs)
        return item

    """The color depth of the project, either 8, 16, or 32 bit"""

    @property
    def bits_per_channel(self) -> int:
        return self._eval_on_object("bitsPerChannel")

    @bits_per_channel.setter
    def bits_per_channel(self, value: int):
        if value not in [8, 16, 32]:
            message = "Unable to set 'bits_per_channel', value must be 8, 16, or 32"
            logger.error(message)
            raise ValueError(message)
        else:
            self._eval_on_object(f"bitsPerChannel = {value}")

    """Compensate for scene referred profiles"""

    @property
    def compensate_for_scene_referred_profiles(self) -> bool:
        return self._eval_on_object("compensateForSceneReferredProfiles")

    @compensate_for_scene_referred_profiles.setter
    def compensate_for_scene_referred_profiles(self, value):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"compensateForSceneReferredProfiles = {extend_value}")

    """Returns True if file has been modified since last save. False if it has not"""

    @property
    def dirty(self) -> bool:
        return self._eval_on_object("dirty")

    """Alternate way to set Frame count menu setting"""

    @property
    def display_start_frame(self) -> int:
        return self._eval_on_object("displayStartFrame")

    @display_start_frame.setter
    def display_start_frame(self, value: int):
        if value > 1:
            raise ValueError("Display start frame must be set to either 0 or 1")
        self._eval_on_object(f"displayStartFrame = {value}")

    """The expression engine setting in the Project Settings dialog box"""

    @property
    def expression_engine(self) -> str:
        return self._eval_on_object("expressionEngine")

    @expression_engine.setter
    def expression_engine(self, value: str):
        if value != "javascript-1.0" and value != "extendscript":
            raise ValueError("No engine exists by this name")
        self._eval_on_object(f'expressionEngine = "{value}"')

    """The Use Feet + Frames menu setting"""

    @property
    def feet_frames_film_type(self) -> str:
        value = self._eval_on_object("feetFramesFilmType")
        value_as_string = feet_and_frames_dictionary[value]
        return value_as_string

    @feet_frames_film_type.setter
    def feet_frames_film_type(self, value: int or str):
        if isinstance(value, str):
            value = feet_and_frames_dictionary[value]
        self._eval_on_object(f"feetFramesFilmType = {value}")

    """"Identifies the file object containing the project"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    """The footage start type menu setting"""

    @property
    def footage_timecode_display_start_type(self) -> int:
        value = self._eval_on_object("footageTimecodeDisplayStartType")
        value_as_string = footage_start_time_dictionary[value]
        return value_as_string

    @footage_timecode_display_start_type.setter
    def footage_timecode_display_start_type(self, value: int):
        if isinstance(value, str):
            value = footage_start_time_dictionary[value]
        self._eval_on_object(f"footageTimecodeDisplayStartType = {value}")

    """The frame count menu setting"""

    @property
    def frames_count_type(self) -> str:
        value = self._eval_on_object("framesCountType")
        value_as_string = frames_count_dictionary[value]
        return value_as_string


    @frames_count_type.setter
    def frames_count_type(self, value: int):
        if isinstance(value, str):
            value = frames_count_dictionary[value]
        self._eval_on_object(f"framesCountType = {value}")

    """The Use Feet + Frames menu setting - 16mm or 35mm"""

    @property
    def frames_use_feet_frames(self) -> bool:
        return self._eval_on_object("framesUseFeetFrames")

    @frames_use_feet_frames.setter
    def frames_use_feet_frames(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"framesUseFeetFrames = {extend_value}")

    """The frame count menu setting"""

    @property
    def gpu_accel_type(self) -> str:
        value = self._eval_on_object("gpuAccelType")
        value_as_string = gpu_accel_type_dictionary[value]
        return value_as_string

    @gpu_accel_type.setter
    def gpu_accel_type(self, value: int):
        if isinstance(value, str):
            value = gpu_accel_type_dictionary[value]
        if value not in pydobe.objects.app.available_gpu_accel_types:
            raise ValueError("This GPU Acceleration is not available")
        self._eval_on_object(f"gpuAccelType = {value}")

    """All of the items in the project"""

    @property
    def items(self) -> ItemCollection:
        kwargs = self._eval_on_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """True if linear blending should be enabled for this project"""

    @property
    def linear_blending(self) -> bool:
        return self._eval_on_object("linearBlending")

    @linear_blending.setter
    def linear_blending(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"linearBlending = {extend_value}")

    """True if linearize working space should be enabled for this project"""

    @property
    def linearize_working_space(self) -> bool:
        return self._eval_on_object("linearizeWorkingSpace")

    @linearize_working_space.setter
    def linearize_working_space(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"linearizeWorkingSpace = {extend_value}")

    """The number of items within the project"""

    @property
    def num_items(self) -> int:
        return self._eval_on_object("numItems")

    """The render queue of the project."""

    @property
    def render_queue(self) -> RenderQueue:
        kwargs = self._eval_on_object("renderQueue")
        return RenderQueue(**kwargs) if kwargs else None

    """The current revision of the project"""

    @property
    def revision(self) -> int:
        return self._eval_on_object("revision")

    """The root folder containing the contents of the project
    Items inside internal folders will not be shown"""

    @property
    def root_folder(self) -> FolderItem:
        kwargs = self._eval_on_object("rootFolder")
        return FolderItem(**kwargs) if kwargs else None

    "All items selected in the Project Panel"

    @property
    def selection(self) -> list[Item]:
        item_list = []
        kwargs_list = self._eval_on_object("selection")
        for kwargs in kwargs_list:
            object_type = kwargs["object_type"]
            item = create_python_object(object_type)(**kwargs)
            item_list.append(item)
        return item_list

    """The time display style"""

    @property
    def time_display_type(self) -> str:
        value = self._eval_on_object("timeDisplayType")
        value_as_string = time_display_dictionary[value]
        return value_as_string

    @time_display_type.setter
    def time_display_type(self, value: int or str):
        if isinstance(value, str):
            value = time_display_dictionary[value]
        self._eval_on_object(f"timeDisplayType = {value}")

    """The active tool in the tools panel"""

    @property
    def tool_type(self) -> str:
        value = self._eval_on_object("toolType")
        value_as_string = tool_dictionary[value]
        return value_as_string

    @tool_type.setter
    def tool_type(self, value: int or str):
        if isinstance(value, str):
            value = tool_dictionary[value]
        self._eval_on_object(f"toolType = {value}")

    """When true, thumbnail views use the transparency checkerboard pattern."""

    @property
    def transparency_grid_thumbnails(self) -> bool:
        return self._eval_on_object("transparencyGridThumbnails")

    @transparency_grid_thumbnails.setter
    def transparency_grid_thumbnails(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"transparencyGridThumbnails = {extend_value}")

    """Working gamma value. Only used when color working space is set to none"""

    @property
    def working_gamma(self) -> float:
        return self._eval_on_object("workingGamma")

    @working_gamma.setter
    def working_gamma(self, value: float):
        if value not in [2.2, 2.4]:
            raise ValueError("Unable to set 'working_gamma', value must be 2.2 or 2.4")
        else:
            self._eval_on_object(f'workingGamma = "{value}"')

    """Color profile description"""

    @property
    def working_space(self) -> str:
        return self._eval_on_object("workingSpace")

    @working_space.setter
    def working_space(self, value: str):
        if value in self.list_color_profiles():
            self._eval_on_object(f'workingSpace = "{value}"')
        else:
            raise ValueError(
                "Unable to set 'workingSpace', value must be an accepted color profile"
            )

    """The project’s XMP metadata, stored as RDF (XML-based)"""

    @property
    def xmp_packet(self) -> str:
        return self._eval_on_object("xmpPacket")

    @xmp_packet.setter
    def xmp_packet(self, value: str):
        self._eval_on_object(f'xmpPacket = "{value}"')

    # CUSTOM PROPERTIES

    """All of the composition items within the project"""

    @property
    def compositions(self) -> list:
        composition_items = []
        for item in self.items:
            if item.object_type == "CompItem":
                composition_items.append(item)
        return composition_items

    """All of the footage items within the project"""

    @property
    def footages(self) -> list:
        footage_items = []
        for item in self.items:
            if item.object_type == "FootageItem":
                footage_items.append(item)
        return footage_items

    """All of the folder items within the project"""

    @property
    def folders(self) -> list:
        folder_items = []
        for item in self.items:
            if item.object_type == "FolderItem":
                folder_items.append(item)
        return folder_items

    # FUNCTIONS

    def auto_fix_expressions(self, old_text, new_text):
        """Automatically replaces text found in broken expressions in the project"""
        self._eval_on_object(f'autoFixExpressions("{old_text}", "{new_text})')

    def close(self, save: bool = None) -> bool:
        """This will close the current project with an option to save changes or not"""
        if save is None:
            return self._eval_on_object("close(CloseOptions.PROMPT_TO_SAVE_CHANGES)")
        elif save:
            return self._eval_on_object("close(CloseOptions.SAVE_CHANGES)")
        else:
            return self._eval_on_object("close(CloseOptions.DO_NOT_SAVE_CHANGES)")

    def consolidate_footage(self) -> int:
        """Consolidates all footage in the project, returns total number of footage items removed"""
        return self._eval_on_object("consolidateFootage()")

    def import_file(
            self, path: str, sequence: bool = False, force_alphabetical: bool = False
    ):
        """This will import a file"""
        import_options = ImportOptions(
            **eval_script_returning_object("new ImportOptions()")
        )
        file = File(**eval_script_returning_object(f'File("{path}")'))
        import_options.file = file
        import_options.sequence = sequence
        import_options.force_alphabetical = force_alphabetical
        extend_import_options = format_to_extend(import_options)
        kwargs = self._eval_on_object(f"importFile({extend_import_options})")
        return FootageItem(**kwargs) if kwargs else None

    def import_file_with_dialog(self) -> list:
        """Shows an import file dialog box"""
        return self._eval_on_object("importFileWithDialog()")

    def import_placeholder(
            self,
            name: str,
            width: int,
            height: int,
            frame_rate: float,
            duration: float or str,
            duration_in_current_format: bool = True,
    ) -> object:
        """Shows an import file dialog box"""
        if duration_in_current_format:
            duration = time_to_current_format(duration, frame_rate)
        kwargs = self._eval_on_object(
            f'importPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})'
        )
        return FootageItem(**kwargs) if kwargs else None

    def item(self, index: int) -> object:
        """Retrieves an item at a specified index position"""
        index = index + 1
        kwargs = self._eval_on_object(f"item({index})")
        object_type = kwargs["object_type"]
        item = create_python_object(object_type)(**kwargs)
        return item

    def item_by_id(self, item_id: int) -> Item:
        """Retrieves an item by its ID"""
        kwargs = self._eval_on_object(f"itemByID({item_id})")
        object_type = kwargs["object_type"]
        item = create_python_object(object_type)(**kwargs)
        return item

    def layer_by_id(self, layer_id: int) -> Layer:
        """Retrieves a layer by its ID"""
        kwargs = self._eval_on_object(f"layerByID({layer_id})")
        object_type = kwargs["object_type"]
        layer = create_python_object(object_type)(**kwargs)
        return layer

    def reduce_project(self, items: list[Item]) -> int:
        """Removes all items from the project except those specified"""
        extend_items = format_to_extend(items)
        return self._eval_on_object(f"reduceProject({extend_items})")

    def remove_unused_footage(self) -> int:
        """Removes unused footage from the project"""
        return self._eval_on_object(f"removeUnusedFootage()")

    def set_default_import_folder(self, path: str) -> bool:
        """Sets the folder that will be shown in the file import dialog"""
        folder = Folder(**eval_script_returning_object(f'Folder("{path}")'))
        extend_folder = format_to_extend(folder)
        return self._eval_on_object(f"setDefaultImportFolder({extend_folder})")

    def save(self, path: str = None) -> bool:
        """This will save the current scene"""
        if path:
            file = File(**eval_script_returning_object(f'File("{path}")'))
            extend_file_object = format_to_extend(file)
            return self._eval_on_object(f"save({extend_file_object})")
        else:
            return self._eval_on_object("save()")

    def save_with_dialog(self) -> bool:
        """This will prompt the user to save with a dialog box"""
        return self._eval_on_object("saveWithDialog()")

    def show_window(self, show: bool):
        """Shows or hides the Project panel."""
        extend_show = format_to_extend(show)
        return self._eval_on_object(f"showWindow({extend_show})")

    def list_color_profiles(self) -> list[list]:
        """List of available color profile descriptions"""
        return self._eval_on_object(f"listColorProfiles()")

    # CUSTOM FUNCTIONS

    def item_by_name(self, name: str) -> Item:
        """Get an item by its name from within this project"""
        for item in self.items:
            if item.name == name:
                return item
        raise LookupError("There is no item by this name in your project")

    def save_incremental(self):
        """Save incremental"""
        self._execute_command("app.executeCommand(3088)")

