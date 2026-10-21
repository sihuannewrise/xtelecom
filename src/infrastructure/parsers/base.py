from typing import Protocol

from .schemas import ChargesFile


class ChargesParser(Protocol):
    def parse(self, content: bytes) -> ChargesFile: ...
