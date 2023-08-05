
import traceback
import weakref
import aioredis

from aioredis import Redis, ConnectionsPool
from hagworm.extend.base import catch_error

from wintersweet.asyncs.pool.base import BasePoolManager
from wintersweet.asyncs.pool.context import RedisAsyncContextManager
from wintersweet.asyncs.task.tasks import IntervalTask
from wintersweet.asyncs.tools.circular import AsyncCircularForTimeout
from wintersweet.utils.base import Utils
from wintersweet.utils.metaclass import SafeSingleton


class MutexLock:
    """基于Redis实现的分布式锁，当await lock.acquire()一旦获取锁成功，会自动触发看门狗，持续对lock进行检查并保持持有
        直到跳出async with管理或者手动调用release()
        使用方法1（建议）：
            async with MutexLock(redis_pool, 'test-key', 60) as lock:
                is_locked = await lock.acquire()
                if is_locked:
                    # do something
                else:
                    # do something

        当你需要在程序生命周期内保持锁占有时，可使用方法2
        使用方法2：
            lock = MutexLock(redis_pool, 'test-key', 60)
            try:
                is_locked = await lock.acquire()
                if is_locked:
                    # do something
                else:
                    # do something
            except Exception as e:
                # do something
            finally:
                await lock.release()
    """

    _renew_script = '''
    if redis.call("get",KEYS[1]) == ARGV[1] and redis.call("ttl",KEYS[1]) > 0 then
        return redis.call("expire",KEYS[1],ARGV[2])
    else
        return 0
    end
    '''

    _unlock_script = '''
    if redis.call("get",KEYS[1]) == ARGV[1] then
        return redis.call("del",KEYS[1])
    else
        return 0
    end
    '''

    def __init__(self, redis_pool: ConnectionsPool, key, expire=60, commands_factory=Redis):

        self._redis_pool = redis_pool
        assert expire > 3, '"expire" is too small'
        self._expire = expire
        self._commands_factory = commands_factory
        self._key = key
        self._lock_tag = f'process_lock_{key}'
        self._lock_val = Utils.uuid.uuid1().encode()

        self._locked = False
        self._cache = None
        self._conn = None
        self._err_count = 0

        # watch dog
        self._watcher = None

    async def __aenter__(self):

        await self._init_conn()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):

        await self.release()

    def __del__(self):
        if self._watcher.running():
            self._watcher.stop()
            self._watcher = None

        if self._conn:
            self._redis_pool.release(self._conn)
            self._cache = self._conn = None
            self._redis_pool = None

    def __repr__(self):
        return f'{self.__class__.__name__}<{self._key}>'

    @property
    def locked(self):
        return self._locked

    async def _do_heartbeat(self):
        """watch dog continuous to refresh the lock"""
        res = await self.acquire(0)
        Utils.log.info(f'{str(self)} Watcher lock result: {res}')

    async def _init_conn(self, reset=False):
        """init redis conn or reset redis conn"""
        try:
            if self._conn is None or reset:
                if reset and self._conn is not None:
                    await self.release()
                self._conn = await self._redis_pool.acquire()
                self._cache = self._commands_factory(self._conn)
                self.init_watcher()
                return True
        except Exception:
            Utils.log.error(f'{str(self)} init redis conn error')
            Utils.log.error(traceback.format_exc())

    def init_watcher(self, alone=True):
        """init watch dog"""
        interval = Utils.math.floor(self._expire / 3)
        self._watcher = IntervalTask(interval or 3, self._do_heartbeat, alone=alone)

    async def exists(self):
        """check the lock exist or not"""
        await self._init_conn()
        if await self._cache.exists(self._lock_tag):
            return True
        else:
            return False

    async def acquire(self, timeout=0):
        """acquire the lock"""
        try:
            await self._init_conn()
            if self._locked:
                self._locked = await self.renew()
            else:
                params = {
                    r'key': self._lock_tag,
                    r'value': self._lock_val,
                    r'expire': self._expire,
                    r'exist': Redis.SET_IF_NOT_EXIST,
                }

                async for _ in AsyncCircularForTimeout(timeout):

                    if await self._cache.set(**params):
                        self._locked = True

                    if self._locked or timeout == 0:
                        break
            if self._locked and not self._watcher.running():
                self._watcher.start()
        except aioredis.errors.ConnectionClosedError:
            self._err_count += 1
            Utils.log.error(f'{str(self)} acquire conn closed error')
            if self._err_count >= 3:
                # If the connection is damaged, automatic reset to ensure service resume
                reset_res = await self._init_conn(reset=True)
                if reset_res:
                    self._err_count = 0

        return self._locked

    async def wait(self, timeout=0):

        async for _ in AsyncCircularForTimeout(timeout):

            if not await self.exists():
                return True
        else:

            return False

    async def renew(self):
        """renew the lock when lock held"""
        if self._cache is None:
            self._locked = False

        if self._locked:
            self._locked = False
            if await self._cache.eval(self._renew_script, [self._lock_tag], [self._lock_val, self._expire]):
                self._locked = True
            else:
                self._locked = False

        return self._locked

    async def release(self):
        """release the lock, and stop the watch dog"""
        with catch_error():
            if self._watcher.running():
                self._watcher.stop()

            if self._locked and self._cache:
                await self._cache.eval(self._unlock_script, [self._lock_tag], [self._lock_val])
                self._locked = False

            if self._conn:
                self._redis_pool.release(self._conn)
                self._cache = self._conn = None


class RedisPoolManager(SafeSingleton, BasePoolManager):
    """Redis连接池管理器"""
    def __init__(self):
        super().__init__(RedisAsyncContextManager)

    def __await__(self):

        if not self._pools:

            for pool_name, pool_config in self._config.items():

                self._pools[pool_name] = yield from aioredis.create_pool(**pool_config).__await__()

                setattr(self._pools[pool_name], 'pool_name', pool_name)

                Utils.log.success(f'redis pool {self.pool_status(pool_name)} initialized')

            self._ready = True

        return self

    def _echo_pool_info(self, pool_name='default'):

        assert self._ready, f'{self.__class__.__name__} does not initialize'

        pool = self._pools[pool_name]

        if (pool.maxsize - pool.size + pool.freesize) < Utils.math.ceil(pool.maxsize / 3):
            Utils.log.warning(
                f'Redis pool not enough ({pool_name}): {pool.freesize}({pool.size}/{pool.maxsize})'
             )

    def close(self):
        if not self._pools:
            return
        pools, self._pools = self._pools, {}
        for pool in pools.values():
            pool.close()

    def pool_status(self, pool_name='default'):
        pool = self._pools[pool_name]
        return f'<[{pool_name}] {pool.address} [db:{pool.db}, size:[{pool.minsize}:{pool.maxsize}], free:{pool.freesize}]>'

    def allocate_lock(self, key, expire=60, pool_name='default'):

        return MutexLock(self._pools[pool_name], key, expire=expire)

    def func_partial(self, conn, pool_name):
        client = Redis(conn)
        self._contexts[pool_name].set(weakref.ref(client))
        return client


redis_pool_manager = RedisPoolManager()

