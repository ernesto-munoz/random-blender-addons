import math

import bpy
import blf
import bgl
import gpu
from gpu_extras.batch import batch_for_shader




class EM_OT_bounding_box_operator(bpy.types.Operator):
    bl_idname = "em.bounding_box_operator"
    bl_label = "Activate Bounding Box"
    bl_description = "See the bounding box of the selected object"
    bl_options = {"REGISTER"}

    def __init__(self):  # TODO: NO SE SI ESTO ES CORRECTO
        self._draw_handle = None
        self._shader = gpu.shader.from_builtin("3D_UNIFORM_COLOR")
        self._bounding_box_vertices = []
        self._bounding_box_edges = []


    def invoke(self, context, event):
        args = (self, context)

        if context.window_manager.EM_BBO_STARTED is False:
            context.window_manager.EM_BBO_STARTED = True

            self._draw_handle = bpy.types.SpaceView3D.draw_handler_add(
                self.draw_callback_view,
                args,
                "WINDOW",
                "POST_VIEW"  # POST_PIXEL for 2D operations
            )

            # mandatory before returning RUNNING_MODAL
            context.window_manager.modal_handler_add(self)
            return {"RUNNING_MODAL"}
        else:
            context.window_manager.EM_BBO_STARTED = False
            return {"CANCELLED"}

    def modal(self, context, event):

        if context.area:
            # TODO: NO SE EXACTAMENTE QUE ES CONTEXT.AREA
            context.area.tag_redraw()

            if not context.window_manager.EM_BBO_STARTED:
                bpy.types.SpaceView3D.draw_handler_remove(
                    self._draw_handle, "WINDOW"
                )
                self._draw_handle = None

                return {"CANCELLED"}

            return {"PASS_THROUGH"}

    def draw_callback_view(self, op, context):
        selected_objects = bpy.context.selected_objects

        min_x, min_y, min_z = math.inf, math.inf, math.inf
        max_x, max_y, max_z = -math.inf, -math.inf, -math.inf

        for each_selected_object in selected_objects:
            for each_vertex in each_selected_object.data.vertices:
                each_vertex_world_position = each_selected_object.matrix_world @ each_vertex.co
                if each_vertex_world_position[0] < min_x:
                    min_x = each_vertex_world_position[0]
                if each_vertex_world_position[0] > max_x:
                    max_x = each_vertex_world_position[0]

                if each_vertex_world_position[1] < min_y:
                    min_y = each_vertex_world_position[1]
                if each_vertex_world_position[1] > max_y:
                    max_y = each_vertex_world_position[1]
                    
                if each_vertex_world_position[2] < min_z:
                    min_z = each_vertex_world_position[2]
                if each_vertex_world_position[2] > max_z:
                    max_z = each_vertex_world_position[2]

        self._bounding_box_vertices = (
            (min_x, min_y, min_z),
            (min_x, max_y, min_z),
            (max_x, max_y, min_z),
            (max_x, min_y, min_z),

            (min_x, min_y, max_z),
            (min_x, max_y, max_z),
            (max_x, max_y, max_z),
            (max_x, min_y, max_z),
        )

        self._bounding_box_edges = (
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )

        self._batch = batch_for_shader(self._shader, "LINES", {"pos": self._bounding_box_vertices},
                                       indices=self._bounding_box_edges)
        self._shader.bind()
        # self._shader.uniform_float("color", (0.48, 0.78, 0.91, 0.7))
        self._shader.uniform_float("color", (1.0, 0.0, 0.0, 0.7))
        bgl.glLineWidth(2)
        self._batch.draw(self._shader)
        bgl.glLineWidth(1)

