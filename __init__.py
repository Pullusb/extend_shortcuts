# SPDX-License-Identifier: GPL-3.0-or-later

bl_info = {
    "name": "Extend Shortcuts",
    "description": "Additional keymap entry for practical use",
    "author": "Samuel Bernou",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object"
}

import bpy

from . import swap_paint_value
from . import preferences

mods = (
    preferences,
    swap_paint_value,
        )

def register():
    for mod in mods:
        mod.register()

def unregister():
    for mod in reversed(mods):
        mod.unregister()

if __name__ == "__main__":
    register()
