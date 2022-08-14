from typing import TypeVar, Generic, List

T = TypeVar('T')


class Page(Generic[T]):
    def __init__(self, items: List[T], page: int, page_size: int, total: int):
        self._items = items
        self._page = page
        self._page_size = page_size
        self._total = total

    @property
    def items(self):
        return self._items

    @property
    def page(self):
        return self._page

    @property
    def page_size(self):
        return self._page_size

    @property
    def total(self):
        return self._total
