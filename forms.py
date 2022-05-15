from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, InputRequired, EqualTo


class AddUserForm(FlaskForm):
    '''Form to create a new user'''

    first_name = StringField('First Name', validators=[InputRequired(message='Requires a first name')])
    last_name = StringField('Last Name', validators=[InputRequired(message='Requires a last name')])
    email = StringField('Email', validators=[InputRequired(message='Email required'), Length(max=30)])
    username = StringField('Username', validators=[InputRequired(message='Enter username')])
    password = PasswordField('Password', [InputRequired(), Length(min=8, max=20), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class LoginForm(FlaskForm):
    '''Form to login existing user to app'''

    username = StringField('Username', validators=[InputRequired(message='Username required')])
    password = PasswordField('Password', validators= [InputRequired(message='Invalid Password')])


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
