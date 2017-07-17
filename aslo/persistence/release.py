from .access import Access
from aslo.models.release import release_access


class Release(Access):
    impl = release_access

    @classmethod
    def _get_impl(cls):
        return cls.impl
