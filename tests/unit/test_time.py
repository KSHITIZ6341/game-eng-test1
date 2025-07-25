# tests/unit/test_time.py
from engine.core.time import Clock

def test_clock_tick():
    clk = Clock(target_fps=30)
    clk.tick()
    assert 0 < clk.dt < 1

# tests/unit/test_ecs.py
from dataclasses import dataclass
from engine.core.ecs import World

@dataclass(slots=True)
class Health:
    hp: int = 100

def test_add_and_query_component():
    w = World()
    e = w.create()
    w.add(e, Health())
    result = list(w.query(Health))
    assert result and result[0][0].id == e.id
