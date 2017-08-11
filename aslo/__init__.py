from flask import Flask
from flask_babel import Babel
import logging

logger = logging.getLogger(__name__)


def init_app():
    app = Flask(__name__)
    app.config.from_object('aslo.settings')

    from .i18n import set_lang_redirect
    set_lang_redirect(app)

    # init celery
    from .celery_app import init_celery
    init_celery(app)

    # init Babel
    babel = Babel(app)  # noqa

    # blueprints
    from .web import web
    app.register_blueprint(web)

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    # logging
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('[%(asctime)s] %(levelname).3s %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)
    logger.addHandler(stream_handler)

    if app.config['DEBUG']:
        logger.setLevel(logging.DEBUG)

    # setup db
    from .service import setup_db
    setup_db(app)

    # custom jinja filters
    from .filters import init_filters
    init_filters(app)

    return app
