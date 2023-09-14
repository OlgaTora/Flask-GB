from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from Home_3.registration_module.BirthdayValidator import BirthdayValidator


class RegisterForm(FlaskForm):
    username = StringField("name", validators=[DataRequired()])
    surname = StringField("surname", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    birthday = DateField(
        "birthday", format="%Y-%m-%d", validators=[DataRequired(), BirthdayValidator()]
    )
    password = PasswordField(
        "password",
        validators=[
            DataRequired(),
            Length(min=8),
            Regexp(r".*[a-zA-Z].*", message="Password must contain minimum 1 letter"),
            Regexp(r".*[0-9].*", message="Password must contain minimum 1 number"),
        ],
    )
    confirm_password = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )
    confirm = BooleanField(
        "Please, confirm processing of personal data", validators=[DataRequired()]
    )


class LoginForm(FlaskForm):
    username = StringField("name", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
