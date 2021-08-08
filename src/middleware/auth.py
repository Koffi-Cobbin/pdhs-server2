from datetime import datetime, timezone
from flask import (Blueprint, request, jsonify, render_template)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required, current_user)
from src.middleware.security import jwt
from werkzeug.security import check_password_hash, generate_password_hash

from src.database import db
from src.pdhs_app.models.users.user import User
from .tokens import TokenBlocklist

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/', methods=['GET'])
def all():
    if request.method == 'GET':
        result = User.query.all()
        users = [user.to_json() for user in result]
        return jsonify(users=users)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user = User.find_by_id(identity)
    return user if user else None


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = current_user
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)

@jwt.token_verification_loader
def verify_token(jwt_header, jwt_data):
    print('verify_token', jwt_header)
    return True


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None


@bp.route('/signup', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        _id = request.form['id'] if request.form['id'] else request.json.get('id', None)
        first_name = request.form['first_name'] if request.form['first_name'] else request.json.get('first_name', None)
        last_name = request.form['last_name'] if request.form['last_name'] else request.json.get('last_name', None)
        email = request.form['email'] if request.form['email'] else request.json.get('email', None)
        password = request.form['password'] if request.form['password'] else request.json.get('password', None)
        portfolio_id = request.form['portfolio_id'] if request.form['portfolio_id'] else request.json.get('portfolio_id', None)
        department_id = request.form['department_id'] if request.form['department_id'] else request.json.get('department_id', None)
        
        faculty_id = request.form['faculty_id'] if request.form['faculty_id'] else request.json.get('faculty_id', None)
        college_id = request.form['college_id'] if request.form['college_id']  else request.json.get('college_id', None)

        error = None

        if not email:
            error = 'Email is required.'
        elif not first_name:
            error = 'First name is required.'
        elif not _id:
            error = 'ID is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not portfolio_id:
            error = 'Portfolio is required.'
#         elif not department_id:
#             error = 'Department is required.'
        elif not password:
            error = 'Password is required.'
            
        elif department_id and not (faculty_id and college_id):
            error = 'Faculty and College IDs are required if Dept is provided.'
        elif faculty_id and not college_id:
            error = 'College ID is required if faculty is provided.'
            
        elif User.find_by_id(_id) is not None:
            error = f"The ID {_id} is already registered."
        elif User.find_by_email(email) is not None:
            error = f"The email address {email} is already registered."

        if error is not None:
            return jsonify({"msg": error}), 500
        else:
            password = generate_password_hash(password)
            new_user = User(
                id=_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                portfolio_id=portfolio_id,
                department_id=department_id,
                faculty_id=faculty_id,
                college_id=college_id
            )
            try:
                new_user.save_to_db()
            except Exception as e:
                print("Error saving user to database: ..............................\n", e)
                return jsonify(msg="Could not save new user to database"), 500
            return jsonify({'msg': 'User created successfully'}), 201
    return render_template("users/signup.html")


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        _id = request.json.get('id', None) #request.form['id'] if request.form['id'] else 
        password = request.json.get('password', None) # request.form['password'] if request.form['password'] else 
        try:
            user = User.find_by_id(int(_id))
        except:
            return jsonify(message="User Don't Exist")
        correct_password = check_password_hash(user.password, password)
        if _id is not None and correct_password:
            user.last_login = datetime.utcnow()
            user.save_to_db()
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return jsonify(access_token=access_token, refresh_token=refresh_token, user=user.to_json()), 200
        else:
            return jsonify(msg='Invalid ID or password'), 401
    else:
        return render_template("users/login.html") #404


@bp.route('/logout', methods=["DELETE"])
@jwt_required()
def modify_token():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    token_block = TokenBlocklist(
        jti=jti, created_at=now, created_by=current_user.id)
    db.session.add(token_block)
    db.session.commit()
    return jsonify(msg="JWT revoked")


@bp.route('/test_login', methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@bp.route("/who_am_i", methods=["GET"])
@jwt_required()
def who_am_i():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        first_name=current_user.first_name.title(),
        last_name=current_user.last_name.title()
    )


# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.filter_by(id=user_id).first()


# @bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view
