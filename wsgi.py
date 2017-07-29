from aslo import init_app
from flask import request, redirect

application = init_app()


@application.route('/')
def handle_no_locale():
    return redirect("/en" + request.full_path)


if __name__ == "__main__":
    host = '0.0.0.0'
    application.run(host=host)
