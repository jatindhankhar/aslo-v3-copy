from flask import render_template, url_for,abort
from . import web
import aslo.models.Activity as model
from flask import current_app as app
import mongoengine as me



    
@web.route('/')
def index():
    try:
        me.connect(host=app.config['MONGO_URI'])
        activities = model.Activity.objects
        return render_template('index.html',activities=activities)
    except Exception as error:
        abort(404)

   

@web.route('/detail')
def detail():
    return render_template('detail.html')
