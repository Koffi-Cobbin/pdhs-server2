from flask import Blueprint, request, jsonify
from src.pdhs_app.models.users.user import User  # src.
from src.pdhs_app.models.approvals.approval import Approval
from src.pdhs_app.models.approvals import errors as ApprovalErrors

bp = Blueprint('approvals', __name__, url_prefix='/approval')


@bp.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        result = request.get_json()
        approval_id = request['approval_id']
        status = result['status']
        try:
            approval = Approval.query.filter_by(id=approval_id)
        except:
            return jsonify(message=f"Approval with {approval_id} does not exist")
        approval.status = status
        approval.save_to_db()
        return {"message": "Done"}
