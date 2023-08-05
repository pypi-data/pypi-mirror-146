from __future__ import annotations

import scrapewiki

__all__ = ["Scrapewiki"]


class Scrapewiki:
    def __init__(self):
        self.http = scrapewiki.HTTP()

    def search(self, query: str, limit: int = 20, **kwargs) -> scrapewiki.searcher.Searcher:
        return scrapewiki.Searcher(self, query, limit, **kwargs)

    def wiki(self, page_name: str, **kwargs) -> scrapewiki.Wiki:
        return scrapewiki.Wiki(self, page_name, **kwargs)
