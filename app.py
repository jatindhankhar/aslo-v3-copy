from flask import Flask,request,abort
from celery import Celery
import os
from IPython import embed
import utils

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
# Set false for production systems
app.debug = True
GITHUB_HOOK_SECRET = os.environ.get('GITHUB_HOOK_SECRET')

@app.route('/')
def main():
    return "Welcome"

@app.route('/webhook',methods=['POST'])
def handle_payload():
    content = request.get_json(silent=True)
    #embed()
    header_signature = request.headers['X-Hub-Signature']
    embed()
    if header_signature is None:
        abort(403)
    if not utils.verify_signature(header_signature,request.data,GITHUB_HOOK_SECRET):
        abort(403)

    return "Authenticated request :D"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
