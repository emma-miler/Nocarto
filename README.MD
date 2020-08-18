## Nocarto

Nocarto is a desktop mind mapping application where the user is in control of the map. Unlike traditional mind mapping software, Nocarto treats all nodes as equal, allowing for arbitrary connections between any two nodes. 

Nocarto is written in Python using the PyQt framework.

## Features

* Human readable file format (JSON)
* Import functionality for existing mindmap formats (Currently only FreeMind (.mm))
* Easy to learn keyboard shortcuts
* Very lightweight and fast operation and editing

## In-development/planned features
* Undo/redo stack
* Export to PNG
* Support for more existing formats
* Grid snapping
* Zooming and moveable UI

## License

Nocarto's source code is licensed under GNU GPLv3. 
See COPYING for the complete license text.

All image files, except where otherwise noted, are licensed under
CC BY-SA 3.0: http://creativecommons.org/licenses/by-sa/3.0/

## Installation

Nocarto currently does not have any binary builds. 
To get started, clone the repository:

`git clone  https://github.com/NoaMiler/Nocarto.git`

from there, enter the newly created directory and install the required packages:

`cd Nocarto`

`pip install -r requirements.txt`

then simply run the application:

`python main.py`