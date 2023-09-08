from flask import (Blueprint, render_template, flash,
                    redirect, url_for, session, request)

from app.auth.forms import (RegistrationForm, LoginForm,
                             LoginEmailForm, LoginPasswordForm)

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form_email = LoginEmailForm()
    form_password = LoginPasswordForm()
    
    next = False
    email_data = None

    if form_email.validate_on_submit():
        if form_email.email.data == 'admin@blog.com':
            session['email_data'] = form_email.email.label(), form_email.email.data
            session['next'] = True
            session['count'] = 1
            return redirect(url_for('auth.login'))
        else:
            flash('Sorry, we could not find your account', 'danger')
            return redirect(url_for('auth.login'))
        
    elif form_password.validate_on_submit():
        if form_password.password.data == 'password':
            flash("You're Logged In!", 'success')
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
    
    if form.validate_on_submit():
        flash('A confirmation email has been sent to your email', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form, title='Register')