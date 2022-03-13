from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, URL as URLval
import requests
import phonenumbers
from flask_mail import Message, Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MAIL_SERVER'] = "smtp.sendgrid.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = 'secret'
mail = Mail()
mail.init_app(app)


class RegistrationForm(FlaskForm):
    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "E.g. John Doe"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "E.g. you@domain.com"})
    phone = StringField('Phone Number(append with +1)', validators=[DataRequired()], render_kw={"placeholder": "E.g. +12345678901"})
    over18 = BooleanField('I am over the age of 15', validators=[DataRequired()])
    emergencyname = StringField('Emergency Contact Name', validators=[DataRequired(), Length(min=2, max=50)], render_kw={"placeholder": "E.g. Jane Doe"})
    emergencyphone = StringField('Emergency Contact Phone(append with +1)', validators=[DataRequired()], render_kw={"placeholder": "E.g. +12341234567"})
    emergencyemail = StringField('Emergency Contact Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "E.g. someone@domain.com"})
    futureeventscontact = BooleanField('Would you like to be contacted about future events?')
    submit = SubmitField('Register')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
    def validate_emergencyphone(self, emergencyphone):
        try:
            p = phonenumbers.parse(emergencyphone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')
 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/volunteer', methods=["GET", "POST"])
def volunteer():
    form = RegistrationForm()
    if form.validate_on_submit():
        msg = Message(subject="New Volunteer Just Registered!", sender="noreply@eshan.dev", recipients=["LaderaRanchLibrary@gmail.com", "ipolavar@gmail.com"], reply_to=form.email.data)
        msg.html = f"""
        <h1>New Volunteer Just Registered!</h1>
        <h3>Volunteer Details</h3>
        <p><strong>Full Name:</strong> {form.fullname.data}</p>
        <p><strong>Email:</strong> {form.email.data}</p>
        <p><strong>Phone:</strong> {form.phone.data}</p>
        <p><strong>Over 18:</strong> {form.over18.data}</p>
        <p><strong>Emergency Contact Name:</strong> {form.emergencyname.data}</p>
        <p><strong>Emergency Contact Phone:</strong> {form.emergencyphone.data}</p>
        <p><strong>Emergency Contact Email:</strong> {form.emergencyemail.data}</p>
        <p><strong>Would you like to be contacted about future events?:</strong> {form.futureeventscontact.data}</p>
        """
        mail.send(msg)
        flash('Your registration has been submitted! Watch your inbox for more info!', 'success')
        return redirect(url_for('index'))
    return render_template('volunteer.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)