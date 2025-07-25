from __future__ import annotations
import pyrr

class Camera:
    def __init__(self) -> None:
        self.position = pyrr.Vector3([0.0, 0.0, 3.0])
        self.target   = pyrr.Vector3([0.0, 0.0, 0.0])
        self.up       = pyrr.Vector3([0.0, 1.0, 0.0])
        self.aspect   = 16 / 9
        self.fov_y    = 45.0
        self.near     = 0.1
        self.far      = 100.0

    def view_matrix(self) -> pyrr.Matrix44:
        return pyrr.matrix44.create_look_at(self.position, self.target, self.up)

    def proj_matrix(self) -> pyrr.Matrix44:
        return pyrr.matrix44.create_perspective_projection_matrix(
            self.fov_y, self.aspect, self.near, self.far
        )
