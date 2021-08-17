from flask import Blueprint, request, jsonify
from src.pdhs_app.models.users.user import User  # src.
import src.pdhs_app.models.users.errors as UserErrors  # src.
import src.pdhs_app.models.users.decorators as user_decorators  # src.
import src.pdhs_app.models.users.constants as UserConstants
from src.pdhs_app.models.documents.document import Document
from src.pdhs_app.models.departments.department import Department
from src.pdhs_app.blueprints.document_routes import inbox as get_new_docs
from werkzeug.utils import secure_filename
from src.storage.cloud_storage import delete_blob, upload_blob

bp = Blueprint('users', __name__, url_prefix='/users')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def _allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
    Query the database and return a single user that matches the specified id
    """
    if request.method == 'GET':
        user = User.find_by_id(user_id)
    if user is not None:
        return jsonify(user.to_json())
    return jsonify(msg="User not found"), 404


@bp.route('/<string:email>', methods=['GET'])
def get_user_by_email(email):
    if request.method == 'GET':
        user = User.find_by_email(email)
    if user is not None:
        return jsonify(user.to_json())
    return jsonify(msg="User not found"), 404


@bp.route('/update/profile-image/<int:user_id>', methods=['PUT'])
def update_user_profile_image(user_id):
    """
    Handling the upload of a user profile image.
    """
    if request.method == 'PUT':
        image_file = request.files.get('user_img', None)
        error_msg = None
        if user_id is None:
            error_msg = 'User ID is required'
        elif image_file is None:
            error_msg = 'No selected file'
        if error_msg is not None:
            return jsonify(msg=error_msg), 500
        else:
            user = User.find_by_id(user_id)
            if user is None:
                return jsonify(msg="Unauthorized request"), 401

        if _allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_filename = f"{user_id}_{filename}"
            image_url = upload_blob(
                image_file.stream, image_filename)
            if image_url is not None:
                user.img_url = image_url
            else:
                return jsonify(msg="Error uploading image")
            try:
                user.save_to_db()
                return jsonify(image=image_url), 200
            except:
                return jsonify(msg='Error updating profile'), 500
        else:
            return jsonify(msg="File type not supported"), 500


@bp.route('/delete/profile-image/<int:user_id>', methods=['DELETE'])
def delete_user_profile_image(user_id):
    if request.method == 'DELETE':
        error_msg = None
        try:
            user = User.find_by_id(user_id)
        except:
            error_msg = 'Error occured finding user'
            error_code = 404
        if user is not None:
            image_filename = user.img_url.split('/').pop()
            if not delete_blob(image_filename):
                error_msg = 'Error occured deleting user from cloud storage'
                error_code = 500
            else:
                user.img_url = ''
                user.save_to_db()
        if error_msg is not None:
            return jsonify(msg=error_msg), error_code
        else:
            return jsonify(msg='Profile Image deleted successfully'), 200


@bp.route('/', methods=['GET'])
def get_all_users():
    """
    Return all the users in the user table
    """
    if request.method == 'GET':
        result = []
        users = []
        try:
            result = User.query.all()
        except:
            return jsonify({'msg': 'There was an error retrieving the items requested'}), 500
        for user in result:
            users.append(user.to_json())
        if len(users) == 0 or len(result) == 0:
            return jsonify({'msg': 'Ther are no registered users'}), 404
        return jsonify({'users': users})


@bp.route('delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == 'DELETE':
        user = User.find_by_id(user_id)
    if user is not None:
        try:
            user.delete_from_db()
        except:
            return jsonify(msg="Error deleting user."), 500

    return jsonify(msg="User not found"), 404
