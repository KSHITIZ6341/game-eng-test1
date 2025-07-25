from dataclasses import dataclass

from engine.core.ecs import World


@dataclass(slots=True)
class Health:
    hp: int = 100


def test_add_and_query_component() -> None:
    world = World()
    ent = world.create()
    world.add(ent, Health())
    rows = list(world.query(Health))
    assert len(rows) == 1
    e, comp = rows[0]
    assert e.id == ent.id
    assert comp.hp == 100


def test_system_decorator() -> None:
    world = World()
    ent = world.create()

    @dataclass(slots=True)
    class Tag:
        pass

    world.add(ent, Health(50))
    world.add(ent, Tag())

    @world.system
    def heal(e, h: Health, t: Tag, *, dt: float) -> None:  # type: ignore[valid-type]
        h.hp += 10

    world.step(0.016)
    assert world.get(ent, Health).hp == 60
