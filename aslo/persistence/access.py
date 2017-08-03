import abc


class Access(metaclass=abc.ABCMeta):

    @classmethod
    @abc.abstractmethod
    def _get_impl(cls):
        pass

    @classmethod
    def get_by_id(cls, _id):
        return cls._get_impl().get_by_id(_id)

    @classmethod
    def get_all(cls, *args, **kwargs):
        return cls._get_impl().get_all(*args, **kwargs)

    @classmethod
    def add_or_update(cls, obj):
        return cls._get_impl().add_or_update(obj)

    @classmethod
    def query(cls, *args, **kwargs):
        return cls._get_impl().query(*args, **kwargs)

    @classmethod
    def delete(cls, obj):
        cls._get_impl().delete(obj)

    @classmethod
    def paginate(cls, *args, **kwargs):
        return cls._get_impl().paginate(*args, **kwargs)
