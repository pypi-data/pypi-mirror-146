
import asyncio
import functools
import weakref
import aiomysql

from aiomysql.sa import SAConnection, Engine
from aiomysql.sa.engine import _dialect
from sqlalchemy.sql.selectable import Select
from sqlalchemy.sql.dml import Insert, Update, Delete
from wintersweet.asyncs.pool.base import BasePoolManager
from wintersweet.asyncs.pool.context import MysqlAsyncContextManager
from wintersweet.utils.base import Utils
from wintersweet.utils.metaclass import SafeSingleton


class MysqlClient:
    """MySQL客户端
    """
    def __init__(self, conn: SAConnection):
        self._conn = conn
        self._lock = asyncio.Lock()

    def __del__(self):
        if self._conn and not self._conn.closed:
            _conn, self._conn = self._conn, None
            Utils.asyncio.create_task(_conn.close)
            Utils.log.critical(f'Mysql:{self._conn} conn leakage!')

    @staticmethod
    def safestr(val):

        cls = type(val)

        if cls is str:
            val = aiomysql.escape_string(val)
        elif cls is dict:
            val = aiomysql.escape_dict(val, 'utf8')
        else:
            val = str(val)

        return val

    @property
    def conn(self):
        return self._conn

    @property
    def closed(self):
        return self._conn.closed

    def close(self):
        return self._conn.close()

    async def execute(self, query, *multiparams, **params):

        result = None

        async with self._lock:

            result = await self._conn.execute(query, *multiparams, **params)

        return result

    async def select(self, query, *multiparams, **params):

        result = []

        if not isinstance(query, Select):
            raise TypeError(r'Not sqlalchemy.sql.selectable.Select object')

        proxy = await self.execute(query, *multiparams, **params)

        if proxy is not None:

            records = await proxy.cursor.fetchall()

            if records:
                result = records

            if not proxy.closed:
                await proxy.close()

        return result

    async def find(self, query, *multiparams, **params):

        result = None

        if not isinstance(query, Select):
            raise TypeError(r'Not sqlalchemy.sql.selectable.Select object')

        proxy = await self.execute(query.limit(1), *multiparams, **params)

        if proxy is not None:

            record = await proxy.cursor.fetchone()

            if record:
                result = record

            if not proxy.closed:
                await proxy.close()

        return result

    async def count(self, query, *multiparams, **params):

        result = await self.find(query, *multiparams, **params)

        return result[r'tbl_row_count']

    async def insert(self, query, *multiparams, **params):

        result = 0

        if not isinstance(query, Insert):
            raise TypeError(r'Not sqlalchemy.sql.dml.Insert object')

        proxy = await self.execute(query, *multiparams, **params)

        if proxy is not None:

            result = self._conn.connection.insert_id

            if not proxy.closed:
                await proxy.close()

        return result

    async def update(self, query, *multiparams, **params):

        result = 0

        if not isinstance(query, Update):
            raise TypeError(r'Not sqlalchemy.sql.dml.Update object')

        proxy = await self.execute(query, *multiparams, **params)

        if proxy is not None:

            result = proxy.rowcount

            if not proxy.closed:
                await proxy.close()

        return result

    async def delete(self, query, *multiparams, **params):

        result = 0

        if not isinstance(query, Delete):
            raise TypeError(r'Not sqlalchemy.sql.dml.Delete object')

        proxy = await self.execute(query, *multiparams, **params)

        if proxy is not None:

            result = proxy.rowcount

            if not proxy.closed:
                await proxy.close()

        return result

    def begin(self):
        return self._conn.begin()


class MysqlPoolManager(SafeSingleton, BasePoolManager):
    """数据库连接池管理器"""

    def __init__(self):

        super(MysqlPoolManager, self).__init__(MysqlAsyncContextManager)
        self._engines = {}

    def __await__(self):
        if self._ready:
            return self

        for pool_name, pool_config in self._config.items():
            pool = yield from aiomysql.create_pool(**pool_config).__await__()
            self._pools[pool_name] = pool
            setattr(self._pools[pool_name], 'pool_name', pool_name)

            self._engines[pool_name] = Engine(_dialect, pool)
            Utils.log.success(
                f"mysql pool {self.pool_status(pool_name)} initialized"
            )
        self._ready = True

        return self

    def func_partial(self, conn, pool_name):
        client = MysqlClient(SAConnection(conn, self._engines[pool_name]))
        self._contexts[pool_name].set(weakref.ref(client))

        return client

    def pool_status(self, pool_name='default'):
        pool = self._pools[pool_name]
        user = self._config[pool_name].get('user', 'root')
        host = self._config[pool_name].get('host', 'localhost')
        db = self._config[pool_name].get('db', None)
        port = self._config[pool_name].get('port', 3306)

        return f'<[{pool_name}] {user}@{host}:{port} [db:{db}, size:[{pool.minsize}:{pool.maxsize}], free:{pool.freesize}]>'

    def _echo_pool_info(self, pool_name='default'):

        assert self._ready, f'{self.__class__.__name__} does not initialize'
        pool = self._pools[pool_name]
        if (pool.maxsize - pool.size + pool.freesize) < Utils.math.ceil(pool.maxsize / 3):
            Utils.log.warning(
                f'Mysql pool not enough ({pool_name}): {pool.freesize}({pool.size}/{pool.maxsize})'
             )

    async def find(self, sql: Select, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.find(sql, *args, **kwargs)

    async def select(self, sql: Select, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.select(sql, *args, **kwargs)

    async def count(self, sql, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.count(sql, *args, **kwargs)

    async def update(self, sql: Update, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.update(sql, *args, **kwargs)

    async def insert(self, sql, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.insert(sql, *args, **kwargs)

    async def delete(self, sql: Delete, *args, pool_name='default', **kwargs):

        async with self.get_client(pool_name) as client:
            return await client.delete(sql, *args, **kwargs)

    async def execute(self, query, *multiparams, pool_name='default', **params):

        async with self.get_client(pool_name) as client:
            return await client.execute(query, *multiparams, **params)

    def close(self):
        self._ready = False
        _pools, self._pools = self._pools, None
        for pool in _pools.values():
            pool.close()


mysql_pool_manager = MysqlPoolManager()


def atomic(pool_name='default'):

    def wrapper(func):
        @functools.wraps(func)
        async def callback(*args, **kwargs):
            global mysql_pool_manager
            if not mysql_pool_manager.ready:
                await mysql_pool_manager

            async with mysql_pool_manager.get_client(pool_name) as trx:
                async with trx.begin():
                    result = await func(*args, **kwargs)
                    return result
        return callback
    return wrapper

