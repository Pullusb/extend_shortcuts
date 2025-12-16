# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.props import FloatProperty

def get_addon_prefs():
    return bpy.context.preferences.addons[__package__].preferences

class extend_shortcut_Prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    add_brush_value : FloatProperty(name='Add Brush Value', default=0.02,
                          description='value set when swapping to Add brush')
    
    mix_brush_value : FloatProperty(name='Mix Brush Value', default=0.0,
                          description='value set when swapping to Mix brush')

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.label(text='X : Swap brush weight value between 0 and 1')

        layout.separator()
        layout.label(text='Shift + X : Swap brush between Mix and Add (Disable unified weight)')
        box = layout.box()
        box.label(text='Swap Value When swapping')
        box.prop(self, "add_brush_value")
        box.prop(self, "mix_brush_value")


classes=(
extend_shortcut_Prefs,
)

def register(): 
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)