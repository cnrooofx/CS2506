
from page import Page

class Block:
    
    def __init__(self, num_pages, page_size=0):
        self._num_pages = num_pages
        self._pages = []

        for _ in range(num_pages):
            self._pages.append(Page(page_size))

    def __str__(self):
        return "Block of {} Pages".format(self._num_pages)
    
    def __eq__(self, other):
        return self._num_pages == other.page_count()

    def __lt__(self, other):
        return self._num_pages < other.page_count()

    def __gt__(self, other):
        return self._num_pages > other.page_count()

    def __le__(self, other):
        return self._num_pages <= other.page_count()

    def __ge__(self, other):
        return self._num_pages >= other.page_count()

    def page_count(self):
        return self._num_pages


def main():
    b = Block(2)

    for page in b._pages:
        print(page)


if __name__ == "__main__":
    main()

