from __future__ import annotations

from pydobe.core import PydobeBaseObject, format_to_extend, eval_script_returning_object, create_python_object, \
    PydobeBaseCollection
from pydobe.utils import hex_to_rgb
from pydobe.adobe_objects import File
from pydobe.after_effects.utils import time_to_current_format, current_format_to_time
from pydobe.after_effects.data import label_dictionary

from .source import FileSource, FootageSource
from .layer import CameraLayer, LayerCollection
from .property import Property, PropertyGroup
from .viewer import Viewer


class Item(PydobeBaseObject):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    def __str__(self):
        return self.name

    # PROPERTIES

    """A string that holds a comment, the comment is for the user’s purpose only"""

    @property
    def comment(self) -> str:
        return self._eval_on_object("comment")

    @comment.setter
    def comment(self, value: str):
        self._eval_on_object(f'comment = "{value}"')

    """A unique and persistent identification number used for the dynamic link"""

    @property
    def dynamic_link_guide(self):
        return self._eval_on_object("dynamicLinkGUID")

    """An array of guide objects, containing orientationType, positionType, and position attributes."""

    @property
    def guides(self):
        return self._eval_on_object("guides")

    """A unique and persistent identification number used internally to identify an item between sessions"""

    @property
    def id(self) -> int:
        return self._eval_on_object("id")

    """The color of the label assigned to the item, expressed as an integer between 1-16. 0 = none"""

    @property
    def label(self) -> str:
        value = self._eval_on_object("label")
        value_as_string = label_dictionary[value]
        return value_as_string

    @label.setter
    def label(self, value: int or str):
        if isinstance(value, int):
            if value not in range(17):
                raise ValueError("Cannot set label, value must be between 0 and 16")
            int_value = value
        else:
            if not label_dictionary.get(value):
                raise ValueError(
                    "Cannot set label, value is not an available label color"
                )
            int_value = label_dictionary[value]
        self._eval_on_object(f"label = {int_value};")

    """The name of the item as displayed in the Project panel"""

    @property
    def name(self) -> str:
        return self._eval_on_object("name")

    @name.setter
    def name(self, value: str):
        self._eval_on_object(f'name = "{value}"')

    """The folder object that the item is parented to"""

    @property
    def parent_folder(self) -> FolderItem:
        kwargs = self._eval_on_object("parentFolder")
        return FolderItem(**kwargs) if kwargs else None

    @parent_folder.setter
    def parent_folder(self, value: FolderItem):
        if value.object_type == "FolderItem":
            extend_value = format_to_extend(value)
            self._eval_on_object(f"parentFolder = {extend_value}")
        else:
            raise TypeError("Unable to set 'parent_folder', type must be 'Folder'")

    """Whether the item is selected or not, multiple items can be selected at the same time"""

    @property
    def selected(self) -> bool:
        return self._eval_on_object("selected")

    @selected.setter
    def selected(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"selected = {extend_value}")

    """User readable name for Item type"""

    @property
    def type_name(self) -> str:
        return self._eval_on_object("typeName")

    # FUNCTIONS

    def add_guide(self, orientation: int, position: int):
        """Creates a new guide and adds it to the guides object of the Item."""
        self._eval_on_object(f"addGuide({orientation},{position})")

    def duplicate(self):
        """Duplicates the Item"""
        self._execute_command("app.executeCommand(2080)")

    def remove(self):
        """Deletes this item from the project and the Project panel.
        If the item is a FolderItem, all the items contained in the folder are also removed from the project
        """
        self._eval_on_object("remove()")

    def remove_guide(self, index: int):
        """Removes an existing guide. Choose the guide based on its index"""
        if index not in range(len(self.guides)):
            raise ValueError("The index provided is outside of the range of guides")
        self._eval_on_object(f"removeGuide({index})")

    def set_guide(self, position: int, index: int):
        """Modifies the position of an existing guide"""
        if index not in range(len(self.guides)):
            raise ValueError("The index provided is outside of the range of guides")
        self._eval_on_object(f"setGuide({position}, {index})")


