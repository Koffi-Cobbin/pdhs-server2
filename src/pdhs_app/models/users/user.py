from src.database.db import db
from src.middleware.utils import Utils
import src.pdhs_app.models.users.errors as UserErrors
from src.pdhs_app.models.faculties.faculty import Faculty
from src.pdhs_app.models.colleges.college import College

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    
    college = db.relationship("College", lazy='select', backref=db.backref('user', lazy='joined'))
    faculty = db.relationship("Faculty", lazy='select', backref=db.backref('user', lazy='joined'))
    documents = db.relationship("Document", lazy='select', backref=db.backref('user', lazy='joined'))
    comments = db.relationship("Comment", lazy='select', backref=db.backref('user', lazy='joined'))
    approvals = db.relationship("Approval", lazy='select', backref=db.backref('recipient', lazy='joined'))
    tokens = db.relationship('TokenBlocklist', lazy='select', backref=db.backref('user', lazy='joined'))
    

    def __repr__(self):
        return '<User %r>' % self.id

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
         department = self.department.to_json()
         faculty = Faculty.find_by_id(department['faculty_id']).to_json()
         college = College.find_by_id(faculty['college_id']).to_json()
         return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'portfolio': self.portfolio.to_json()['name'],
            'department_id': self.department_id,
            'college_id': college['id']
         }

    @staticmethod
    def is_login_valid(user_id, password):
        """
        This method verifies that an user_id/password combo (As sent by the site forms) is valid or not.
        Checks that the user exists and that the password associated to the user is correct.
        :param user_id: The user's ID (ie. student ID or staff ID)
        :param password: A sha512 hashed password
        :return: True if valid, False if otherwise.
        """
        # checking if user actually exists
        try:
            user = User.query.filter_by(user_id=user_id).first()
        except:
            user = None
        if user:
            if not Utils.check_hashed_password(password, user.password):
                # Tell the user that their password is wrong
                raise UserErrors.IncorrectPasswordError("Invalid Password")
        else:
            # Tell the user their user_id does'nt exist
            raise UserErrors.UserDontExistError("User does'nt exist")
        return user

    @staticmethod
    def register_user(user_id, first_name, last_name, email, password, portfolio_id, department_id):
        """
        This registers a user using user_id, first_name, last_name, e-mail and password.
        :param user_id: The user's ID (ie. student ID or staff ID)
        :param email:   user's e-mail (might be invalid)
        :param password:    sha256-hashed password  
        :param portfolio:    the user's position (eg. HOD, Secretary, President etc.) as an int
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        # checking if user actually exists
        try:
            user = User.query.filter_by(user_id=user_id).first()
        except:
            user = None
        if user:
            # Tell user they already exist
            raise UserErrors.UserAlreadyRegisteredError("User already exists.")

        # add the new user to the database
        new_user = User(user_id, first_name, last_name, email,
                        password, portfolio_id, department_id).save_to_db()
        return True

    
