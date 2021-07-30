__author__ = "Koffi Cobbin"
import uuid
from pdhs_app.common.database import Database
from pdhs_app.common.utils import Utils
import pdhs_app.models.users.errors as UserErrors
import pdhs_app.models.users.constants as UserConstants
# from config import users


class User(object):
    def __init__(self, user_id, first_name, last_name, email, password, department_name, profile_image_link=None):
        self.user_id = user_id                  # INT PRIMARY KEY
        self.first_name = first_name            # VARCHAR(50) NOT NULL
        self.last_name = last_name              # VARCHAR(50) NOT NULL
        self.email = email                      # VARCHAR(50) NOT NULL
        self.password = password                # VARCHAR(20) NOT NULL
        self.portfolio = portfolio              # VARCHAR(50) NOT NULL
        # VARCHAR(50) FOREIGN KEY REFERENCES department(department_name)
        self.department_name = department_name
        self.profile_image_link = None if profile_image_link is None else profile_image_link

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(user_id, password):
        """
        This method verifies that an user_id/password combo (As sent by the site forms) is valid or not.
        Checks that the user exists and that the password associated to the user is correct.
        :param user_id: The user's ID (ie. student ID or staff ID)
        :param password: A sha512 hashed password
        :return: True if valid, False if otherwise.
        """
        # result = Database.select_from_where("*", "users", f"user_id='{user_id}'")
        # user_data, *_ = result
        for user in users:
            if (user["user_id"] == user_id) and (user["password"] == password):
                user_data = user
            else:
                user_data = None
        if user_data is None:
            # Tell the user their user_id does'nt exist
            raise UserErrors.UserDontExistError("User does'nt exist ):")
        # if not Utils.check_hashed_password(password, user_data['password']):
        #     # Tell the user that their password is wrong
        #     raise UserErrors.IncorrectPasswordError("Invalid Password ):")
        return True

    @staticmethod
    def register_user(user_id, first_name, last_name, email, password, portfolio, department_name):
        """
        This registers a user using user_id, first_name, last_name, e-mail and password.
        The password already comes hashed as sha-512.
        :param user_id: The user's ID (ie. student ID or staff ID)
        :param email:   user's e-mail (might be invalid)
        :param password:    sha512-hashed password  
        :param portfolio:    the user's position (eg. HOD, Secretary, President etc.)
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        result = Database.select_from_where(
            "*", "users", f"user_id='{user_id}'")
        user_data, *_ = result
        if user_data:
            # Tell user they already exist
            raise UserErrors.UserAlreadyRegisteredError("User already exists.")
        if not Utils.email_is_valid(email):
            # Tell user that their e-mail is not constructed properly.
            raise UserErrors.InvalidEmailError(
                "The email does not have the right format.")
        data = [
            user_id,
            first_name,
            last_name,
            email,
            password,
            portfolio,
            department_name
        ]
        Database.insert("user", data)
        return True

    @staticmethod
    def delete(user_id):
        val = Database.delete("user", f"user_id='{user_id}'")
        return val

    def user_alerts(self):
        return None
