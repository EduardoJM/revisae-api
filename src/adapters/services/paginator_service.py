from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select, select, func

from application.interfaces.paginator_port import PaginatorPort, Page

class PaginatorService(PaginatorPort):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def paginate(self, query: Select, offset: int = 0, limit: int = 10):
        if offset < 0:
            raise AttributeError("offset should be > 0")
        if limit <= 0:
            raise AttributeError("limit should >= 1")
        
        items = query.limit(limit).offset(offset)
        results = await self._session.execute(items)

        count = await self._session.scalar(select(func.count()).select_from(query.froms[0]))
        return Page(
            results=[entity for entity, *_ in results],
            total=count,
            per_page=limit
        )
