# Reaper Engine — MVP Milestone Report

> **Status:** _Rendering & Visual‑Scripting core online_  
> **Tag:** `v0.1.0-alpha`

---

##  What’s Working

| Pillar | Deliverable | Result |
|--------|-------------|--------|
| **Core Runtime** | `Clock`, `World (ECS)`, structured logger | Deterministic heartbeat at ≥ 60 FPS |
| **Rendering** | WGPU swap‑chain, scene graph, camera (view × proj) | Red cube rendered with per‑frame resources guard |
| **Shader Pipeline** | WGSL vertex/fragment (`basic.*.wgsl`) | Compiles & draws on Metal backend |
| **Visual Scripting** | JSON schema v1, compiler, hot‑reload runtime | `RotateY` node drives cube spin; speed edits live |
| **Demo** | `run_demo_cube.py` | Launches window, shows spinning cube |

---


##  Project Directory Snapshot

```text
ReaperEngine/
├─ engine/
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ time.py
│  │  ├─ ecs.py
│  │  ├─ events.py
│  │  └─ utils/
│  │     └─ logger.py
│  ├─ rendering/
│  │  ├─ backend/
│  │  │  ├─ __init__.py
│  │  │  └─ wgpu.py
│  │  ├─ scenegraph.py
│  │  ├─ camera.py
│  │  ├─ mesh.py
│  │  └─ shaders/
│  │     ├─ basic.vert.wgsl
│  │     └─ basic.frag.wgsl
│  ├─ scripting/
│  │  └─ node/
│  │     ├─ base.py
│  │     ├─ schema.py
│  │     ├─ compiler.py
│  │     ├─ runtime.py
│  │     ├─ nodes/
│  │     │  └─ utility/
│  │     │     └─ rotate_y.py
│  │     └─ __init__.py
│  └─ __init__.py
├─ assets/
│  └─ graphs/
│     └─ spin.json
├─ scripts/
│  ├─ run_demo_cube.py
│  └─ __init__.py
├─ tests/                 # (unit tests to come)
├─ docs/                  # (MkDocs scaffold)
└─ README.md
