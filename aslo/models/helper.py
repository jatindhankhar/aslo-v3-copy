from math import ceil


class Pagination:
    def __init__(self, items, page, items_per_page, total_items):
        self.items = items
        self.page = page
        self.total_items = total_items
        self.items_per_page = items_per_page
        self.num_pages = int(ceil(total_items / float(items_per_page)))

    @property
    def has_next(self):
        return self.page < self.num_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        return self.page + 1

    @property
    def prev_page(self):
        return self.page - 1
