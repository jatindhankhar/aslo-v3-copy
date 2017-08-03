from .helper import Pagination


class MongoDBAccess():
    def __init__(self, model):
        self._model = model

    def get_by_id(self, value):
        for model_object in self._model.objects(id=value):
            return model_object
        raise ValueError('{} with id "{}" does not exist.'.format(
            self._model.__name__, value))

    def get_all(self, *args, **kwargs):
        return self.query(*args, **kwargs)

    def add_or_update(self, model_object):
        return model_object.save()

    def query(self, offset=0, limit=None, order_by=None, exclude_fields=None,
              Qcombination=None, **filters):
        order_by = order_by or []
        exclude_fields = exclude_fields or []
        eop = offset + int(limit) if limit else None

        if Qcombination:
            result = self._model.objects.filter(Qcombination)
        else:
            result = self._model.objects.filter(**filters)

        if exclude_fields:
            result = result.exclude(*exclude_fields)

        result = result.order_by(*order_by)
        result = result[offset:eop]

        return result

    def delete(self, model_object):
        model_object.delete()

    def paginate(self, page=1, pagesize=9, Qcomb=None, **filters):
        pagesize = 9 if not pagesize else pagesize
        offset = (page - 1) * pagesize
        result = self.query(offset=offset, limit=pagesize, Qcombination=Qcomb,
                            **filters)
        return Pagination(result, page, pagesize, result.count())
