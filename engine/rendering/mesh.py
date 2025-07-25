"""Static cube mesh (positions only)."""
from __future__ import annotations
import array
from dataclasses import dataclass
import wgpu

_POS = [
    (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5),
    (0.5,  0.5, -0.5), (-0.5,  0.5, -0.5),
    (-0.5, -0.5,  0.5), (0.5, -0.5,  0.5),
    (0.5,  0.5,  0.5), (-0.5,  0.5,  0.5),
]
_IND = [
    0, 1, 2, 2, 3, 0,   4, 5, 6, 6, 7, 4,
    0, 4, 7, 7, 3, 0,   1, 5, 6, 6, 2, 1,
    3, 2, 6, 6, 7, 3,   0, 1, 5, 5, 4, 0,
]

@dataclass(slots=True)
class Mesh:
    vbo: wgpu.GPUBuffer
    ibo: wgpu.GPUBuffer
    index_count: int

    @classmethod
    def cube(cls, device: wgpu.GPUDevice) -> "Mesh":
        flat = array.array("f", sum(_POS, ()))
        vbo = device.create_buffer_with_data(data=flat, usage=wgpu.BufferUsage.VERTEX)
        ibo = device.create_buffer_with_data(data=array.array("I", _IND), usage=wgpu.BufferUsage.INDEX)
        return cls(vbo, ibo, len(_IND))
