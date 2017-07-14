from flask import render_template,url_for
from . import web


@web.route('/')
def index():
    return render_template('index.html')

@web.route('/detail')
def detail():
    return render_template('detail.html')