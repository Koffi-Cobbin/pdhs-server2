from flask import Blueprint, request, jsonify, render_template
from src.pdhs_app.models.users.user import User  # src.
from src.pdhs_app.models.colleges.college import College

bp = Blueprint('colleges', __name__, url_prefix='/colleges')


@bp.route('/', methods=['GET'])
def get_all_colleges():
    """
    Get all the colleges in the college
    table.
    """
    if request.method == 'GET':
        colleges = []
        result = []
        error_msg = None
        try:
            result = College.query.all()
        except:
            error_msg = 'Error occured retrieving colleges'
        if len(result) == 0:
            error_msg = 'No colleges available'
        if error_msg is not None:
            return jsonify(msg=error_msg)
        else:
            for college in result:
                colleges.append(college.to_json())
            return jsonify(colleges=colleges)


@bp.route('/<int:college_id>', methods=['GET'])
def get_college_by_id(college_id):
    """
    Get a particular college by id
    """
    if request.method == 'GET':
        error_msg = None
        try:
            college = College.find_by_id(college_id)
        except:
            error_msg = 'Error occured finding college'
        if error_msg is not None:
            return jsonify(msg=error_msg), 404
        elif college is not None:
            return jsonify(college.to_json())


@bp.route('/new', methods=['GET', 'POST'])
def create_new_college():
    """
    Create a college
    """
    if request.method == 'POST':
        id = request['id'] if request['id'] else request.json.get('id', None) 
        name = request['name'] if request['name'] else request.json.get('name', None)
        provost_id = request['provost_id'] if request['provost_id'] else request.json.get('provost_id', None)
        error_msg = None
        if not id:
            error_msg = 'Id is required.'
        elif not name:
            error_msg = 'Name is required.'
        elif not provost_id:
            provost_id = 0
        if error_msg is not None:
            return jsonify(msg=error_msg), 500
        else:
            new_college = College(
                id=id,
                name=name,
                provost_id=provost_id
            )
            try:
                new_college.save_to_db()
            except:
                return jsonify(msg='Error saving College to database'), 500
            return jsonify(new_college.to_json()), 201
    return render_template("colleges/add_college.html")


@bp.route('/update/<int:college_id>', methods=['PUT'])
def update_college(college_id):
    """
    Update a College
    """
    if request.method == 'PUT':
        college_id = request.json.get('id', None)
        name = request.json.get('name', None)
        provost_id = request.json.get('provost_id', None)

        if not college_id:
            return jsonify(msg='Id is required.'), 500
        else:
            try:
                new_college = College.find_by_id(college_id)
                if new_college is not None:
                    if name is not None:
                        new_college.name = name
                    if provost_id is not None:
                        new_college.provost_id = provost_id
                    new_college.save_to_db()
            except:
                return jsonify(msg='Error updating College'), 500
            return jsonify(new_college.to_json()), 201


@bp.route('/delete/<int:college_id>', methods=['DELETE'])
def delete_college(college_id):
    if request.method == 'DELETE':
        error_msg = None
        try:
            college = College.find_by_id(college_id)
        except:
            error_msg = 'Error occured finding college'
        if college is not None:
            try:
                college.delete_from_db()
            except:
                error_msg = 'Error occured deleting College'
        if error_msg is not None:
            return jsonify(msg=error_msg), 404
        else:
            return jsonify(msg='College deleted successfully')
