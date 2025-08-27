from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SubmitField,PasswordField,SelectField
from wtforms.validators import DataRequired, NumberRange ,EqualTo,Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class ExpenseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField(
        'Category',
        choices=[
            ('Food', 'Food'),
            ('Transportation', 'Transportation'),
            ('Clothes', 'Clothes'),
            ('Rent', 'Rent'),
            ('WiFi', 'WiFi'),
            ('Electricity', 'Electricity'),
            ('Water Bill', 'Water Bill'),
            ('Others', 'Others')
        ],
        validators=[DataRequired()]
    )
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', default=1, validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add')
