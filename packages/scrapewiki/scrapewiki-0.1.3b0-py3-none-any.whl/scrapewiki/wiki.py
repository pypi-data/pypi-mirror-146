from __future__ import annotations

import unicodedata
from typing import Iterator

import arrow
import trio
from selectolax.parser import HTMLParser, Node

import scrapewiki
from scrapewiki.abc.coroutine_handler import CoroutineHandler
from scrapewiki.constants import NOT_FOUND_TEXT
from scrapewiki.structures import (
    Category,
    Content,
    ExternalLink,
    Header,
    HeaderListItem,
    HTMLHeaderTags,
    Note,
    Page,
    Paragraph,
    Reference,
    References,
)

__all__ = ["Wiki", "PageParser"]


class Wiki(CoroutineHandler):
    def __init__(self, scrapewiki: scrapewiki.Scrapewiki, page_name: str, **kwargs):
        super().__init__(page_name, **kwargs)
        self.scrapewiki = scrapewiki
        self.page_name = page_name
        self.kwargs = kwargs

    @property
    def page_url(self):
        url = self.scrapewiki.http.BASE_URL / "wiki" / self.page_name
        return str(url)

    def sync_method(self) -> scrapewiki.structures.Page:
        with self.scrapewiki.http.get(self.page_url, follow_redirects=True) as response:
            return PageParser(self.scrapewiki, response.text, self.page_url).parse()

    async def async_method(self) -> scrapewiki.structures.Page:
        async with self.scrapewiki.http.get(
            self.page_url, follow_redirects=True
        ) as response:
            parser = PageParser(self.scrapewiki, response.text, self.page_url)
            return await trio.to_thread.run_sync(parser.parse)

    def __enter__(self) -> scrapewiki.structures.Page:
        return super().__enter__()

    async def __aenter__(self) -> scrapewiki.structures.Page:
        return await super().__aenter__()


