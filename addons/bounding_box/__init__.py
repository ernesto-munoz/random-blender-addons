import bpy

from .bounding_box_operator import EM_OT_bounding_box_operator

bl_info = {
    "name" : "Bounding Box Operator",
    "author": "Ernesto <emunozfaba@gmail.com>",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "",
    "description": "Bounding Box Operator",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
}

def register():
    bpy.types.WindowManager.EM_BBO_STARTED = bpy.props.BoolProperty(default=False)
    bpy.utils.register_class(EM_OT_bounding_box_operator)

def unregister():
    bpy.utils.unregister_class(EM_OT_bounding_box_operator)