from flask import Blueprint, render_template, flash, redirect, url_for

from app.auth.forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash('A confirmation email has been sent to your email', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form, title='Register')