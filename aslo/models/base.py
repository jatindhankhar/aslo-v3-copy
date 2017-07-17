import mongoengine as me


class AsloBaseModel(me.Document):

    # http://docs.mongoengine.org/guide/defining-documents.html#abstract-classes
    meta = {
        'abstract': True
    }

    def to_dict(self):
        return self.to_mongo.to_dict()


class MongoDBAccess():
    def __init__(self, model):
        self._model = model

    def get_by_id(self, value):
        for model_object in self._model.objects(id=value):
            return model_object
        raise ValueError('{} with id "{}" does not exist.'.format(
            self._model.__name__, value))

    def get_all(self):
        return self._model.objects()

    @staticmethod
    def add_or_update(model_object):
        return model_object.save()

    @staticmethod
    def delete(model_object):
        model_object.delete()
