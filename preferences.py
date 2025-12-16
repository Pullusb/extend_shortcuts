# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.props import (FloatProperty,
                        BoolProperty,
                        EnumProperty,
                        StringProperty,
                        IntProperty,
                        PointerProperty)

def get_addon_prefs():
    """Function to read current addon preferences properties
    access with : get_addon_prefs().super_special_option
    """
    # import os 
    # addon_name = os.path.splitext(__name__)[0]
    # preferences = bpy.context.preferences
    # return preferences.addons[addon_name].preferences
    return bpy.context.preferences.addons[__package__].preferences


class extend_shortcut_Prefs(bpy.types.AddonPreferences):
    bl_idname = __name__.split('.')[0] # or with: os.path.splitext(__name__)[0]

    # mode : StringProperty(name='Mode', default='',
    #                       description='Some text can change tools behaviors')
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


### --- REGISTER ---

classes=(
extend_shortcut_Prefs,
)

def register(): 
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)