

class ReleaseError(Exception):
    pass


class BuildProcessError(ReleaseError):
    pass


class ApiHttpError(Exception):

    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code if status_code else 400

    def to_dict(self):
        return {
            'message': self.message,
            'status_code': self.status_code
        }
