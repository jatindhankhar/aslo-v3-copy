import hmac
from hashlib import sha1

# Thanks to https://github.com/carlos-jenkins/python-github-webhooks/blob/master/webhooks.py
# https://developer.github.com/webhooks/securing/
def verify_signature(header_signature,raw_data,secret):
    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
       return false
    # HMAC requires the key to be bytes, pass raw request data
    mac = hmac.new(secret,raw_data,sha1)
    # Use compare_digest to avoid timing attacks
    return hmac.compare_digest(str(mac.hexdigest()), str(signature))
