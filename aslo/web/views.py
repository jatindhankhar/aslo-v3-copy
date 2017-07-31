from . import web
from flask import render_template, abort, request, redirect, url_for, flash
from aslo.persistence.activity import Activity
from aslo.service import activity as activity_service
from aslo.persistence.access import Pagination


@web.route('/', defaults={'page': 1})
@web.route('/page/<int:page>')
def index(page):
    paginated_activities = Activity.paginate(page=page)
    return render_template('index.html', activities=paginated_activities)


@web.route('/<bundle_id>/<activity_version>', strict_slashes=False)
def activity_detail(bundle_id, activity_version):
    activity_version = float(activity_version)
    activity = Activity.get_by_bundle_id(bundle_id)
    if activity is None:
        abort(404)

    release = activity_service.find_release(activity, activity_version)
    if release is None:
        abort(404)
    else:
        return render_template('detail.html', activity=activity,
                               current_release=release)


@web.route('/search', methods=['GET', 'POST'])
@web.route('/search/page/<int:page>', methods=['GET', 'POST'])
def search(page=1, items_per_page=10):
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get("name")

    if not name:
        return redirect(url_for('web.index'))

    query_result = activity_service.search_by_activity_name(name)
    skip = (page - 1) * items_per_page
    limit = items_per_page
    paginated_query = Pagination(
        items=query_result.limit(limit).skip(skip),
        page=page,
        items_per_page=items_per_page,
        total_items=query_result.count())
    flash("Search Results for {}".format(name), 'success')
    return render_template('index.html',
                           activities=paginated_query,
                           search_query=name)
