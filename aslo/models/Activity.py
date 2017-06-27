from mongoengine import Document, StringField, ListField, DynamicEmbeddedDocument, EmbeddedDocumentListField, IntField, FloatField, URLField, BooleanField, DateTimeField, ReferenceField


class Name(DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    def __str__(self):
        return self.to_json()


class Summary(DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    def __str__(self):
        return self.to_json()


class Developer(DynamicEmbeddedDocument):
    name = StringField(required=True)
    email = StringField()
    page = StringField()

    def __str__(self):
        return self.to_json()


class Release(Document):
    # We can aslo use StringField for storing versions
    activity_version = IntField(required=True)
    release_notes = StringField(required=True)
    # Use custom class bound method to calculate min_sugar_version ?
    min_sugar_version = FloatField(required=True)
    # Also known as xo_url
    download_url = URLField(required=True)
    is_web = BooleanField(required=True, default=False)
    is_gtk = BooleanField(required=True, default=False)
    has_old_toolbars = BooleanField(required=False, default=False)
    # Timestamp when the release was made
    timestamp = DateTimeField(required=True)


class MetaData(Document):
    name = EmbeddedDocumentListField(Name, required=True)
    bundle_id = StringField(required=True)
    summary = EmbeddedDocumentListField(Summary, required=True)
    # We aslo use ListField for categories but then we need to join and slice it from the MetaData
    categories = StringField(default="")
    #activity_version = StringField(required=True)
    repository = StringField(required=True)
    developers = EmbeddedDocumentListField(Developer, required=True)
    # Use GridFs to store images
    #icon = FileField()
    latest_release = ReferenceField(Release)
    previous_releases = ListField(ReferenceField(Release))

    def add_release(self, release):

        # If First release (No previous releases) then just copy the release
        if self.previous_releases.empty():
            latest_release = release
        else:
            self.previous_releases.insert(self.latest_release)
            self.latest_release = release

    def __str__(self):
        return self.to_json
