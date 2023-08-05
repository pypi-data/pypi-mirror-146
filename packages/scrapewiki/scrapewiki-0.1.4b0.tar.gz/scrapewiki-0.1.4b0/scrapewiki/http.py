from typing import Callable, Coroutine

import httpx
import yarl

__all__ = ["HTTP"]


class HTTPContextManager:
    def __init__(
        self,
        sync_method: Callable,
        async_method: Coroutine,
        *args: tuple,
        **kwargs: dict
    ):
        self.sync_method = sync_method
        self.async_method = async_method
        self.args = args
        self.kwargs = kwargs

    async def __aenter__(self):
        return await self.async_method(*self.args, **self.kwargs)

    def __enter__(self):
        return self.sync_method(*self.args, **self.kwargs)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class HTTP:
    BASE_URL: yarl.URL = yarl.URL("https://en.wikipedia.org/")

    def __init__(self):
        self.client_kwargs = dict(timeout=httpx.Timeout(60.0))
        self.client = httpx.Client(**self.client_kwargs)
        self.async_client = httpx.AsyncClient(**self.client_kwargs)

    def get(self, url: yarl.URL, **kwargs: dict) -> HTTPContextManager:
        """Get a response from a url."""

        return HTTPContextManager(
            self.client.get, self.async_client.get, url=str(url), **kwargs
        )

    def put(self, url: yarl.URL, **kwargs) -> HTTPContextManager:
        """Put a response to a url."""

        return HTTPContextManager(
            self.client.put, self.async_client.put, url=str(url), **kwargs
        )
