from abc import ABC, abstractmethod
from typing import TypeVar
from dataclasses import dataclass

from sqlalchemy import Select

TEntity = TypeVar("TEntity")

@dataclass
class Page[TEntity]:
    results: list[TEntity]
    total: int

class PaginatorPort(ABC):
    @abstractmethod
    async def paginate(self, query: Select, offset: int = 0, limit: int = 10) -> Page: ...
