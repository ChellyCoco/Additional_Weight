import bpy
bl_info = {
    "name": "Additional Weight",
    "author": "ChellyCoco",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Additional Weight",
    "description": "Adds a set amount of weight to the currently active vertex group",
    "category": "Mesh",
}


class VertexGroupWeightModifierPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_vertex_group_weight_modifier"
    bl_label = "Additional Weight"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Additional Weight"

    def draw(self, context):
        layout = self.layout

        # Weight modification amount input field
        layout.label(text="Weight Modification Amount:")
        layout.prop(context.scene, "weight_amount")

        # Modify Weight button
        layout.operator("object.modify_vertex_group_weight",
                        text="Modify Weight")


class OBJECT_OT_ModifyVertexGroupWeightOperator(bpy.types.Operator):
    bl_idname = "object.modify_vertex_group_weight"
    bl_label = "Modify Weight"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        weight_amount = context.scene.weight_amount

        # Get the currently selected object
        obj = bpy.context.object
        if obj is None:
            self.report({'ERROR'}, "No object selected.")
            return {'CANCELLED'}

        # Check if the object is a mesh
        if obj.type != 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh.")
            return {'CANCELLED'}

        # Get the active vertex group
        vertex_group = obj.vertex_groups.active
        if vertex_group is None:
            self.report({'ERROR'}, "No active vertex group.")
            return {'CANCELLED'}

        mesh = obj.data

        # Modify weight for each vertex in the group
        for vertex in mesh.vertices:
            vertex_group_weight = vertex_group.weight(vertex.index)
            new_weight = vertex_group_weight + weight_amount
            # Clamp between 0 and 1
            new_weight = max(0.0, min(1.0, new_weight))
            vertex_group.add([vertex.index], new_weight, 'REPLACE')

        self.report(
            {'INFO'}, "Weight modified in the vertex group successfully.")
        return {'FINISHED'}


def register():
    bpy.types.Scene.weight_amount = bpy.props.FloatProperty(
        name="Weight Amount",
        default=0.1,
        step=0.01,
    )
    bpy.utils.register_class(VertexGroupWeightModifierPanel)
    bpy.utils.register_class(OBJECT_OT_ModifyVertexGroupWeightOperator)


def unregister():
    bpy.utils.unregister_class(VertexGroupWeightModifierPanel)
    bpy.utils.unregister_class(OBJECT_OT_ModifyVertexGroupWeightOperator)
    del bpy.types.Scene.weight_amount


if __name__ == "__main__":
    register()
