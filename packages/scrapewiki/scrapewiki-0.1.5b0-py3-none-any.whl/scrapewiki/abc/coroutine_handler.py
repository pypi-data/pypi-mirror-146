from __future__ import annotations

from abc import ABC, abstractmethod


class CoroutineHandler(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    @abstractmethod
    def sync_method(self):
        ...

    @abstractmethod
    async def async_method(self):
        ...

    def __enter__(self):
        return self.sync_method()

    async def __aenter__(self):
        return await self.async_method()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
