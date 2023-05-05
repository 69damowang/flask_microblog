from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
#表单

#用户输入区
from app.models import User

#登录表单
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#用户注册表单
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators = [DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register') #注册按钮

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

        def validate_email(self,email):
            user = User.query.filiter_by(email = email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email address.')


#签名表单
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()]) #修改自己昵称
    about_me = TextAreaField('About_me', validators=[Length(min=0, max=140)])#文本输入框
    submit = SubmitField('Submit')