class AVItem(Item):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    """Duration of the item in seconds"""

    @property
    def duration(self) -> float:
        return self._eval_on_object("duration")

    @duration.setter
    def duration(self, value: float):
        self._eval_on_object(f"duration = {value}")

    """When true the item is a placeholder"""

    @property
    def footage_missing(self) -> float:
        return self._eval_on_object("footageMissing")

    """Returns the length of a frame for this AVItem, in seconds."""

    @property
    def frame_duration(self) -> float:
        return self._eval_on_object("frameDuration")

    @frame_duration.setter
    def frame_duration(self, value: float):
        self._eval_on_object(f"frameDuration = {value}")

    """The fps of the item, when set the frame duration is automatically set"""

    @property
    def frame_rate(self) -> float:
        return self._eval_on_object("frameRate")

    @frame_rate.setter
    def frame_rate(self, value: float):
        self._eval_on_object(f"frameRate = {value}")

    """Returns True if the item has an audio component"""

    @property
    def has_audio(self) -> bool:
        return self._eval_on_object("hasAudio")

    """Returns True if the item has an video component"""

    @property
    def has_video(self) -> bool:
        return self._eval_on_object("hasVideo")

    """The height of the item in pixels"""

    @property
    def height(self) -> int:
        return self._eval_on_object("height")

    @height.setter
    def height(self, value: int):
        self._eval_on_object(f"height = {value}")

    """Test whether the AVItem can be used as an alternate source when calling Property.set_alternate_source()."""

    @property
    def is_media_replacement_compatible(self) -> bool:
        return self._eval_on_object("isMediaReplacementCompatible")

    """The pixel aspect ratio of the item"""

    @property
    def pixel_aspect(self) -> float:
        return self._eval_on_object("pixelAspect")

    @pixel_aspect.setter
    def pixel_aspect(self, value: float):
        self._eval_on_object(f"pixelAspect = {value}")

    """The Footage Source being used as a proxy"""

    @property
    def proxy_source(self) -> FileSource:
        kwargs = self._eval_on_object("proxySource")
        return FileSource(**kwargs) if kwargs else None

    """The current time of the item when it is being previewed"""

    @property
    def time(self) -> float:
        return self._eval_on_object("time")

    @time.setter
    def time(self, value: float):
        self._eval_on_object(f'time = "{value}"')

    """A list of compositions that use this item"""

    @property
    def used_in(self) -> list:
        comp_list = []
        kwargs_list = self._eval_on_object("usedIn")
        for kwargs in kwargs_list:
            comp = CompItem(**kwargs)
            comp_list.append(comp)
        return comp_list

    """The width of the item in pixels"""

    @property
    def use_proxy(self) -> bool:
        return self._eval_on_object("useProxy")

    @use_proxy.setter
    def use_proxy(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f'useProxy = "{extend_value}"')

    """The width of the item in pixels"""

    @property
    def width(self) -> int:
        return self._eval_on_object("width")

    @width.setter
    def width(self, value: int):
        self._eval_on_object(f"width = {value}")

    # CUSTOM PROPERTIES

    @property
    def time_in_current_format(self) -> str:
        return time_to_current_format(self.time, self.frame_rate)

    @time_in_current_format.setter
    def time_in_current_format(self, value: str):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'time = "{value}"')

    @property
    def duration_in_current_format(self) -> str:
        return time_to_current_format(self.duration, self.frame_rate)

    @duration_in_current_format.setter
    def duration_in_current_format(self, value: str):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f'duration = "{value}"')

    # FUNCTIONS

    def set_proxy(self, file_path: str):
        """Sets a file as the proxy of this AVItem."""
        file = File(**eval_script_returning_object(f'File("{file_path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_object(f"setProxy({extend_file_object})")

    def set_proxy_to_none(self):
        """Removes the proxy from this AVItem"""
        self._eval_on_object("setProxyToNone()")

    def set_proxy_with_placeholder(
            self, name: str, width: int, height: int, frame_rate: int, duration: float
    ):
        """Creates a PlaceholderSource object with specified values, sets this as the value of the proxySource
        attribute"""
        self._eval_on_object(
            f'setProxyWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})'
        )

    def set_proxy_with_sequence(self, file_path: str, force_alphabetical: bool = False):
        """Sets a sequence of files as the proxy of this AVItem"""
        file = File(**eval_script_returning_object(f'File("{file_path}")'))
        extend_file_object = format_to_extend(file)
        extend_force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_object(
            f"setProxyWithSequence({extend_file_object}, {extend_force_alphabetical})"
        )

    def set_proxy_with_solid(
            self, color: list, name: str, width: int, height: int, pixel_aspect: float
    ):
        """Creates a SolidSource object with specified values, sets this as the value of the proxySource attribute"""
        self._eval_on_object(
            f'setProxyWithSolid({color}, "{name}", {width}, {height}, {pixel_aspect})'
        )


class CompItem(AVItem):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The front most camera layer that is enabled"""

    @property
    def active_camera(self) -> CameraLayer:
        kwargs = self._eval_on_object("activeCamera")
        return CameraLayer(**kwargs)

    """The background color of the composition"""

    @property
    def bg_color(self):
        return self._eval_on_object("bgColor")

    @bg_color.setter
    def bg_color(self, value: list or str):
        if isinstance(value, str):
            value = hex_to_rgb(value)
        self._eval_on_object(f"bgColor = {value}")

    """The time set as the beginning of the composition in frames"""

    @property
    def display_start_frame(self) -> int:
        return self._eval_on_object("displayStartFrame")

    @display_start_frame.setter
    def display_start_frame(self, value: int):
        self._eval_on_object(f"displayStartFrame = {value}")

    """The time set as the beginning of the composition in seconds"""

    @property
    def display_start_time(self) -> float:
        return self._eval_on_object("displayStartTime")

    @display_start_time.setter
    def display_start_time(self, value: float):
        self._eval_on_object(f"displayStartTime = {value}")

    """When true, Draft 3D mode is enabled for the Composition panel."""

    @property
    def draft_3d(self) -> bool:
        return self._eval_on_object("draft3d")

    @draft_3d.setter
    def draft_3d(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"draft3d = {extend_value}")

    """When true, indicates that the composition uses drop-frame timecode."""

    @property
    def drop_frame(self) -> bool:
        return self._eval_on_object("dropFrame")

    @drop_frame.setter
    def drop_frame(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"dropFrame = {extend_value}")

    """When true, frame blending is enabled for this Composition."""

    @property
    def frame_blending(self) -> bool:
        return self._eval_on_object("frameBlending")

    @frame_blending.setter
    def frame_blending(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"frameBlending = {extend_value}")

    """The duration of a frame, in seconds. This is the inverse of the frameRate value"""

    @property
    def frame_duration(self) -> float:
        return self._eval_on_object("frameDuration")

    @frame_duration.setter
    def frame_duration(self, value: float):
        self._eval_on_object(f"frameDuration = {value}")

    """When true, only layers with shy set to false are shown in the Timeline panel"""

    @property
    def hide_shy_layers(self) -> bool:
        return self._eval_on_object("hideShyLayers")

    @hide_shy_layers.setter
    def hide_shy_layers(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"hideShyLayers = {extend_value}")

    """All of the layers in the composition"""

    @property
    def layers(self) -> LayerCollection:
        kwargs = self._eval_on_object("layers")
        return LayerCollection(**kwargs) if kwargs else None

    """A PropertyGroup object that contains all a composition’s markers."""

    @property
    def marker_property(self) -> PropertyGroup:
        kwargs = self._eval_on_object("markerProperty")
        return PropertyGroup(**kwargs) if kwargs else None

    """When true, only layers with shy set to false are shown in the Timeline panel"""

    @property
    def motion_blur(self) -> bool:
        return self._eval_on_object("motionBlur")

    @motion_blur.setter
    def motion_blur(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"motionBlur = {extend_value}")

    """The maximum number of motion blur samples of 2D layer motion."""

    @property
    def motion_blur_adaptive_sample_limit(self) -> int:
        return self._eval_on_object("motionBlurAdaptiveSampleLimit")

    @motion_blur_adaptive_sample_limit.setter
    def motion_blur_adaptive_sample_limit(self, value: int):
        if value not in range(16, 257):
            raise ValueError(
                "Cannot set motion blur adaptive sample limit, value must be between 16 and 256"
            )
        self._eval_on_object(f"motionBlurAdaptiveSampleLimit = {value}")

    """The minimum number of motion blur samples per frame for Classic 3D layers, shape layers, and certain effects"""

    @property
    def motion_blur_samples_per_frame(self) -> int:
        return self._eval_on_object("motionBlurSamplesPerFrame")

    @motion_blur_samples_per_frame.setter
    def motion_blur_samples_per_frame(self, value: int):
        if value not in range(2, 65):
            raise ValueError(
                "Cannot set motion blur adaptive sample limit, value must be between 2 and 64"
            )
        self._eval_on_object(f"motionBlurSamplesPerFrame = {value}")

    """The number of properties in the Essential Graphics panel for the composition"""

    @property
    def motion_graphics_template_controller_count(self) -> int:
        return self._eval_on_object("motionGraphicsTemplateControllerCount")

    """Name property in the Essential Graphics panel for the composition"""

    @property
    def motion_graphics_template_name(self) -> str:
        return self._eval_on_object("motionGraphicsTemplateName")

    @motion_graphics_template_name.setter
    def motion_graphics_template_name(self, value: str):
        self._eval_on_object(f'motionGraphicsTemplateName = "{value}"')

    """The number of Layers in the Composition"""

    @property
    def num_layers(self) -> int:
        return self._eval_on_object("numLayers")

    """When true, the frame rate of nested compositions is preserved in the current composition."""

    @property
    def preserve_nested_frame_rate(self) -> bool:
        return self._eval_on_object("preserveNestedFrameRate")

    @preserve_nested_frame_rate.setter
    def preserve_nested_frame_rate(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"preserveNestedFrameRate = {extend_value}")

    """When true, the resolution of nested compositions is preserved in the current composition."""

    @property
    def preserve_nested_resolution(self) -> bool:
        return self._eval_on_object("preserveNestedResolution")

    @preserve_nested_resolution.setter
    def preserve_nested_resolution(self, value: bool):
        extend_value = format_to_extend(value)
        self._eval_on_object(f"preserveNestedResolution = {extend_value}")

    """The current rendering plug-in module to be used to render this composition"""

    @property
    def renderer(self) -> str:
        return self._eval_on_object("renderer")

    @renderer.setter
    def renderer(self, value: str):
        if value not in self.renderers:
            raise ValueError(f"{value} is not a valid renderer")
        extend_value = format_to_extend(value)
        self._eval_on_object(f"renderer = {extend_value}")

    """The available rendering plugin modules"""

    @property
    def renderers(self) -> list:
        return self._eval_on_object("renderers")

    """The x and y downsample resolution factors for rendering the composition."""

    @property
    def resolution_factor(self) -> list[int]:
        return self._eval_on_object("resolutionFactor")

    @resolution_factor.setter
    def resolution_factor(self, value: list[int]):
        self._eval_on_object(f"resolutionFactor = {value}")

    """All of the selected layers in this composition."""

    @property
    def selected_layers(self) -> list:
        layer_list = []
        kwargs_list = self._eval_on_object("selectedLayers")
        for kwargs in kwargs_list:
            object_type = kwargs["object_type"]
            layer = create_python_object(object_type)(**kwargs)
            layer_list.append(layer)
        return layer_list

    """All of the selected properties in this composition."""

    @property
    def selected_properties(self):
        properties_list = []
        kwargs_list = self._eval_on_object("selectedProperties")
        for kwargs in kwargs_list:
            object_type = kwargs["object_type"]
            if object_type == "PropertyGroup" or object_type == "MaskPropertyGroup":
                property_ = PropertyGroup(**kwargs)
            else:
                property_ = Property(**kwargs)
            properties_list.append(property_)
        return properties_list

    """The shutter angle setting for the composition."""

    @property
    def shutter_angle(self) -> int:
        return self._eval_on_object("shutterAngle")

    @shutter_angle.setter
    def shutter_angle(self, value: int):
        if value not in range(721):
            raise ValueError(
                "Cannot set shutter angle, value must be between 0 and 720"
            )
        self._eval_on_object(f"shutterAngle = {value}")

    """The shutter phase setting for the composition."""

    @property
    def shutter_phase(self) -> int:
        return self._eval_on_object("shutterPhase")

    @shutter_phase.setter
    def shutter_phase(self, value: int):
        if value not in range(-360, 361):
            raise ValueError(
                "Cannot set shutter phase, value must be between -360 and 360"
            )
        self._eval_on_object(f"shutterPhase = {value}")

    """The duration of the work area in seconds"""

    @property
    def work_area_duration(self) -> float:
        return self._eval_on_object("workAreaDuration")

    @work_area_duration.setter
    def work_area_duration(self, value: float):
        self._eval_on_object(f"workAreaDuration = {value}")

    """The time when the Composition work area begins, in seconds."""

    @property
    def work_area_start(self) -> float:
        return self._eval_on_object("workAreaStart")

    @work_area_start.setter
    def work_area_start(self, value: float):
        self._eval_on_object(f"workAreaStart = {value}")

    # CUSTOM PROPERTIES

    @property
    def work_area_duration_in_current_format(self) -> str:
        duration = self._eval_on_object("workAreaDuration")
        formatted_duration = time_to_current_format(duration, self.frame_rate)
        return formatted_duration

    @work_area_duration_in_current_format.setter
    def work_area_duration_in_current_format(self, value: str or int):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f"workAreaDuration = {value}")

    @property
    def work_area_start_in_current_format(self) -> str:
        duration = self._eval_on_object("workAreaStart")
        formatted_duration = time_to_current_format(duration, self.frame_rate)
        return formatted_duration

    @work_area_start_in_current_format.setter
    def work_area_start_in_current_format(self, value: str or int):
        value = current_format_to_time(value, self.frame_rate)
        self._eval_on_object(f"workAreaStart = {value}")

    # FUNCTIONS

    def export_as_motion_graphics_template(
            self, overwrite: bool = True, path: str = None
    ) -> bool:
        """Exports the composition as a Motion Graphics template."""
        extend_overwrite = format_to_extend(overwrite)
        if path:
            return self._eval_on_object(
                f'exportAsMotionGraphicsTemplate({extend_overwrite},"{path}")'
            )
        else:
            return self._eval_on_object(
                f"exportAsMotionGraphicsTemplate({extend_overwrite})"
            )

    def get_motion_graphics_template_controller_name(self, index: int) -> str:
        """Gets the name of a single property in the Essential Graphics panel."""
        index += 1
        return self._eval_on_object(f"getMotionGraphicsTemplateControllerName({index})")

    def set_get_motion_graphics_controller_name(self, index: int, name: str) -> str:
        """Sets the name of a single property in the Essential Graphics panel."""
        index += 1
        return self._eval_on_object(
            f'getMotionGraphicsTemplateControllerName({index}, "{name}")'
        )

    def layer(self, layer, relative_index=None):
        """Returns a Layer object, which can be specified by name, an index position in this layer,
        or an index position relative to another layer."""
        if relative_index:
            layer = format_to_extend(layer)
            kwargs = self._eval_on_object(f"layer({layer}, {relative_index})")
            if not kwargs.get("pydobe_id"):
                raise ValueError("The value for the relative index is out of range")
        else:
            if isinstance(layer, str):
                kwargs = self._eval_on_object(f'layer("{layer}")')
            else:
                layer += 1
                kwargs = self._eval_on_object(f"layer({layer})")
        object_type = kwargs["object_type"]
        layer = create_python_object(object_type)(**kwargs)
        return layer

    def open_in_essential_graphics(self):
        """Opens the composition in the Essential Graphics panel."""
        self._eval_on_object("openInEssentialGraphics()")

    def open_in_viewer(self):
        """Opens the comp in a panel, moves it to the front and gives it focus"""
        kwargs = self._eval_on_object("openInViewer()")
        return Viewer(**kwargs) if kwargs else None


class FolderItem(Item):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """All of the items in the folder"""

    @property
    def items(self) -> ItemCollection:
        kwargs = self._eval_on_object("items")
        return ItemCollection(**kwargs) if kwargs else None

    """The number of items within the folder"""

    @property
    def num_items(self) -> int:
        return self._eval_on_object("numItems")

    # CUSTOM PROPERTIES

    """The composition items found in the folder"""

    @property
    def compositions(self) -> list:
        composition_items = []
        for item in self.items:
            if item.object_type == "CompItem":
                composition_items.append(item)
        return composition_items

    """The footage items found in the folder"""

    @property
    def footages(self) -> list:
        footage_items = []
        for item in self.items:
            if item.object_type == "FootageItem":
                footage_items.append(item)
        return footage_items

    """The folder items found in the folder"""

    @property
    def folders(self) -> list:
        folder_items = []
        for item in self.items:
            if item.object_type == "FolderItem":
                folder_items.append(item)
        return folder_items

    # FUNCTIONS

    def item(self, sub_index: int) -> Item:
        """Returns the top-level item in this folder at the specified index position."""
        sub_index += 1
        kwargs = self._eval_on_object(f"item({sub_index})")
        object_type = kwargs["object_type"]
        item = create_python_object(object_type)(**kwargs)
        return item


class FootageItem(AVItem):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type)

    # PROPERTIES

    """The footage source, an object that contains all of the settings related to that footage item, 
    including those that are normally accessed through the Interpret Footage dialog box"""

    @property
    def main_source(self) -> FootageSource:
        kwargs = self._eval_on_object("mainSource")
        object_type = kwargs["object_type"]
        return create_python_object(object_type)(**kwargs) if kwargs else None

    """The file object associated with this footage"""

    @property
    def file(self) -> File:
        kwargs = self._eval_on_object("file")
        return File(**kwargs) if kwargs else None

    # OVERRIDES

    @AVItem.duration.setter
    def duration(self, value: float):
        raise AttributeError(
            f"Can not change duration of {self.name} as it is not a Comp Item"
        )

    @AVItem.frame_duration.setter
    def frame_duration(self, value: float):
        raise AttributeError(
            f"Can not set frame duration on a footage Item. Instead set the conform frame"
            f" rate on the main source or proxy source of the item"
        )

    @AVItem.frame_rate.setter
    def frame_rate(self, value: float):
        raise AttributeError(
            "Can not set frame rate on a footage item. Instead set the conform frame rate"
        )

    @AVItem.height.setter
    def height(self, value: int):
        if self.main_source.object_type == "SolidSource":
            self._eval_on_object(f"height = {value}")
        else:
            raise AttributeError(
                "Attribute 'height' cannot be set, as the item is neither a comp, nor a solid"
            )

    @AVItem.width.setter
    def width(self, value: int):
        if self.main_source.object_type == "SolidSource":
            self._eval_on_object(f"width = {value}")
        else:
            raise AttributeError(
                "Attribute 'width' cannot be set, as the item is neither a comp, nor a solid"
            )

    # FUNCTIONS

    def replace(self, path: str):
        """Changes the source of this Footage Item to the specified file"""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        self._eval_on_object(f"replace({extend_file_object})")

    def replace_with_placeholder(
            self,
            name: str,
            width: int,
            height: int,
            frame_rate: float,
            duration: float,
            duration_in_current_format=True,
    ):
        """Changes the source of this FootageItem to the specified placeholder"""
        if duration_in_current_format:
            duration = current_format_to_time(duration, frame_rate)
        self._eval_on_object(
            f'replaceWithPlaceholder("{name}", {width}, {height}, {frame_rate}, {duration})'
        )

    def replace_with_sequence(self, path: str, force_alphabetical: bool = False):
        """Changes the source of this Footage Item to the specified image sequence."""
        file = File(**eval_script_returning_object(f'File("{path}")'))
        extend_file_object = format_to_extend(file)
        force_alphabetical = format_to_extend(force_alphabetical)
        self._eval_on_object(
            f"replaceWithSequence({extend_file_object}, {force_alphabetical})"
        )

    def replace_with_solid(
            self, color: list, name: str, width: int, height: int, pixel_aspect: float
    ):
        """Changes the source of this FootageItem to the specified solid"""
        self._eval_on_object(
            f'replaceWithSolid({color},"{name}", {width}, {height}, {pixel_aspect})'
        )


class ItemCollection(PydobeBaseCollection):
    def __init__(self, pydobe_id=None, object_type=None):
        super().__init__(pydobe_id, object_type, "length")

    def __getitem__(self, index: int):
        index = index + 1
        kwargs = super(ItemCollection, self).__getitem__(index)
        object_type = kwargs["object_type"]
        item = create_python_object(object_type)(**kwargs)
        return item

    # FUNCTIONS

    def add_comp(
            self,
            name: str,
            width: int,
            height: int,
            aspect_ratio: float,
            duration: float or str,
            frame_rate: float,
            duration_in_current_format=True,
    ) -> CompItem:
        """Add a new Composition to the project"""
        if duration_in_current_format:
            duration = current_format_to_time(duration, frame_rate)
        kwargs = self._eval_on_object(
            f'addComp("{name}", {width}, {height}, {aspect_ratio}, {duration}, {frame_rate})'
        )
        return CompItem(**kwargs) if kwargs else None

    def add_folder(self, name: str) -> FolderItem:
        """Add a new Folder to the project"""
        kwargs = self._eval_on_object(f'addFolder("{name}")')
        return FolderItem(**kwargs) if kwargs else None
