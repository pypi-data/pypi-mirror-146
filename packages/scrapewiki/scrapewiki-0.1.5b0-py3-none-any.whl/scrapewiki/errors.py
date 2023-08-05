__all__ = ["PageNotFound", "QueryNotMatched"]


class PageNotFound(Exception):
    """
    Raised when no page for the given title was found.

    Attributes:
    -----------
    title: str
        The title of the page that was not found.
    """

    def __init__(self, title):
        super().__init__()
        self.title = title

    def __str__(self):
        return f"Page was not found: {self.title}"


class QueryNotMatched(Exception):
    """
    Raised when the query did not match any pages.

    Attributes:
    -----------
    query: str
        The query that was not matched.
    """

    def __init__(self, query):
        super().__init__()
        self.query = query

    def __str__(self):
        return f"Query was not matched: {self.query}"
