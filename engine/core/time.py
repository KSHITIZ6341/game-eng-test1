from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Final


@dataclass(slots=True)
class Clock:
    target_fps: int = 60
    _last_tick: float = time.monotonic()
    dt: float = 0.0         # Seconds between frames
    frame: int = 0

    _SEC_PER_NS: Final[float] = 1.0

    def tick(self) -> None:
        """Update delta‑time, enforce target FPS, and increment frame counter."""
        now = time.monotonic()
        self.dt = now - self._last_tick
        sleep_needed = max(0.0, (1 / self.target_fps) - self.dt)
        if sleep_needed:
            time.sleep(sleep_needed)
            now = time.monotonic()
            self.dt = now - self._last_tick
        self._last_tick = now
        self.frame += 1

    @property
    def fps(self) -> float:
        """Actual frames‑per‑second based on last tick."""
        return 1 / self.dt if self.dt else float("inf")