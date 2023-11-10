from flask import (Blueprint, render_template, flash,
                    redirect, url_for, session, request)
from flask_login import current_user, login_user, logout_user, login_required

from datetime import timedelta

from app.auth.forms import (RegistrationForm, LoginEmailForm, 
                            LoginPasswordForm, RequestResetForm, ResetPasswordForm)
from app import bcrypt, db
from app.utils import send_email
from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form_email = LoginEmailForm()
    form_password = LoginPasswordForm()

    # You don't need to use Two forms just use Javascript for 
    # validation form shifting, change it after you confirm the Db is working
    
    next = False
    email_data = None

    if form_email.validate_on_submit():
        user = User.query.filter_by(email=form_email.email.data.lower()).first()
        if user:
            session['email_data'] = form_email.email.label(), form_email.email.data.lower()

            session['next'] = True
            session['count'] = 1
            return redirect(url_for('auth.login'))
        else:
            flash('Sorry, we could not find your account', 'danger')
            return redirect(url_for('auth.login'))
        
    elif form_password.validate_on_submit():
        email = session['email_data'][1]
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, form_password.password.data):
            login_user(user, remember=True, duration=timedelta(days=1))
            next_page = request.args.get('next')

            if next_page == '/logout':
                next_page = None
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            session['count'] = 1
            flash('Please check password and try again or reset your password.', 'danger')
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
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
  
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), 
                    email=form.email.data.lower(), password=hashed_password, 
                    date_of_birth=form.date_of_birth.data, confirmed=True)
         
        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form, title='Register', items=[form, 'valid'])


@auth.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('auth.login'))
    return render_template('logout.html')

# Style the templates of the reset pasword link that of registration so inherit from it or duplicate it

@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_token()
        send_email(user.email, 'Password Reset', 
                   'email/reset_password', token=token, user=user)
        flash('An email has been sent to you with instructions to reset your password.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_request.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.confirm_token(token)
    if not user:
        flash('That is an Invalid or expired token!, request for another token', 'danger')
        return redirect(url_for('auth.reset_request'))
    
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        db.session.commit()
        flash('Your password has been successfully updated. You are now able to login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', form=form)