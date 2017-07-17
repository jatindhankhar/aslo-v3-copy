import base64


def b64encode(s):
    return base64.b64encode(s).decode()


def init_filters(app):
    # see https://github.com/pallets/flask/issues/1907
    app.jinja_env.auto_reload = True
    app.jinja_env.filters['b64encode'] = b64encode
