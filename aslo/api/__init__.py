from flask import Blueprint
from imgurpython import ImgurClient
api = Blueprint('api', __name__)

imgurClient =  ImgurClient(api.app.config['IMGUR_CLIENT_ID'],api.app.config['IMGUR_CLIENT_SECRET'])
from . import views, errors # noqa