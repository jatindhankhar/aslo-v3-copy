from flask import Blueprint

web = Blueprint('web', __name__, template_folder='templates',
                static_folder='static')

from . import views # noqa
