struct Uniforms {
    mvp: mat4x4<f32>,
};

@group(0) @binding(0)
var<uniform> U: Uniforms;

struct VSIn  { @location(0) pos: vec3<f32>, };
struct VSOut { @builtin(position) pos: vec4<f32>, };

@vertex
fn main(v: VSIn) -> VSOut {
    var o: VSOut;
    o.pos = U.mvp * vec4<f32>(v.pos, 1.0);
    return o;
}
