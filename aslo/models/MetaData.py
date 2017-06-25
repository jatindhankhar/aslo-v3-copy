from mongoengine import Document, StringField, DynamicEmbeddedDocument, EmbeddedDocumentListField


class Name(DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    pass


class Summary(DynamicEmbeddedDocument):
    # Empty class to avoid any empty object since we will have dynamic fields
    pass


class MetaData(Document):
    name = EmbeddedDocumentListField(Name, required=True)
    bundle_id = StringField(required=True)
    summary = EmbeddedDocumentListField(Summary, required=True)
    # Use GridFs to store images
    icon = FileField()
