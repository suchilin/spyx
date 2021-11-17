from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length
from wtforms.widgets import TextArea

class HitForm(FlaskForm):
    description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
    target = StringField('Target', validators=[DataRequired()])
    assignee = SelectField("Assignee", validators=[DataRequired()])
    submit = SubmitField('Create Hit')
