from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[
        DataRequired(), 
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message="Invalid email address")
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PersonalInfoForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    dob = DateField('Date of Birth', validators=[DataRequired()], format='%Y-%m-%d')
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(max=20)])
    emergency_contact_name = StringField('Emergency Contact Name', validators=[DataRequired(), Length(max=100)])
    emergency_contact_phone = StringField('Emergency Contact Phone', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Save')
