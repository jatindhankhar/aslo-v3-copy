import mongoengine as me


class AsloBaseModel(me.Document):

    # http://docs.mongoengine.org/guide/defining-documents.html#abstract-classes
    meta = {
        'abstract': True
    }

    def to_dict(self):
        return self.to_mongo.to_dict()
