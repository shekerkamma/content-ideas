import bpy
bpy.ops.preferences.addon_enable(module="blender_mcp")
bpy.context.scene.blendermcp_auto_start_server = True
bpy.context.scene.blendermcp_port = 9876
print("Codex Blender bridge enabled on localhost:9876")
