from flask import (Blueprint, render_template, flash,
                    redirect, url_for, session, request, jsonify)

from app.auth.forms import (RegistrationForm, LoginForm,
                             LoginEmailForm, LoginPasswordForm)
from app import bcrypt, db
from app.models import User
from app.utils import get_vcode, confirm_vcode, send_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form_email = LoginEmailForm()
    form_password = LoginPasswordForm()

    # You don't need to use Two forms just use Javascript for 
    # validation form shifting, change it after you confirm the Db is working
    
    next = False
    email_data = None

    if form_email.validate_on_submit():
        user = User.query.filter_by(email=form_email.email.data).first()
        if user:
            session['email_data'] = form_email.email.label(), form_email.email.data
            # session['login_user'] = user

            session['next'] = True
            session['count'] = 1
            return redirect(url_for('auth.login'))
        else:
            flash('Sorry, we could not find your account', 'danger')
            return redirect(url_for('auth.login'))
        
    elif form_password.validate_on_submit():
        email = session['email_data'][1]
        # user = session['login_user']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, form_password.password.data):
            flash('Login Successful', 'success')
            return redirect(url_for('main.index'))
        else:
            session['count'] = 1
            flash('Invalid Password!', 'danger')
            return redirect(url_for('auth.login'))

    elif request.method == "GET":
        email_data = session.get('email_data')
        next = True
        if (count :=session.get('count')) and count == 1:
            next = session.get('next')
            session['count'] += 1
        else:
            next = False

    return render_template(\
        'landing_page.html', title="Sign in", form=form_email,
        next=next, email_data=email_data, form_password=form_password, popup=True)


@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # form.name.data = "Devyn44"
    # print('REGGY')
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.name.data, 
                    email=form.email.data, password=hashed_password, 
                    date_of_birth=form.date_of_birth.data, confirmed=True)
         
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        # print('Form Validated Successfully')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form, title='Register', items=[form, 'valid'])


# Routes API call from Axios

@auth.route("/validate-email", methods=['POST'])
def validate_email():
    # For Javascript email validation

    if request.method == 'POST':
        email = request.get_json()['email']
        user = User.query.filter_by(email=email).first() # SetUp DB
        if user:
            return jsonify({'user_exists': True})
        else:
            return jsonify({'user_exists': False})
 
    return

@auth.route("/validate-inputs", methods=["POST"])
def validate_inputs():
    form = RegistrationForm()

    if request.method == "POST":
        form_data = request.get_json()
        # print(form_data)
        form.name.data = form_data['name']
        form.email.data = form_data['email']
        form.date_of_birth.data = form_data['date_of_birth']

        email_validate = form.email.validate(form) and form.validate_email(form.email)
        name_validate = form.name.validate(form)
        dob_validate = form.date_of_birth.validate(form)
        isAllValid = email_validate and name_validate and dob_validate

        return jsonify({
            'isValid': isAllValid,
            'data': {
                'email': {
                    'isvalid': email_validate,
                    'message': None
                },
                'name': {
                    'isValid': name_validate,
                    'message': None
                },
                'date_of_birth': {
                    'isValid': dob_validate,
                    'message': None
                }
            }
        })

    return


@auth.route('/get-verification-code', methods=['POST'])
def get_verification_code():
    
    if request.method == 'POST':
        user_data = request.get_json()
        email = user_data['email']
        name = user_data['name']

        token, code = get_vcode().values()
        session['verification_token'] = token

        try:
            send_email(email, 'Confirm Email Address',
                        'email/confirm_new_user', code=code, name=name)
        except Exception as e:
            print(e)
            print('ENAD-------------')
            success = False
        else:
            success = True
        return {
            'success': success,
            'token': token
        }

@auth.route('/confirm-verification-code', methods=['POST'])
def confirm_verification_code():
    # I don't know if i should pass token as a parameter from the request 
    # or send as json or to even just store the token in session and 
    # retrive and clear it once it has been confirmed
    
    token = session['verification_token']

    if request.method == 'POST':
        code = request.get_json()['code']

        if confirm_vcode(token, code):
            session.pop('verification_token')
            message = 'Successfully verified your email'
            verified = True
        else: 
            message = 'Check email for verification or try requesting a new code'
            verified = False

        return {'verified': verified, 'message': message} 
