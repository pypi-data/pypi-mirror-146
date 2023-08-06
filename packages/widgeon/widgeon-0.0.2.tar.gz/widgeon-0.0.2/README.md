# __--DISCLAIMER-- the README below is deprecated. i am rebuilding the project from the ground up as the old project had bad architecture and was very slow.__
\
\
\
# dot-ui
An easy to use yet good-looking UI creation framework for Python

## Contents
* [Basics](#basics)
    * [Creating a window](#creating-a-window)
    * [Adding widgets](#adding-widgets)
    * [Changing renderer settings](#changing-renderer-settings)
    * [Adding Behaviours](#adding-behaviours)
    * [Taking inputs](#taking-inputs)

# Basics
## Creating a window
Opening a Window is as easy as creating a window object and calling open():
```python
from dot_ui import *

win = Window()

win.open()
```
![Opened Window](https://github.com/dots-git/dot-ui/blob/main/docs/assets/new_window.png?raw=true)

In the constructor you can specify the width, height, title, icon and whether the window should be opened in full screen mode.

## Adding widgets
Adding a widget is no more compicated. You create the widget and add it to the window. It takes an x and y position as well as a width and height as optional constructor parameters:
```python
from dot_ui import *

win = Window("Demo")

widget = Widget(10, 10)

win.add_widget(widget)

win.open()
```
![Window with widget](https://github.com/dots-git/dot-ui/blob/main/docs/assets/window_with_widget.png?raw=true)

## Changing renderer settings
Some window and widget properties are universal and are controlled by the renderer. You can customize these settings by calling the corresponding setter on the renderer (DotRenderer by default):
```python
from dot_ui import *

DotRenderer.set_corner_radius(0)
DotRenderer.set_shadow_offset(Vector2(-2, -2))
DotRenderer.set_shadow_radius(10)
DotRenderer.set_default_color(Color.GREEN)
DotRenderer.set_shadow_opacity(1)

win = Window(title="Demo")

widget = Widget(10, 10)

win.add_widget(widget)

win.open()
```
![Changed renderer settings](https://github.com/dots-git/dot-ui/blob/main/docs/assets/changed_renderer_settings.png?raw=true)

## Adding behaviours
You can add behaviours to widgets that consist of a function that is run on initialization and one that is run every tick. This is some example code that prints "Widget initialized" on initialization and prints the delta time every tick.

```python
from dot_ui import *

win = Window(title="Demo")

def print_init(self: Widget):
    print("Widget initialized")

def print_on_tick(self: Widget, delta):
    print(delta)

widget = Widget(10, 10)

widget.add_behaviour("Print", print_on_tick, print_init)

win.add_widget(widget)

win.open()
```

## Taking inputs
The Input class allows you to create actions that are triggered when one of multiple keys or key combinations is pressed. You can then check if these actions have been triggered. This code will print the delta time when "D" or "0" are pressed and close the widget when Crtl+Q is pressed.

```python
from dot_ui import *

Input.add_action("Print Delta", Key.D, 0)

Input.add_action(
    "Close", 
    KeyCombination(Key.L_CTRL, Key.Q)
)

win = Window(title="Demo")


def input_demo(self: Widget, delta):
    if Input.action_pressed("Print Delta"):
        print(delta)
    
    if Input.action_just_pressed("Close"):
        self.close()


widget = Widget(10, 10)

widget.add_behaviour("Input Demo", input_demo)

win.add_widget(widget)

win.open()
```
