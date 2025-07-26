
from __future__ import annotations
from pathlib import Path
import pyrr

from engine.core.time import Clock
from engine.rendering.backend.wgpu import Renderer
from engine.rendering.scenegraph import Node, Transform
from engine.rendering.mesh import Mesh
from engine.rendering.camera import Camera
from engine.scripting.node.runtime import GraphRuntime
from engine.scripting.node.runtime_bridge import GraphRuntimeBridge

graph_path = Path(__file__).parent.parent / "assets/graphs/editing.json"
graph_rt = GraphRuntimeBridge(graph_path)

def step(dt):
    graph_rt.update(dt)                             # advance node graph
    speed = graph_rt.get("rotY1", "rotation")       # example access
    cube.transform.rotation_y = speed               # drive your entity

clock = Clock()
cam   = Camera(); cam.aspect = 1280 / 720
renderer = Renderer()
renderer.set_camera(cam)

root = Node("root")
cube = Node("cube", Transform())
root.add(cube)
cube.drawable = Mesh.cube(renderer._device)
renderer.set_scene(root)

graph = GraphRuntime(Path(__file__).parent.parent / "assets/graphs/editing.json")


def step() -> None:
    ctx = {"entity": cube, "dt": clock.dt}
    graph.step(ctx)

renderer.render_loop(clock.tick, step)
