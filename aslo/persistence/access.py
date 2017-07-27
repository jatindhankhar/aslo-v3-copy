import abc
from math import ceil


class Access(metaclass=abc.ABCMeta):

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

    @classmethod
    @abc.abstractmethod
    def _get_impl(cls):
        pass

    @classmethod
    def get_by_id(cls, _id):
        return cls._get_impl().get_by_id(_id)

    @classmethod
    def get_all(cls):
        return cls._get_impl().get_all()

    @classmethod
    def add_or_update(cls, obj):
        return cls._get_impl().add_or_update(obj)

    @classmethod
    def delete(cls, obj):
        cls._get_impl().delete(obj)

    @classmethod
    def paginate(cls, page=1, items_per_page=10):
        skip = (page - 1) * items_per_page
        limit = items_per_page
        model_objects = cls.get_all()

        return cls.Pagination(items=model_objects.limit(limit).skip(skip), page=page, items_per_page=items_per_page,
                              total_items=model_objects.count())
