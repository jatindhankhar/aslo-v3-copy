from .access import Access
from aslo.models.activity import activity_access


class Activity(Access):
    impl = activity_access

    @classmethod
    def _get_impl(cls):
        return cls.impl

    @classmethod
    def get_by_bundle_id(cls, value):
        _model = cls._get_impl()._model
        try:
            activity = _model.objects.get(bundle_id=value)
        except _model.DoesNotExist:
            activity = None

        return activity
