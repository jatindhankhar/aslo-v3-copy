import abc


class Access(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def _get_impl(cls):
        pass

    @classmethod
    def get_by_id(cls, _id):
        cls._get_impl().get_by_id(_id)

    @classmethod
    def get_all(cls):
        cls._get_impl().get_all()

    @classmethod
    def add_or_update(cls, obj):
        cls._get_impl().add_or_update(obj)

    @classmethod
    def delete(cls, obj):
        cls._get_impl().delete(obj)
