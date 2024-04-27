"""Forms for flask-feedback."""

from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

from models import UserType


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )


class RegisterForm(FlaskForm):
    """User registration form."""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=20)],
    )
    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6, max=55)],
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)],
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)],
    )
    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)],
    )
    user_type_id = SelectField(
        "User Type",
        coerce=int,
        choices=[],
        # choices=[(ut.id, ut.type) for ut in UserType.query.all()],
    )
    # refactor One_A: The error message RuntimeError: Working outside of application context. is occurring because you're trying to query the database outside of an application context.  In your forms.py file, you're trying to populate the choices for a SelectField with all instances of UserType from the database. This requires an application context because it involves a database operation.  However, when the forms.py file is imported, Flask hasn't fully set up the application context yet, so the database operation fails.
    # To fix this, you can delay the database operation until an application context is available. You can do this by populating the choices for the SelectField in the view function, not in the form class.  To fix this in your forms.py file, change the `SelectField` in the `RegisterForm` class to not include any choices initially.  Then in your `app.py` file...


class FeedbackForm(FlaskForm):
    """Add feedback form."""

    title = StringField(
        "Title",
        validators=[InputRequired(), Length(max=100)],
    )
    content = StringField(
        "Content",
        validators=[InputRequired()],
    )


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
