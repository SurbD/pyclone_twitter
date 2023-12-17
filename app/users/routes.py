from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from app.models import User

users = Blueprint('users', __name__)

@users.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username.lower()).first()

    if user:
        return render_template('profile.html', username=username, user=user)
    return redirect(url_for('auth.login'))

@users.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    print('got here')
    if current_user.username != username:
        return redirect(url_for( 'users.profile', username=username))
    return render_template('edit_profile.html')
