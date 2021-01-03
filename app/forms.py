from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User, UserEngagement, UserGroup, GroupEngagement, FriendRequest

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class UserSearchForm(FlaskForm):
    text = StringField('Search Query')
    submit = SubmitField('Search')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already used!')

class EditProfileForm(FlaskForm):
    username = StringField('Change Username', validators=[DataRequired()])
    email = StringField('Change Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update Info')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and user != current_user:
            raise ValidationError('Username already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user != current_user:
            raise ValidationError('Email already used!')

class CreateEngagementForm(FlaskForm):
    weekday = StringField('Weekday')
    month = StringField('Month')
    day = StringField('Day')
    time = StringField('Time', validators=[DataRequired()])
    am_pm = StringField('AM/PM')
    description = TextAreaField('Short Description', validators=[Length(min=0, max=128)])
    is_published_mates = BooleanField('Publish to Your Friends')
    is_published_groupies = BooleanField('Publish to Your Groups')
    submit = SubmitField('Create Event')
    update_submit = SubmitField('Update Event')

class CreateGroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_desc = TextAreaField('Group Description', validators=[DataRequired(), Length(min=1, max=128)])
    submit = SubmitField('Create Group')