class PageParser:
    def __init__(self, scrapewiki: scrapewiki.Scrapewiki, html: str, page_url: str):
        self.scrapewiki = scrapewiki
        self.html = html
        self.page_url = page_url
        self.parser = HTMLParser(html)
        self.header_names = [x.name for x in HTMLHeaderTags]

    def parse_notes(self, notes: list[Node]) -> Iterator[Note]:
        """Parse the notes from a list of nodes."""

        for note in notes:
            text = str()
            refs = list()

            for child in note.iter(include_text=True):
                if child.tag == "-text":
                    text += str(child.raw_value, "utf-8")
                elif child.tag == "a":
                    refs.append(
                        Reference(child.text(), self.parse_url(child.attrs["href"]))
                    )
                    text += child.text()
                elif child.tag != "sup":
                    text += child.text()

            yield Note(text, refs)

    def parse_categories(self, nodes: list[Node]) -> Iterator[Category]:
        """Parse the categories from a list of nodes."""

        for node in nodes:
            yield Category(
                node.css_first("a").text(),
                self.parse_url(node.css_first("a").attrs["href"]),
            )

    def parse_external_links(self, nodes: Iterator[Node]) -> Iterator[ExternalLink]:
        """Parse the external links from a list of nodes."""

        for node in nodes:
            if node.tag == "h2" and node.text(strip=True) == "External links":
                break

        for node in nodes:
            if node.tag == "ul":
                for a in node.css("a.external"):
                    yield ExternalLink(
                        a.text(),
                        a.attrs["href"],
                    )

    def parse_references(self, nodes: Iterator[Node]) -> Iterator[References]:
        """Parse the references from a list of nodes."""

        for node in nodes:
            if node.tag == "h2" and node.text(strip=True) == "References":
                break

        for node in nodes:
            if node.tag == "ol":
                for li in node.css("li"):
                    text_node = li.css_first("span.reference-text")
                    cite = text_node.css_first("cite")
                    if cite:
                        cite.unwrap()

                    references = []

                    if text_node:
                        text = self.get_paragraph(text_node).text
                        for a in text_node.css("a"):
                            a_t = a.attributes.get("title")
                            a_c = a.attributes.get("class")
                            if a_t:
                                references.append(
                                    Reference(a_t, self.parse_url(a.attributes["href"]))
                                )
                            elif a_c == "external text":
                                references.append(
                                    Reference(a.text(), a.attributes["href"])
                                )
                        yield References(text, references)

    def get_paragraph(self, node: Node) -> Paragraph:
        """Get a paragraph from a node."""

        text = str()
        refs = list()

        for child in node.iter(include_text=True):
            if child.tag == "-text":
                data = str(child.raw_value, "utf-8")
                text += unicodedata.normalize("NFD", data).replace("&#160;", " ")
            elif child.tag == "a" and "external" not in child.attributes.get(
                "class", ""
            ):
                refs.append(
                    Reference(child.text(), self.parse_url(child.attrs["href"]))
                )
                text += child.text()
            elif child.tag not in ("sup", "style"):
                text += child.text()

        text = text.strip()
        if text or refs:
            return Paragraph(text, refs)

    def parse_contents(self, toc: Node) -> list[Content]:
        """Parse the contents of the table of contents."""

        contents = list()

        for node in toc.iter():
            if node.tag == "li":
                name = node.css_first("a").attributes["href"][1:]
                url = str(
                    (self.scrapewiki.http.BASE_URL / "wiki" / self.title).with_fragment(
                        node.css_first("a").attrs["href"][1:]
                    )
                )
                ul = node.css_first("ul")
                sub_contents = self.parse_contents(ul) if ul else None

                contents.append(Content(name, url, sub_contents))

        return contents

    def parse_ul(self, node: Node) -> list[HeaderListItem]:
        """Parse the contents of a unordered list."""

        contents = list()

        for child in node.iter():
            if child.tag == "li":
                name = child.text()
                url = child.css_first("a")
                if url:
                    if "wiki/" in url.attributes["href"]:
                        url = self.parse_url(url.attributes["href"])
                    else:
                        url = url.attributes["href"]

                ul = child.css_first("ul")
                sub_lists = self.parse_ul(ul) if ul else None

                contents.append(HeaderListItem(name, url, sub_lists))

        return contents

    def parse_url(self, url: str) -> str:
        """Parses a URL from a relative path."""

        return str(self.scrapewiki.http.BASE_URL / url[1:])

    def parse_headers(self, nodes: list[Node], headers=[]) -> list[Header]:
        """Parse headers from the given nodes."""

        if not nodes:
            return headers

        for node in nodes.copy():
            if node.tag.upper() in self.header_names:
                header = node

                try:
                    title = header.css_first("span.mw-headline").text(strip=True)
                except AttributeError:
                    title = header.text(strip=True)

                paras = []
                notes = []
                references = []
                lists = None
                nodes.pop(0)

                for node in nodes.copy():
                    if node.tag == "p":
                        paras.append(self.get_paragraph(node))
                        nodes.pop(0)

                    elif node.attributes.get("role") == "note":
                        notes.append(node)
                        nodes.pop(0)

                    elif node.tag == "ul" and title != "References":
                        lists = self.parse_ul(node)

                    elif node.tag.upper() in self.header_names:
                        headers.append(
                            Header(
                                title,
                                HTMLHeaderTags[header.tag.upper()].value,
                                list(self.parse_notes(notes)),
                                paras or None,
                                references or None,
                                lists,
                            )
                        )
                        return self.parse_headers(nodes, headers)

                return headers
            else:
                nodes.pop(0)

    def parse(self) -> Page:
        """Parse the page and return a Page object."""

        content = self.parser.css_first("#content")
        self.title = content.css_first("#firstHeading").text()

        for b in self.parser.css("div + b"):
            if b.text(strip=True) == NOT_FOUND_TEXT:
                raise scrapewiki.PageNotFound(self.title) from None

        last_modified = (
            self.parser.css_first("#footer-info-lastmod")
            .text()[30:-7]
            .replace(", at", "")
        )
        try:
            last_modified = arrow.get(last_modified, "DD MMMM YYYY HH:mm")
        except arrow.parser.ParserMatchError:
            last_modified = arrow.get(last_modified, "D MMMM YYYY HH:mm")

        content.css_first("#bodyContent").unwrap()
        content.css_first("#mw-content-text").unwrap()
        content.css_first(".mw-parser-output").unwrap()
        reflist = content.css_first("div.reflist")

        categories = list(self.parse_categories(content.css("#catlinks li a")))
        external_links = list(self.parse_external_links(content.iter()))
        contents = content.css_first(".toc ul") or None

        if contents:
            contents = self.parse_contents(contents)

        if reflist:
            reflist.unwrap()
            references = list(self.parse_references(content.iter()))
        else:
            references = None

        headers = self.parse_headers(list(content.iter()))
        return Page(
            categories,
            self.title,
            self.page_url,
            last_modified.datetime,
            headers or None,
            contents,
            external_links or None,
            references,
        )
