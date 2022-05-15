from flask import Flask, redirect, render_template, session
from forms import AddUserForm, LoginForm, FeedbackForm
from models import Feedback, db, connect_db, hash_pwd, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///usersprac'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret28*&335@735!&$@'


connect_db(app)
db.create_all()

@app.route('/')
def red_home():
    '''Redirect to registration page'''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user_form():
    '''Display form for user registration. Hash password and store in database'''

    form = AddUserForm()

    if form.validate_on_submit():
        user = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data,
            username = form.username.data,
            password = hash_pwd(form.password.data)
        )
        # save user to the database
        db.session.add(user)
        db.session.commit()
        # store username in cookies for authentication
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template('register.html', form=form)


@app.route('/users/<username>', methods=['GET'])
def display_user_content(username):
    '''If authenticated, display user content'''

    user = User.query.filter_by(username=username).first_or_404()
    session_user = session['username']

    if user and user.username == session_user:
        return render_template('profile.html', user=user)

    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def app_login():
    '''Display form for login'''

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, pwd=form.password.data)

        if user:
            session['username'] = form.username.data

            return redirect(f'/users/{user.username}')
        else:
            return redirect('/login')

    else:
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout_user():
    '''Remove user from session and redirect to home'''
    session.pop('username')

    return redirect('/login')


@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user then redirect to registeration."""

    if username != session['username']:
        session.pop('username')
        return redirect('/logout')

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/register")


@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if username != session['username']:
        session.pop['username']
        return redirect('/login')

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
        return render_template("feedback_form.html", form=form, username=username)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if feedback.username != session['username']:
        session.pop['username']
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if feedback.username != session['username']:
        session.pop['username']
        return redirect('/login')

    else:
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
