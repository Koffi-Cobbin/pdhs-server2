from flask import Blueprint, request, jsonify, render_template
from src.pdhs_app.models.users.user import User  # src.
import src.pdhs_app.models.users.errors as UserErrors  # src.
import src.pdhs_app.models.users.decorators as user_decorators  # src.
import src.pdhs_app.models.users.constants as UserConstants
from src.pdhs_app.models.documents.document import Document
from src.pdhs_app.models.departments.department import Department
from src.pdhs_app.blueprints.document_routes import inbox as get_new_docs
from werkzeug.utils import secure_filename
from src.middleware.cloud_upload import upload_file
# from src.storage.cloud_storage import delete_blob, upload_blob
from src.pdhs_app.models.approvals.approval import Approval

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


@bp.route('/update/<int:user_id>', methods=['PUT', 'GET', 'POST'])
def update_user(user_id):
    """
    Handling the upload of a user profile image.
    """
#     user = User.find_by_id(user_id)
    
    approvals = Approval.query.filter_by(recipient_id=user_id)
    if approvals:
        for approval in approvals:
            if approval:
                approval.delete_from_db()
            
#    docs = Document.find_by_user_id(user_id)
#     for doc in docs:
#         if doc:
#             doc.delete_from_db()
            
#     user.delete_from_db()
    
    if request.method == 'POST':
        _id = request.form['id'] if request.form['id'] else request.json.get('id', None)
        first_name = request.form['first_name'] if request.form['first_name'] else request.json.get('first_name', None)
        last_name = request.form['last_name'] if request.form['last_name'] else request.json.get('last_name', None)
        email = request.form['email'] if request.form['email'] else request.json.get('email', None)
        contact = request.form['contact'] if request.form['contact'] else request.json.get('contact', None)
        password = request.form['password'] if request.form['password'] else request.json.get('password', None)
        user_img = request.files['user_img'] if request.files['user_img'] else request.files.get('user_img', None)
        portfolio_id = request.form['portfolio_id'] if request.form['portfolio_id'] else request.json.get('portfolio_id', None)
        department_id = request.form['department_id'] if request.form['department_id'] else request.json.get('department_id', None)
        
        faculty_id = request.form['faculty_id'] if request.form['faculty_id'] else request.json.get('faculty_id', None)
        college_id = request.form['college_id'] if request.form['college_id']  else request.json.get('college_id', None)
        
        error_msg = None
        
        try:
            user = User.find_by_id(user_id)
        except Exception as e:
                print('Error uploading file: %s' % e)
                return jsonify(msg="Unauthorized request"), 401

        if user_id:
            user.id = user_id
        
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if contact:
            user.contact = contact
        if password:
            user.password = password
        if portfolio_id:
            user.portfolio_id = portfolio_id
        if department_id:
            user.department_id = department_id
        if faculty_id:
            user.faculty_id = faculty_id
        if college_id:
            user.college_id = college_id
        if user_img:
            if _allowed_file(user_img.filename):
                filename = secure_filename(user_img.filename)
                
                try:
                    user_img_url = upload_file(user_img)
                except Exception as e:
                    print('Error uploading file: %s' % e)
                    return jsonify(msg='Error uploading image'), 500
                
                if user_img_url is not None:
                    user.img_url = user_img_url

                try:
                    user.save_to_db()
                except:
                    return jsonify(msg='Error updating profile'), 500
            else:
                return jsonify(msg="Image File type not supported"), 500
        return jsonify(msg="User successfully updated")
    else:
        return render_template("users/signup.html")


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
