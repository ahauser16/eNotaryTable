"""Models for flask-feedback."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# This line initializes a Bcrypt object. Bcrypt is a password hashing function that you'll use to securely store user passwords.
bcrypt = Bcrypt()

# This line initializes a SQLAlchemy object, which provides the tools to interact with your database using Python code.
db = SQLAlchemy()

# This function connects your Flask application to your database. It's called in your Flask app to connect the database to the app. 
def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


# This class defines the UserType model. Each attribute of the class represents a column in the "user_types" table in your database. The `users` attribute is a relationship that links user types with users. The `backref` argument allows you to access a user type's users with `user_type.users`. 

# FYI, To create the user_types table in a Flask application using SQLAlchemy, you first define the UserType model as you have done. Then, you need to create the table in your database. This is typically done using Flask-Migrate, a Flask extension that handles SQLAlchemy database migrations.
class UserType(db.Model):
    """User type."""

    __tablename__ = "user_types"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False, unique=True)

    users = db.relationship("User", backref="user_type")

# This class defines the User model. Each attribute of the class represents a column in the "users" table in your database. The `feedback` attribute is a relationship that links users with their feedback. The `backref` argument allows you to access a user's feedback with `user.feedback`. The `cascade` argument ensures that when a user is deleted, all of their feedback is also deleted. This is a common practice to ensure that your database remains consistent.  
class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_types.id'))

    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")

    # start of convenience class methods
    # This class method is used to register a new user. It hashes the user's password and creates a new User instance with the provided data. The new user is then added to the database session, which is like a staging area for changes that will be written to the database. 
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email
        )

        db.session.add(user)
        return user

    # This class method is used to authenticate a user. It checks if a user with the provided username exists and if the provided password matches the hashed password stored in the database. If both checks pass, it returns the user; otherwise, it returns False. 
    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

# This class defines the Feedback model. Each attribute of the class represents a column in the "feedback" table in your database. The `username` attribute is a foreign key that links each piece of feedback to a user. This relationship is defined by the `ForeignKey` argument, which specifies the column in the "users" table that the `username` column in the "feedback" table references. 
class Feedback(db.Model):
    """Feedback."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,
    )

# In the context of your routes, these models are used to interact with your database. For example, in the register() route, the User.register() method is used to create a new user. In the login() route, the User.authenticate() method is used to authenticate a user. In the new_feedback() route, a new Feedback instance is created and added to the database session. These models provide a way to interact with your database using Python code.