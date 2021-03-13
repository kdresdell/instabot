from flask_wtf import FlaskForm
from wtforms import ( PasswordField, StringField,BooleanField,DateTimeField,
                      RadioField, SelectField, TextField,TextAreaField,
                      SubmitField )

from wtforms.validators import InputRequired, DataRequired, Length, Email, EqualTo
from wtforms import ValidationError




class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])

    submit = SubmitField('Submit')




class BotForm(FlaskForm):

    insta_user = StringField('Instagram Account',validators=[DataRequired()])
    insta_password = PasswordField('Instagram password', validators=[DataRequired()])

    tags =  StringField('Tags', validators=[DataRequired()])
    comments = StringField('Comments', validators=[DataRequired()])
    location = StringField('Location')
    radius = StringField('Distance / Radius')

    media = SelectField(u'Media type you want to like and comment:',
                        choices=[('both', 'Photo & Video'),('photo','Photo Only'),('video','Video Only')]
                       )

    submit = SubmitField('Create bot',render_kw={"onclick": "move()"})
