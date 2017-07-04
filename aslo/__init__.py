from flask import Flask
from flask_bootstrap import Bootstrap
import logging
from imgurpython import ImgurClient
logger = logging.getLogger(__name__)


def init_app():
    app = Flask(__name__)
    app.config.from_object('aslo.default_settings')

    # init bootstrap
    Bootstrap(app)

    # init celery
    from .celery_app import init_celery
    init_celery(app)

    imgur_client = ImgurClient(app.config['IMGUR_CLIENT_ID'],app.config['IMGUR_CLIENT_SECRET'])
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

    return app
