from aslo import init_app
from flask import request, redirect, g, send_from_directory
from flask.ext.babel import Babel
import os

application = init_app()
babel = Babel(application)


# Handle Annoyning Favicon.ico
# TODO - Delegate static asset handling to Proxy Server
# http://flask.pocoo.org/docs/0.12/patterns/favicon/
@application.route('/favicon.ico')
def handle_fav():
    return send_from_directory(
        os.path.join(application.root_path, 'web/static/'),
        'favicon.ico')


@babel.localeselector
def get_locale():
    # if a user is logged in, use the locale from the user settings
    user = getattr(g, 'user', None)
    if user is not None:
        print("Return use locale")
        return user.locale
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  We support de/fr/en/es/hi in this
    # example.  The best match wins.
    return request.accept_languages.best_match(['de', 'hi', 'fr', 'en', 'es'])


@application.route('/')
def handle_no_locale():
    fallback_locale = get_locale().strip()
    return redirect("/" + fallback_locale + request.full_path)


if __name__ == "__main__":
    host = '0.0.0.0'
    application.run(host=host)
