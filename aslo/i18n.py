from flask import request, redirect, send_from_directory
import os.path


def set_lang_redirect(app):
    def get_language():
        # Detect lang based on Accept-Language header
        langs = request.accept_languages
        if not langs:
            return 'en'

        langs = [lang.replace('-', '_') for lang in langs.values()]
        lang = langs[0]
        # treat 'en_*' languages as 'en' except for en_US and en_GB
        if 'en_' in lang and lang not in ['en_US', 'en_GB']:
            lang = 'en'

        return lang

    @app.route('/')
    def lang_redirect():
        lang_code = get_language()
        return redirect('/' + lang_code + request.full_path)

    # Manage exception for favicon
    # http://flask.pocoo.org/docs/0.12/patterns/favicon/
    @app.route('/favicon.ico')
    def handle_fav():
        return send_from_directory(
            os.path.join(app.root_path, 'web/static'), 'favicon.ico'
        )
