from flask import Blueprint, request, jsonify
from src.pdhs_app.models.users.user import User  # src.
from src.pdhs_app.models.faculties.faculty import Faculty

bp = Blueprint('facultys', __name__, url_prefix='/faculty')


@bp.route('/hello', methods=['GET'])
def hello():
    if request.method == 'GET':
        return "Hello from /faculty"
