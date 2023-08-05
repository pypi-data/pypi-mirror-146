from __future__ import annotations

from typing import AsyncIterator, Iterator

import arrow
import trio
from selectolax.parser import HTMLParser, Node

import scrapewiki

from .abc.coroutine_handler import CoroutineHandler
from .structures import BytesConvertUnits, SearchResult

__all__ = ["Searcher", "SearchParser"]


class Searcher(CoroutineHandler):
    def __init__(self, scrapewiki: scrapewiki.Scrapewiki, query: str, limit: int, **kwargs):
        super().__init__(query, **kwargs)
        self.scrapewiki = scrapewiki
        self.query = query
        self.limit = limit
        self.kwargs = kwargs

    @property
    def search_url(self):
        url = self.scrapewiki.http.BASE_URL / "w/index.php"
        url = url.with_query(
            dict(
                title="Special:Search",
                search=self.query,
                limit=self.limit,
                offset=0,
                ns0=1,
            )
        )
        return url

    def sync_method(self) -> SearchParser:
        with self.scrapewiki.http.get(self.search_url) as response:
            return SearchParser(self.scrapewiki, self.query, response.text)

    async def async_method(self) -> SearchParser:
        async with self.scrapewiki.http.get(self.search_url) as response:
            return SearchParser(self.scrapewiki, self.query, response.text)

    def __enter__(self) -> Iterator[SearchResult]:
        return super().__enter__()

    async def __aenter__(self) -> AsyncIterator[SearchResult]:
        return await super().__aenter__()


class SearchParser:
    def __init__(self, scrapewiki_obj: scrapewiki.Scrapewiki, query: str, html: str):
        self.scrapewiki = scrapewiki_obj
        self.html = html
        self.parser = HTMLParser(html)
        self.li_tags = self.parser.css("li.mw-search-result")

        if self.parser.css_first(".mw-search-nonefound") is not None:
            raise scrapewiki.QueryNotMatched(query) from None

    def parse_li(self, li: Node) -> SearchResult:
        """Parses and returns the search result from a list item."""

        heading_a = li.css_first(".mw-search-result-heading a")

        title = heading_a.attrs["title"]
        snippet = li.css_first(".searchresult").text()
        url = str(self.scrapewiki.http.BASE_URL / heading_a.attrs["href"][1:])
        size, words, date = self.parse_information(
            li.css_first(".mw-search-result-data").text()
        )

        return SearchResult(title, snippet, url, size, words, date)

    def __iter__(self):
        return self

    def __aiter__(self):
        return self

    def __next__(self):
        if self.li_tags:
            return self.parse_li(self.li_tags.pop(0))
        else:
            raise StopIteration

    async def __anext__(self):
        if self.li_tags:
            return await trio.to_thread.run_sync(self.parse_li, self.li_tags.pop(0))
        else:
            raise StopAsyncIteration

    def parse_information(self, info: str):
        """Parses and returns the information of the search result."""

        size_words, ratio_date = info.split(" - ")

        size, words = size_words.split(" (")
        size, size_unit = size.split()
        size = int(size.replace(",", "")) * BytesConvertUnits[size_unit.upper()].value

        words = int(words.split()[0].replace(",", ""))
        date = ratio_date.split(maxsplit=1)[1]

        try:
            date = arrow.get(date, "DD MMMM YYYY")
        except arrow.parser.ParserMatchError:
            date = arrow.get(date, "D MMMM YYYY")

        return int(size), words, date.datetime
