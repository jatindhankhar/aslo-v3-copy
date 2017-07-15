from flask import render_template, url_for, abort
from . import web
import aslo.models.Activity as model
from flask import current_app as app
import mongoengine as me


@web.route('/')
def index():
    try:
        me.connect(host=app.config['MONGO_URI'])
        activities = model.Activity.objects
        return render_template('index.html', activities=activities)
    except me.LookUpError as error:
        abort(404)


@web.route('/<bundle_id>/<activity_version>',strict_slashes=False)
def activity_detail(bundle_id, activity_version):
    try:
        me.connect(host=app.config['MONGO_URI'])
        activity_version = float(activity_version)
        activity = model.Activity.objects.get(bundle_id=bundle_id)
        release = activity.find_release(activity_version)
        if release is None:
            abort(404)
        else:
            return render_template('detail.html', activity=activity, current_release=release)
    except model.Activity.DoesNotExist as error:
        abort(404)
