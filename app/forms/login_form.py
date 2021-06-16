from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, validators
from wtforms.validators import Length, Email, InputRequired


class RegistrationForm(FlaskForm):
    email = StringField("Email Address", [Length(min=6, max=30),
                                          Email(message="Not a valid email address.")]
                        )
    password = PasswordField("Password")
    submit = SubmitField("Login")