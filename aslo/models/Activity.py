from mongoengine import Document, StringField, ListField, DynamicEmbeddedDocument, EmbeddedDocumentListField, IntField, FloatField, URLField, BooleanField, DateTimeField, ReferenceField, ValidationError


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
    activity_version = FloatField(required=True)
    release_notes = StringField(required=True)
    # Use custom class bound method to calculate min_sugar_version ?
    min_sugar_version = FloatField(required=True)
    # Also known as xo_url
    download_url = URLField(required=True)
    is_web = BooleanField(required=True, default=False)
    is_gtk = BooleanField(required=True, default=False)
    has_old_toolbars = BooleanField(required=False, default=False)
    # Timestamp when the release was made
    screenshots = ListField(URLField(required=False), required=False)
    timestamp = DateTimeField(required=True)

    def __str__(self):
        self.to_json()


class MetaData(Document):
    name = EmbeddedDocumentListField(Name, required=True)
    bundle_id = StringField(required=True)
    summary = EmbeddedDocumentListField(Summary, required=False, default=[])
    # We aslo use ListField for categories but then we need to join and slice it from the MetaData
    categories = StringField(default="")
    #activity_version = StringField(required=True)
    repository = StringField(required=True)
    developers = EmbeddedDocumentListField(Developer, required=False)
    # Base64 encoded string to store images
    icon = StringField(required=True)
    latest_release = ReferenceField(Release)
    previous_releases = ListField(ReferenceField(Release))

    def add_release(self, release):
        # first release
        if not self.latest_release and len(self.previous_releases) == 0:
            self.latest_release = release
            return

        if self.latest_release.activity_version >= release.activity_version:
            release.delete()
            raise ValidationError(
                'New activity release version {} is less or equal than the '
                'current version {}'
                .format(
                    release.activity_version,
                    self.latest_release.activity_version
                )
            )

        self.previous_releases.append(self.latest_release)
        self.latest_release = release
