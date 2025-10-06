from psycopg.connection_async import AsyncConnection
from typing import Any, Iterable, Mapping, Protocol, Sequence, TypeAlias


Params: TypeAlias = Sequence[Any] | Mapping[str, Any]

class DatabaseConnection(Protocol):
    async def execute(self, query: str, params: Params) -> Any: ...
    async def execute_many(self, query: str, params: Iterable[Params]) -> None: ...

class PostgresDBConnection(DatabaseConnection):
    def __init__(self, conn_str: str) -> None:
        self._conn_str = conn_str

    async def execute(self, query: str, params: Params) -> Any:
        async with await AsyncConnection.connect(self._conn_str) as conn:
            async with conn.cursor() as cur:
                value = await cur.execute(query, params)
        return value

    async def execute_many(self, query: str, params: Iterable[Params]) -> None:
        async with await AsyncConnection.connect(self._conn_str) as conn:
            async with conn.cursor() as cur:
                await cur.executemany(query, params)

