

from __future__ import annotations

import array
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import glfw
import wgpu
import wgpu.backends.auto
import wgpu.gui.glfw as glfw_gui
import pyrr

_CLEAR: Tuple[float, float, float, float] = (0.392, 0.584, 0.929, 1.0)  # cornflower
@dataclass(slots=True)
class Swapchain:
    context: wgpu.gui.WgpuCanvasContext  # type: ignore[attr-defined]



class Renderer:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Reaper") -> None:
        self._canvas = glfw_gui.WgpuCanvas(title=title, size=(width, height))
        self._window = self._canvas._window
        self._adapter = wgpu.gpu.request_adapter(canvas=self._canvas, power_preference="high-performance")
        self._device = self._adapter.request_device()
        self._context = self._canvas.get_context()
        self._context.configure(
            device=self._device,
            format=wgpu.TextureFormat.bgra8unorm,
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

        self._swapchain = Swapchain(self._context)
        self._frame_refs: List[wgpu.GPUObjectBase] = []
        self._scene_root = None
        self._camera = None
        self._build_pipeline()

    def _build_pipeline(self) -> None:
        shader_dir = Path(__file__).parent.parent / "shaders"
        vs_mod = self._device.create_shader_module(code=(shader_dir / "basic.vert.wgsl").read_text())
        fs_mod = self._device.create_shader_module(code=(shader_dir / "basic.frag.wgsl").read_text())

        self._bind_layout = self._device.create_bind_group_layout(entries=[{
            "binding": 0,
            "visibility": wgpu.ShaderStage.VERTEX,
            "buffer": {"type": wgpu.BufferBindingType.uniform},
        }])
        layout = self._device.create_pipeline_layout(bind_group_layouts=[self._bind_layout])

        self._pipeline = self._device.create_render_pipeline(
            layout=layout,
            vertex={
                "module": vs_mod,
                "entry_point": "main",
                "buffers": [{
                    "array_stride": 12,
                    "attributes": [{"shader_location": 0, "format": wgpu.VertexFormat.float32x3, "offset": 0}],
                }],
            },
            primitive={"topology": wgpu.PrimitiveTopology.triangle_list},
            fragment={
                "module": fs_mod,
                "entry_point": "main",
                "targets": [{"format": wgpu.TextureFormat.bgra8unorm}],
            },
        )


    def set_scene(self, root) -> None:
        self._scene_root = root

    def set_camera(self, cam) -> None:
        self._camera = cam


    def _render_frame(self, view) -> None:
        enc = self._device.create_command_encoder()
        rpass = enc.begin_render_pass(color_attachments=[{
            "view": view,
            "clear_value": _CLEAR,
            "load_op": wgpu.LoadOp.clear,
            "store_op": wgpu.StoreOp.store,
        }])
        rpass.set_pipeline(self._pipeline)

        frame_refs: List[wgpu.GPUObjectBase] = []

        if self._scene_root and self._camera:
            from engine.rendering.mesh import Mesh  # local import to avoid cycle

            view_m = self._camera.view_matrix()
            proj_m = self._camera.proj_matrix()

            for node, model_m in self._scene_root.traverse():
                if getattr(node, "drawable", None) and isinstance(node.drawable, Mesh):
                    mesh = node.drawable

                    mvp = pyrr.matrix44.multiply(model_m, view_m)
                    mvp = pyrr.matrix44.multiply(mvp, proj_m)

                    ubuf = self._device.create_buffer_with_data(
                        data=array.array("f", mvp.flatten()),
                        usage=wgpu.BufferUsage.UNIFORM,
                    )
                    bind = self._device.create_bind_group(
                        layout=self._bind_layout,
                        entries=[{"binding": 0, "resource": {"buffer": ubuf, "offset": 0, "size": 64}}],
                    )
                    frame_refs += [ubuf, bind]

                    rpass.set_vertex_buffer(0, mesh.vbo, 0, 0)
                    rpass.set_index_buffer(mesh.ibo, wgpu.IndexFormat.uint32, 0, 0)
                    rpass.set_bind_group(0, bind)
                    rpass.draw_indexed(mesh.index_count, 1, 0, 0, 0)

        rpass.end()
        self._device.queue.submit([enc.finish()])
        self._frame_refs = frame_refs  # keep GPU objects alive until next frame


    def render_loop(self, tick_cb, step_cb) -> None:
        while not glfw.window_should_close(self._window):
            glfw.poll_events()
            tick_cb()
            step_cb()
            tex = self._context.get_current_texture()
            self._render_frame(tex.create_view())
            self._context.present()
        glfw.terminate()
