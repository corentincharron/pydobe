# Pydobe

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg?style=flat-square)](https://www.python.org/)
[![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black.svg?style=flat-square)](https://github.com/psf/black)
[![SemVer](https://img.shields.io/badge/semver-2.0.0-blueviolet?style=flat-square)](https://semver.org/)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/LisaGG89/pydobe/main?style=flat-square)

A Python wrapper allowing developers to communicate with adobe applications

This package is based upon Pymiere - created by Quentin Masingarbe (https://github.com/qmasingarbe/pymiere)

# Installation

Windows: 

``
pip install pydobe
``

## After Effects

Copy the directory `pydobe_panel` from `pydobe/integrations/after_effects` to your CEP directory:
- User (no elevated permission needed): `%userprofile%\AppData\Roaming\Adobe\CEP\extensions`
- System: `C:\Program Files\Common Files\Adobe\CEP\extensions`

Enable "**Allow Scripts to Write Files and Access Network**" in your "_Scripting & Expressions_" preferences.

# Use cases and examples

Snippets and examples for potential uses within After Effects

### Working with projects

```python
# Retrieve project object
project = pydobe.objects.app.project

# Set project settings
project.bits_per_channel = 8
project.working_space = "ACEScg ACES Working Space AMPAS S-2014-004"
project.time_display_type = "Frames"
project.frames_use_feet_frames = False
project.frames_count_type = "Start at 0"

```


```python
app = pydobe.objects.app

# Open a Project
project_path = "path/to/my/project.aep"
app.open(project_path)

# Get path of current project
current_project = app.project.file
print(current_project)

# Save a Project
app.project.save()

# Save a Project to a new path
new_path = "path/to/my/new/project.aep"
app.project.save(new_path)

# Make some changes to your project

# Check if scene has been modified
print(app.project.dirty)

# # Close a Project
app.project.close()  # This will display a user prompt
# app.project.close(save=True)  # This will save before opening a new project
# app.project.close(save=False)  # This will not save before opening a new project


# Create a new Project
app.new_project()  # This will display a user prompt
# app.new_project(save=True)  # This will save before opening a new project
# app.new_project(save=False)  # This will not save before opening a new project

```

### Working with items

```python
project = pydobe.objects.app.project

# Check how many items are in the project
print(project.num_items)

# Get the names of all the items in the project
for item in project.items:
    print(item.name)
    # check which items are selected
    if item.selected:
        print(f'{item.name} is selected')

# Get the active item
my_item = project.active_item  # This attribute requires precisely 1 item to be selected

# Find out what type of item it is
print(my_item.type_name)

# Find the parent folder of the item
print(my_item.parent_folder)

# Get the names of all the compositions
for comp in project.compositions:
    print(comp.name)

# Get item by name
footage_folder = project.item_by_name("My Footage")

# Remove items from the scene:
for child in footage_folder.items:
    child.remove()
    
```

### Adding items to a project

```python
project = pydobe.objects.app.project

# Create some folders
# Add a comment and set a label colour
footage_folder = project.items.add_folder("Footage")
footage_folder.comment = "This is where we keep our footage"
footage_folder.label = "Fuchsia"

comps_folder = project.items.add_folder("Compositions")
comps_folder.comment = "This is where we keep our comps"
comps_folder.label = "Blue"

# Create a composition
my_comp = project.items.add_comp("My New Comp", 1920, 1080, 1, 100, 25)
my_comp.parent_folder = comps_folder
# duration is set using frames, to set duration using seconds
# ("My New Comp", 1920, 1080, 1, 4, 25, duration_as_frames=False)

# Add some footage
list_of_paths = [
    "path/to/my/file_01_v001_0000.png",
    "path/to/my/file_02_v001_0000.png",
    "path/to/my/file_03_v001_0000.png",
]

for path in list_of_paths:
    footage = project.import_file(path)
    # Set the frame rate
    footage.main_source.conform_frame_rate = 24
    # Set the parent
    footage.parent_folder = footage_folder

# Replace the footage with a new version
list_of_replacement_paths = [
    "path/to/my/file_01_v002_0000.png",
    "path/to/my/file_02_v002_0000.png",
    "path/to/my/file_03_v002_0000.png",
]

for footage in footage_folder.items:
    for new_path in list_of_replacement_paths:
        file_name = new_path.split("/")[-1]
        unique_file = file_name.rsplit("_", 2)[0]
        unique_footage = footage.name.rsplit("_", 2)[0]
        if unique_file == unique_footage:
            footage.replace(new_path)

```

Working with Layers
```python
project = pydobe.objects.app.project

# Create a new composition

my_comp = project.item_by_name("My Comp")
footage_folder = project.item_by_name("My Footage")

# Check the settings of the composition

print(my_comp.width)
print(my_comp.height)
print(my_comp.duration)
print(my_comp.bg_colour)

# Adjust the settings of the composition

my_comp.width = 1920
my_comp.height = 1080
my_comp.duration = 50
my_comp.bg_colour = [0.1, 0.7, 0.8]

# Create a new layer within your composition using your footage
for footage in footage_folder.items:
    my_comp.layers.add(footage)

# Check which compositions your footage is used in
for footage in footage_folder.items:
    print(footage.used_in)

# Check number of layers in the composition
print(my_comp.num_layers)

# Set the work area duration in your comp

my_comp.work_area_start = 0
my_comp.work_area_duration = 2

# Hide the shy layers in your composition

my_comp.hide_shy_layers = True

# Check if motion Blur is turned on
print(my_comp.motion_blur)


```
# Thanks

Thank you to Quentin Masingarbe for his Pymiere repository, as well as sharing his knowledge with me.

Thank you to Corentin Charron for constant mentoring.

# License

This project is licensed under the MIT License. See the LICENSE file for details. Copy it, steal it, modify it, share it!

# Contact

For support, questions, or interest, please contact me at lisa.gg89@gmail.com