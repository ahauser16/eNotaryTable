"""Feedback Flask app."""

from flask import Flask, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from werkzeug.exceptions import Unauthorized

from models import connect_db, db, User, UserType, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///enotary_db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "count_duckula"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
migrate = Migrate(app, db)
# Flask-Migrate will handle the creation and management of your database schema.
# Now, you can use the command line to manage your database. First, initialize your migration repository with the terminal command: 'flask db init'.  Then, whenever you make changes to your models, generate a migration script with the command: 'flask db migrate'. Finally, apply the changes to your database with: `flask db upgrade`.




# This is the homepage route. When a user navigates to the root URL of your application, they are immediately redirected to the /register route. This route does not render a template. It simply redirects the user to the register route. 
@app.route("/")
def homepage():
    """Homepage of site; redirect to register."""

    return redirect("/register")

# This route handles user registration. If a user is already logged in (i.e., their username is stored in the session), they are redirected to their user page. If the user is not logged in and submits the registration form with valid data, a new user is registered, their username is stored in the session, and they are redirected to their user page. If the user submits invalid data, the registration form is re-rendered with error messages. 
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a user: produce form and handle form submission."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    #cont'd from forms.py_refactor One_A: populate the choices for the SelectField in the register view function
    form.user_type_id.choices = [(ut.id, ut.type) for ut in UserType.query.all()]

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        user_type_id = form.user_type_id.data

        user = User.register(username, password, first_name, last_name, email, user_type_id)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("users/register.html", form=form)


# This route handles user login. Similar to the register route, if a user is already logged in, they are redirected to their user page. If the user is not logged in and submits the login form with valid credentials, their username is stored in the session and they are redirected to their user page. If the user submits invalid credentials, they are shown an error message and the login form is re-rendered.   
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)  # <User> or False
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

# This route handles user logout. The user's username is removed from the session and they are redirected to the login page. If a user is not logged in, they are redirected to the login page. This route does not render a template. It simply redirects the user to the login page. 
@app.route("/logout")
def logout():
    """Logout route."""

    session.pop("username")
    return redirect("/login")

# This route displays a user's page. If a user is not logged in or if the username in the URL does not match the username in the session, an Unauthorized error is raised. If the user is logged in and the username in the URL matches the username in the session, the user's information is displayed. A form to delete the user is also displayed. 
@app.route("/users/<username>")
def show_user(username):
    """Example page for logged-in-users."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)


# This route handles the deletion of a user. Similar to the user page route, if a user is not logged in or if the username in the URL does not match the username in the session, an Unauthorized error is raised. If the user is authorized, their record is deleted from the database, their username is removed from the session, and they are redirected to the login page.  
@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


# This route handles the creation of new feedback. The authorization checks are the same as the previous routes. If the user is authorized and submits the feedback form with valid data, a new feedback record is created in the database and the user is redirected to their user page. If the user submits invalid data, the feedback form is re-rendered with error messages. 
@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback/new.html", form=form)


# This route handles the updating of feedback. The authorization checks are similar to the previous routes, but this time the username associated with the feedback must match the username in the session. If the user is authorized and submits the feedback form with valid data, the feedback record is updated in the database and the user is redirected to their user page. If the user submits invalid data, the feedback form is re-rendered with error messages. 
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


# This route handles the deletion of feedback. The authorization checks are the same as the update feedback route. If the user is authorized, the feedback record is deleted from the database and the user is redirected to their user page. 
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
