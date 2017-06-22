import hmac
import hashlib


def verify_signature(gh_signature, body, secret):
    sha1 = hmac.new(secret.encode(), body, hashlib.sha1).hexdigest()
    return hmac.compare_digest('sha1=' + sha1, gh_signature)
