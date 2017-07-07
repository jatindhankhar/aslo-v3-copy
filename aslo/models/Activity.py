import mongoengine as me


class Name(me.DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.to_mongo.to_dict()


class Summary(me.DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.to_mongo.to_dict()


class Developer(me.DynamicEmbeddedDocument):
    name = me.StringField(required=True)
    email = me.EmailField()
    page = me.URLField()
    avatar = me.URLField()

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.to_mongo.to_dict()


class Release(me.Document):
    activity_version = me.FloatField(required=True)
    release_notes = me.StringField(required=True)
    min_sugar_version = me.FloatField(required=True)
    # Also known as xo_url
    download_url = me.URLField(required=True)
    is_web = me.BooleanField(required=True, default=False)
    is_gtk3 = me.BooleanField(required=True, default=False)
    has_old_toolbars = me.BooleanField(required=False, default=False)
    # Timestamp when the release was made
    timestamp = me.DateTimeField(required=True)

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.to_mongo.to_dict()


class Activity(me.Document):
    bundle_id = me.StringField(required=True)
    name = me.EmbeddedDocumentField(Name, required=True)
    summary = me.EmbeddedDocumentField(Summary, required=True)
    categories = me.ListField(me.StringField(max_length=30))
    repository = me.StringField(required=True)
    license = me.StringField(required=True)
    developers = me.EmbeddedDocumentListField(Developer, required=True)
    latest_release = me.ReferenceField(Release)
    previous_releases = me.ListField(me.ReferenceField(Release))

    def __str__(self):
        return self.to_json()

    def to_dict(self):
        return self.to_mongo.to_dict()

    def add_release(self, release):
        # first release
        if not self.latest_release and len(self.previous_releases) == 0:
            self.latest_release = release
            return

        if self.latest_release.activity_version >= release.activity_version:
            release.delete()
            raise me.ValidationError(
                'New activity release version {} is less or equal than the '
                'current version {}'.format(
                    release.activity_version,
                    self.latest_release.activity_version
                 )
            )

        self.previous_releases.append(self.latest_release)
        self.latest_release = release

    def set_developers(self, developers):
        devs = []
        for developer in developers:
            dev = Developer()
            dev.name = developer['name']
            dev.email = developer['email']
            dev.page = developer['page']
            dev.avatar = developer['avatar']
            devs.append(dev)
        self.developers = devs
