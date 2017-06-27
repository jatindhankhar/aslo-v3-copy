from mongoengine import Document, StringField, DynamicEmbeddedDocument, EmbeddedDocumentListField


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

class MetaData(Document):
    name = EmbeddedDocumentListField(Name, required=True)
    bundle_id = StringField(required=True)
    summary = EmbeddedDocumentListField(Summary, required=True)
    categories = StringField(default="")
    activity_version = StringField(required=True)
    repository = StringField(required=True)
    developers = EmbeddedDocumentListField(Developer,required=True)
    # Use GridFs to store images
    #icon = FileField()


    def __str__(self):
        return self.to_json
