from flask import request, current_app as app

from . import api
from .exceptions import ApiHttpError
from .tasks import release_process
from .gh import verify_signature


@api.route('/hook', methods=['POST'])
def hook():
    if request.is_json:
        body_json = request.get_json()
    else:
        raise ApiHttpError(
            'Invalid Content-type. application/json expected.', 400
        )

    if 'X-Hub-Signature' not in request.headers:
        raise ApiHttpError(
            'X-Hub-Signature header required.', 400
        )

    valid_signature = verify_signature(
        request.headers['X-Hub-Signature'],
        request.data,
        app.config['GITHUB_HOOK_SECRET']
    )

    if not valid_signature:
        raise ApiHttpError('Invalid Signature', 400)

    release_process.apply_async(args=[body_json])

    return "{'status_code': 200, 'message': 'OK'}", 200
