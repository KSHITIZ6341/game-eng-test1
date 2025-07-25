# Changelog
_All notable changes to **Reaper Engine** will be documented in this file._  
The project adheres to **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)** and **SemVer** (pre‑1.0 rules).

---

## [Unreleased]

### Added
- Data‑flow link design draft  
- Qt Graph Editor skeleton (`graph_view.py`)

### Changed
- **Rendering** – pipeline layout now ready for texture sampling  
- **Node Runtime** – prepared for topological sort execution

### Fixed
- Lifetime guard edge‑case when zero draw‑calls submitted  
- WGSL compliance with latest wgpu‑native validator

---

## [0.1.0‑alpha] – 2025‑07‑25

### Added
- **Core Runtime**
  - `Clock` with frame‑rate throttling  
  - `World (ECS)` registry + system decorator  
  - Structured JSON logger (`structlog`)
- **Rendering**
  - WGPU backend (`wgpu.py`), swap‑chain, clear‑pass  
  - SceneGraph (`scenegraph.py`) with hierarchical transforms  
  - Perspective `Camera` helper
  - Static cube `Mesh` generator
  - WGSL shader pair `basic.vert/frag.wgsl`
- **Resource Management**
  - Per‑frame lifeboat to retain GPU objects
- **Visual Scripting**
  - JSON schema v1 (`schema.py`)  
  - Compiler to Python AST (`compiler.py`)  
  - Hot‑reload runtime (`runtime.py`)  
  - `RotateY` node (spins entity on Y axis)
- **Assets**
  - Example graph `assets/graphs/spin.json`
- **Demo**
  - `run_demo_cube.py` → spinning red cube in a cornflower‑blue window

### Changed
- Renderer pipeline rebuilds after shader hot‑swap  
- Camera integrated into renderer frame pass

### Fixed
- GPU validation panic (“BindGroup does not exist”) via resource lifeboat  
- WGSL struct syntax updated to comma‑terminated fields  
- Positional arg errors converted to keyword calls for wgpu 0.16 API

### Removed
- Legacy ad‑hoc cube rotation code (superseded by RotateY node)

---

## [0.0.0] – 2025‑07‑24

### Added
- Repository scaffold (~360 modules & placeholders)  
- MIT‑based Community License (later superseded)  
- Unit tests for `Clock`, `ECS`, and logger

