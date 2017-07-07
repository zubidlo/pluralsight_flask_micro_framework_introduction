"""
forms
"""
from ..models import User
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError

class LoginForm(FlaskForm):
    """
    login form
    """
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(FlaskForm):
    """
    sign up form
    """
    username = StringField('Username',
        validators=[
            DataRequired(),
            Length(3, 80),
            Regexp('^[A-Za-z0-9_]{3,}$',
                message='Usernames consists of numbers, '
                        'letters and underscores.')
        ])
    password = PasswordField('Password',
            validators=[
                DataRequired(),
                EqualTo('password2', message='Passwords must match.')
            ]
        )
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[
                                    DataRequired(),
                                    Length(1, 120),
                                    Email()
                                ])

    def validate_email(self, email_field):
        """
        custom email validation
        """
        if User.get_by_email(email_field.data):
            raise ValidationError('There already is user '
                                'with this email address.')

    def validate_username(self, username_field):
        """
        custom username validation
        """
        if User.get_by_username(username_field.data):
            raise ValidationError('Username is already taken.')