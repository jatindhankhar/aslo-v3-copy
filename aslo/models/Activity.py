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
    summary = EmbeddedDocumentListField(Summary, required=True)
    # We aslo use ListField for categories but then we need to join and slice it from the MetaData
    categories = StringField(default="")
    #activity_version = StringField(required=True)
    repository = StringField(required=True)
    developers = EmbeddedDocumentListField(Developer, required=True)
    # Use GridFs to store images
    icon = URLField(required=True)
    latest_release = ReferenceField(Release)
    previous_releases = ListField(ReferenceField(Release))

    def add_release(self, release):
        if self.latest_release.activity_version >= release.activity_version:
            # In that case delete the activity, since we can only reference data if we save it
            release.delete()
            raise ValidationError("New release activity version {} is less than the current version {}".format(
                self.latest_release.activity_version, release.activity_version))
        # If First release (No previous releases) then just copy the release
        if len(self.previous_releases) == 0:
            latest_release = release
        else:
            self.previous_releases.append(self.latest_release)
            self.latest_release = release
