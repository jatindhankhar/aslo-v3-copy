import mongoengine as me

from . import MongoDBAccess
from .base import AsloBaseModel


class ReleaseModel(AsloBaseModel):
    meta = {'collection': 'release'}
    activity_version = me.FloatField(required=True)
    release_notes = me.StringField(required=True)
    min_sugar_version = me.FloatField(required=True)
    # Also known as xo_url
    download_url = me.URLField(required=True)
    is_web = me.BooleanField(required=True, default=False)
    is_gtk3 = me.BooleanField(required=True, default=False)
    has_old_toolbars = me.BooleanField(required=False, default=False)
    screenshots = me.DictField()
    # Timestamp when the release was made
    timestamp = me.DateTimeField(required=True)


release_access = MongoDBAccess(ReleaseModel)
