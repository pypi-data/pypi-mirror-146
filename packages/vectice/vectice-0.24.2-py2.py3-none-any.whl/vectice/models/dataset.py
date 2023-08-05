from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Dataset:
    name: str
    project: Optional[str] = None
    description: Optional[str] = None

    def with_description(self, description: str):
        """ """
        self.description = description
        return self
