
import aiomysql
from aioredis import Redis


class MysqlAsyncContextManager:
    __slots__ = ('_pool', '_commands_partial', '_sa_conn')

    def __init__(self, pool_or_conn, commands_partial):
        self._pool = self._sa_conn = None
        if not isinstance(pool_or_conn, aiomysql.Pool):
            self._sa_conn = pool_or_conn
        else:
            self._pool = pool_or_conn

        self._commands_partial = commands_partial

    async def __aenter__(self):
        if self._sa_conn is not None:
            return self._sa_conn
        conn = await self._pool.acquire()
        pool_name = getattr(self._pool, 'pool_name')
        self._sa_conn = self._commands_partial(conn, pool_name)
        return self._sa_conn

    async def __aexit__(self, exc_type, exc_value, tb):
        if self._pool is None:
            return
        await self._sa_conn.close()
        self._pool = None
        self._sa_conn = None


class RedisAsyncContextManager:
    __slots__ = ('_pool', '_sa_conn', '_commands_partial', 'conn')

    def __init__(self, pool_or_conn, commands_partial):
        self._sa_conn = self._pool = None

        if isinstance(pool_or_conn, Redis):
            self._sa_conn = pool_or_conn
        else:
            self._pool = pool_or_conn
        self._commands_partial = commands_partial

    async def __aenter__(self):
        if not self._sa_conn:
            conn = await self._pool.acquire()
            pool_name = getattr(self._pool, 'pool_name')
            self._sa_conn = self._commands_partial(conn, pool_name)

        return self._sa_conn

    async def __aexit__(self, exc_type, exc_value, tb):
        if self._pool is None:
            return
        self._sa_conn.close()

        await self._sa_conn.wait_closed()
        try:
            self._pool.release(self._sa_conn._pool_or_conn)
        finally:
            self._pool = None
            self._sa_conn = None


