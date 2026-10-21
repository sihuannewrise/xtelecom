from __future__ import annotations

from typing import Protocol

from .schemas import ChargesFile


class ChargesParser(Protocol):
    """Любой парсер обязан вернуть ChargesFile."""

    def parse(self, content: bytes) -> ChargesFile: ...
