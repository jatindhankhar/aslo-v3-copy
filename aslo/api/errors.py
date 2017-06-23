import json
from flask import make_response
from . import api
from .exceptions import ApiHttpError


@api.errorhandler(ApiHttpError)
def HandleHttpApiError(e):
    error_msg = json.dumps(e.to_dict())
    response = make_response(error_msg, e.status_code)
    response.headers['Content-Type'] = 'application/json'
    return response
