from flask import Blueprint, request, jsonify
from src.pdhs_app.models.users.user import User  # src.
from src.pdhs_app.models.comments.comment import Comment

bp = Blueprint('comments', __name__, url_prefix='/comments')


@bp.route('/hello', methods=['GET'])
def hello():
    if request.method == 'GET':
        return "Hello from /comment"
