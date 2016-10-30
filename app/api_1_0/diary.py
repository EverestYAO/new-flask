from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Post,Diary





@api.route('/diarys/<int:id>')
def get_diary(id):
    diary = Diary.query.get_or_404(id)
    return jsonify(diary.to_json())