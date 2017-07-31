from flask import Blueprint, g, session

web = Blueprint('web', __name__, template_folder='templates',
                static_folder='static',
                static_url_path='/web/static',
                url_prefix='/<lang_code>')


@web.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)


@web.url_value_preprocessor
def pull_lang_code(point, values):
    g.lang_code = values.pop('lang_code')
    # Tie user session to a particular language,
    # so it can be retrived when we pop the request values
    session['lang_code'] = g.lang_code


from . import views  # noqa
