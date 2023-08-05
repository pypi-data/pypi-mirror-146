import json
import uuid
from contextvars import ContextVar


class BasePoolManager:
    def __init__(self, client_context_manager):
        self._pools = {}
        self._config = {}
        self._ready = False
        self._client_context_manager = client_context_manager
        self._contexts = {}

    def register(self, config):
        assert not self.ready, f'{self.__class__.__name__} already registered'
        self._contexts = {
            pool_name: ContextVar(f'{self.__class__.__name__}_{pool_name}_{uuid.uuid1()}', default=None)
            for pool_name in config
        }
        self._config = config

    async def initialize(self):

        await self

    def __await__(self):

        raise NotImplementedError()

    def __repr__(self):
        return id(self)

    def __str__(self):
        return json.dumps({
            pool_name: self.pool_status(pool_name)
            for pool_name, pool in self._pools.items()
        }, indent=4, ensure_ascii=False)

    @property
    def ready(self):

        return self._ready

    def func_partial(self, conn, pool_name):

        raise NotImplementedError()

    def pool_status(self, pool_name='default'):

        raise NotImplementedError()

    def _echo_pool_info(self, pool_name='default'):

        raise NotImplementedError()

    def get_context_client(self, pool_name='default'):
        ref = self._contexts[pool_name].get()
        client = None
        if ref is not None:
            _client = ref() or None
            if _client and not _client.closed:
                client = _client
        return client

    def get_client(self, pool_name='default'):
        self._echo_pool_info(pool_name)
        _client = self.get_context_client(pool_name)
        if _client:
            return self._client_context_manager(_client, self.func_partial)

        return self._client_context_manager(self._pools[pool_name], self.func_partial)

    async def close(self):

        raise NotImplementedError()
