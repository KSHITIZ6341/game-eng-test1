from __future__ import annotations

import inspect
from collections import defaultdict
from dataclasses import dataclass, is_dataclass
from typing import Any, Callable, Dict, Generator, List, Tuple, Type, TypeVar

T = TypeVar("T")


@dataclass(slots=True)
class Entity:
    id: int  # Unique identifier


class World:


    def __init__(self) -> None:
        self._next_id: int = 1
        self._components: Dict[Type, Dict[int, Any]] = defaultdict(dict)
        self._systems: List[Callable[[float], None]] = []

    # Entity -----------------------------------------------------------------
    def create(self) -> Entity:
        e = Entity(self._next_id)
        self._next_id += 1
        return e

    # Component --------------------------------------------------------------
    def add(self, entity: Entity, component: T) -> None:
        if not is_dataclass(component):
            raise TypeError("Components must be dataclass instances")
        self._components[type(component)][entity.id] = component

    def get(self, entity: Entity, comp_type: Type[T]) -> T | None:
        return self._components.get(comp_type, {}).get(entity.id)

    def remove(self, entity: Entity, comp_type: Type) -> None:
        self._components.get(comp_type, {}).pop(entity.id, None)

    # Query ------------------------------------------------------------------
    def query(self, *comp_types: Type) -> Generator[Tuple[Entity, ...], None, None]:
        if not comp_types:
            return
        ids = set.intersection(*(set(self._components[c].keys()) for c in comp_types))
        for eid in ids:
            yield (Entity(eid), *[self._components[c][eid] for c in comp_types])

    # Systems ----------------------------------------------------------------
    def system(self, fn: Callable[..., None]) -> Callable[..., None]:
        sig = inspect.signature(fn)
        comp_types = tuple(p.annotation for p in sig.parameters.values() if p.name != "dt")

        def wrapper(dt: float) -> None:
            for row in self.query(*comp_types):
                fn(*row, dt=dt)

        self._systems.append(wrapper)
        return fn

    def step(self, dt: float) -> None:
        for sys in self._systems:
            sys(dt)
