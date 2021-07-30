from flask import Blueprint, request, jsonify
from pdhs_app.models.users.user import User  # src.
from pdhs_app.models.faculties.faculty import Faculty

bp = Blueprint('facultys', __name__, url_prefix='/faculty')


@bp.route('/hello', methods=['GET'])
def hello():
    if request.method == 'GET':
        return "Hello from /faculty"
