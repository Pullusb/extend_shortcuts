# SPDX-License-Identifier: GPL-3.0-or-later

# Add X shortcut in weight paint mode to swap weight value between 0 and 1
# Add Shit + X shortcut in weight paint mode to swap paint brush blend Mix 0 with blend Add 0.02

import bpy

from bpy.types import Operator
from . preferences import get_addon_prefs

class OBJECT_OT_swap_paint_value(Operator):
    bl_idname = "object.swap_paint_value"
    bl_label = "Swap Paint Value"
    bl_description = "Swap the paint value"
    bl_options = {"REGISTER"} # , "UNDO"

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'PAINT_WEIGHT'

    def execute(self, context):
        scn_tools = context.scene.tool_settings
        ## Swap Wight between 0.0 and 1.0

        if bpy.app.version >= (5,0,0):
            # now not global but under the weight paint
            unified_paint_settings = scn_tools.weight_paint.unified_paint_settings
        else:
            unified_paint_settings = scn_tools.unified_paint_settings


        if unified_paint_settings.use_unified_weight:
            paint_settings = unified_paint_settings
        else:
            paint_settings = context.tool_settings.weight_paint.brush
            if not paint_settings:
                return {'CANCELLED'}

        if paint_settings.weight < 1:
            paint_settings.weight = 1.0
        else:
            paint_settings.weight = 0.0

        return {"FINISHED"}

class OBJECT_OT_swap_brush_with_value(Operator):
    bl_idname = "object.swap_brush_with_value"
    bl_label = "Swap Brush With Value"
    bl_description = "Swap Weight paint brush with custom values"
    bl_options = {"REGISTER"} # , "UNDO"

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'PAINT_WEIGHT'

    def execute(self, context):
        prefs = get_addon_prefs()
        scn_tools = context.scene.tool_settings

        brush = context.tool_settings.weight_paint.brush
        if not brush:
            return {'CANCELLED'}
        
        ## Disable unified paint settings
        if bpy.app.version >= (5,0,0):
            unified_paint_settings = scn_tools.weight_paint.unified_paint_settings

            ## Activate brush from library
            try:
                bpy.ops.brush.asset_activate(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="brushes\\essentials_brushes-mesh_weight.blend\\Brush\\Paint")
            except:
                pass

            brush = bpy.data.brushes.get('Paint')
            if not brush:
                self.report({'WARNING'}, 'Cannot find brush named Paint, try to active it first manually')
                return {'CANCELLED'}
            if brush.blend == 'ADD':
                brush.blend = 'MIX'
                brush.weight = prefs.mix_brush_value # 0.0
            else:
                brush.blend = 'ADD'
                brush.weight = prefs.add_brush_value # 0.02
            self.report({'INFO'}, f'Blend {brush.blend} {round(brush.weight, 2)}')

        else:
            unified_paint_settings = scn_tools.unified_paint_settings
            if brush.name == 'Add':
                brush = bpy.data.brushes.get('Mix')
                if not brush:
                    return {'CANCELLED'}
                
                brush.weight = prefs.mix_brush_value # 0.0
            else:
                brush = bpy.data.brushes.get('Add')
                if not brush:
                    return {'CANCELLED'}
                brush.weight = prefs.add_brush_value # 0.02

            context.tool_settings.weight_paint.brush = brush
        
        # disable unified paint settings and assign brush
        unified_paint_settings.use_unified_weight = False

        return {"FINISHED"}


## region KEYMAP

addon_keymaps = []

def register_keymap():
    addon = bpy.context.window_manager.keyconfigs.addon
    
    km = addon.keymaps.new(name="Weight Paint", space_type="EMPTY")
    
    # X
    kmi = km.keymap_items.new('object.swap_paint_value', type='X', value='PRESS')
    addon_keymaps.append((km, kmi))
    
    # Shift + X
    kmi = km.keymap_items.new('object.swap_brush_with_value', type='X', value='PRESS', shift=True)
    addon_keymaps.append((km, kmi))

def unregister_keymap():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    
    addon_keymaps.clear()


## region REGISTER

classes = (
    OBJECT_OT_swap_paint_value,
    OBJECT_OT_swap_brush_with_value,
        )

def register():
    if bpy.app.background:
        return
    for cls in classes:
        bpy.utils.register_class(cls)
    
    register_keymap()

def unregister():
    if bpy.app.background:
        return
    unregister_keymap()
    
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
