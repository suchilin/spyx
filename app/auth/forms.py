from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Regexp


class SignupForm(FlaskForm):
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8,message="Password could be minimum 8 chars"),
        Regexp("[A-Z]", message="Password must contain upercasse letters"),
        Regexp("[0-9]", message="Password must contain numbers"),
        Regexp("[!#$%&()*+,:;<=>?@]", message="Password must contain al least one special char (!#$%&()*+,:;<=>?@)")
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')
