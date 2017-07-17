import mongoengine as me


def setup_db(app):
    me.connect(host=app.config['MONGO_URI'], connect=False)
