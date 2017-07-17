import mongoengine as me

from . import MongoDBAccess
from .base import AsloBaseModel
from .release import ReleaseModel


class DeveloperModel(me.DynamicEmbeddedDocument):
    name = me.StringField(required=True)
    email = me.EmailField()
    page = me.URLField()
    avatar = me.URLField()


class ActivityModel(AsloBaseModel):
    meta = {'collection': 'activity'}
    bundle_id = me.StringField(required=True, unique=True)
    name = me.DictField(required=True)
    summary = me.DictField(required=True)
    categories = me.ListField(me.StringField(max_length=30))
    repository = me.StringField(required=True)
    license = me.StringField(required=True)
    icon = me.BinaryField(required=False, max_bytes=1000000)
    icon_hash = me.StringField(required=False)
    developers = me.EmbeddedDocumentListField(DeveloperModel, required=True)
    latest_release = me.ReferenceField(ReleaseModel)
    previous_releases = me.ListField(me.ReferenceField(ReleaseModel))


activity_access = MongoDBAccess(ActivityModel)
