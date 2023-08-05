from __future__ import annotations

import datetime
from dataclasses import dataclass

__all__ = [
    "SearchResult",
    "Reference",
    "References",
    "Category",
    "ExternalLink",
    "Note",
    "CiteNote",
    "Paragraph",
    "Header",
    "Content",
    "HeaderListItem",
    "Page",
]


@dataclass
class SearchResult:
    """
    A search result.

    Attributes
    ----------
    `title`: `str`
        The title of the page.
    `snippet`: `str`
         The short description of the search result.
    `url`: `str`
        The url of the page.
    `size`: `int`
        The size of the page in bytes unit.
    `word_count`: `int``
        The word count of the page.
    `last_modified`: `datetime.datetime`
        The last modified date of the page.
    """

    title: str
    snippet: str
    url: str
    size: int
    word_count: int
    last_modified: datetime.datetime


@dataclass
class Reference:
    """
    A reference.

    Attributes
    ----------
    `name`: `str`
        The name of the reference.
    `url`: `str`
        The url of the reference.
    """

    name: str
    url: str


@dataclass
class References:
    """
    One item from the list of references in the "References" section of any page.

    Attributes
    ----------
    `text`: `str`
        The text of the reference.
    `references`: `list[Reference]`
        The list of references.
    """

    text: str
    references: list[Reference]


@dataclass
class Category:
    """
    A category.

    Attributes
    ----------
    `name`: `str`
        The name of the category.
    `url`: `str`
        The url of the category.
    """

    name: str
    url: str


@dataclass
class ExternalLink:
    """
    An external link.

    Attributes
    ----------
    `name`: `str`
        The name of the external link.
    `url`: `str`
        The url of the external link.
    """

    name: str
    url: str


@dataclass
class Note:
    """
    A note.

    Attributes
    ----------
    `text`: `str`
        The text of the note.
    `references`: `list[Reference]`
        The references of the note.
    """

    text: str
    references: list[Reference]


@dataclass
class CiteNote:
    """
    Unused
    ------
    A cite note.

    Attributes
    ----------
    `text`: `str`
        The text of the cite note.
    `references`: `list[Reference]`
        The references of the cite note.
    """

    text: str
    references: list[Reference]


@dataclass
class Paragraph:
    """
    A paragraph.

    Attributes
    ----------
    text: `str`
        The text of the paragraph.
    references: `list[Reference]`
        The references of the paragraph.
    """

    text: str
    references: list[Reference]

    def __repr__(self):
        return f"Paragraph(text='{self.text[:30]}...', references={self.references!r})"


@dataclass
class Header:
    """
    A header.

    Attributes
    ----------
    `text`: `str`
        The text of the header.
    `level`: `int`
        The level of the header.
    `notes`: `list[Note]`
        The notes of the header.
    `references`: `list[Reference]`
        The references of the header."""

    text: str
    level: int
    notes: list[Note]
    paragraphs: list[Paragraph] | None
    references: list[Reference] | None
    lists: list[Reference] | None

    def __repr__(self):
        return f"<Header level={self.level} text={self.text}, paragraphs={self.paragraphs}>"


@dataclass
class Content:
    """
    A content.

    Attributes
    ----------
    `name`: `str`
        The name of the content.
    `url`: `str`
        The url of the content.
    `sub_contents`: `list[Content]`
        The sub contents of the content.
    """

    name: str
    url: str
    sub_contents: list[Content] | None

    def __repr__(self) -> str:
        return f"<Content: {self.name}>"


@dataclass
class HeaderListItem:
    """
    A list item.

    Attributes
    ----------
    `text`: `str`
        The text of the list item.
    `url`: `str`
        The url of the first a tag if found.
    `sub_lists`: `list[HeaderListItem]`
        The sub lists of the list item.
    """

    name: str
    url: str
    sub_lists: list[HeaderListItem] | None

    def __repr__(self) -> str:
        return f"<HeaderListItem: {self.name}>"


@dataclass
class Page:
    """
    A page.

    Attributes
    ----------
    `categories`: `list[Category]`
        The categories of the page.
    `title`: `str`
        The title of the page.
    `url`: `str`
        The url of the page.
    `headers`: `list[Header]`
        The headers of the page.
    `contents`: `list[Content]`
        The content of the page.
    `external_links`: `list[ExternalLink]`
        The external links of the page.
    `references`: `list[References]`
        The references listed in the "References" section of the page.
    """

    categories: list[Category]

    title: str
    url: str
    last_modified: datetime.datetime

    headers: list[Header] = None
    contents: list[Reference] = None
    external_links: list[ExternalLink] = None
    references: list[References] = None
