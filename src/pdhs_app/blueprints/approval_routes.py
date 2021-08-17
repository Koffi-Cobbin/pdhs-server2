from flask import Blueprint, request, jsonify
from src.pdhs_app.models.users.user import User  # src.
from src.pdhs_app.models.approvals.approval import Approval
from src.pdhs_app.models.approvals import errors as ApprovalErrors

bp = Blueprint('approvals', __name__, url_prefix='/approvals')


@bp.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        result = request.get_json()
        doc_id = result['doc_id']
        recipient_id = result['recipient_id']
        status = result['status']
        try:
            approval = Approval.query.filter_by(document_id=doc_id, recipient_id=recipient_id)
        except:
            return jsonify(message=f"Error updating approval")
        approval.status = status
        approval.save_to_db()
        return {"message": "Done"}


@bp.route('/', methods=['GET'])
def get_all_approvals():
    """
    Get all the approvals in the approval
    table.
    """
    if request.method == 'GET':
        approvals = []
        result = []
        error_msg = None
        try:
            result = Approval.query.all()
        except:
            error_msg = 'Error occured retrieving approvals'
        if len(result) == 0:
            error_msg = 'No approvals available'
        if error_msg is not None:
            return jsonify(msg=error_msg)
        else:
            for approval in result:
                approvals.append(approval.to_json())
            return jsonify(approvals=approvals)


@bp.route('/<int:approval_id>', methods=['GET'])
def get_approval_by_id(approval_id):
    """
    Get a particular approval by id
    """
    if request.method == 'GET':
        error_msg = None
        try:
            approval = Approval.find_by_id(approval_id)
            if approval is None:
                error_msg = f'No approval with ID {approval_id} found'
        except:
            error_msg = 'Error occured finding approval'
        if error_msg is not None:
            return jsonify(msg=error_msg), 404
        elif approval is not None:
            return jsonify(approval.to_json())

@bp.route('/delete/<int:approval_id>', methods=['DELETE'])
def delete_approval(approval_id):
    if request.method == 'DELETE':
        error_msg = None
        try:
            approval = Approval.find_by_id(approval_id)
        except:
             error_msg = 'Error occured finding approval'
        if approval is not None:
            try:
                approval.delete_from_db()
            except:
                error_msg = 'Error occured deleting Approval'
        if error_msg is not None:
            return jsonify(msg=error_msg), 404
        else:
            return jsonify(msg='Approval deleted successfully')
