from flask import request,render_template, redirect,url_for
from . import douban
from .. import db
from ..models import Douban

from config import config

@douban.route('/douban', methods=['GET', 'POST'])
def douban():
    #pagination = Douban.query.order_by(Douban.title)
    #doubans = pagination
    #return render_template('douban.html', doubans=doubans)
    page = request.args.get('page',1, type=int)
    pagination = Douban.query.order_by(Douban.title).paginate(
        page,per_page=10,
        error_out=False)
    doubans = pagination.items
    return render_template('douban.html',doubans=doubans,pagination=pagination)