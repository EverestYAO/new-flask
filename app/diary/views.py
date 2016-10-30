from flask import request,render_template, redirect,url_for
from . import diary
from .. import db
from ..models import Diary
from .forms import DiaryForm
from config import config

@diary.route('/diary', methods=['GET', 'POST'])
def blog():
    form = DiaryForm()
    if form.validate_on_submit():

        diary = Diary(title=form.title.data,body=form.body.data,src=form.src.data)
        db.session.add(diary)
        return redirect('diary')
    page = request.args.get('page',1, type=int)
    pagination = Diary.query.order_by(Diary.timestamp.desc()).paginate(
        page,per_page=20,
        error_out=False)
    diarys = pagination.items
    return render_template('diary.html', form = form,diarys=diarys,pagination=pagination)

@diary.route('/diary/<int:id>', methods=['GET', 'POST'])
def diary(id):
    diary = Diary.query.get_or_404(id)
    return render_template('diarys.html', diarys=[diary])
