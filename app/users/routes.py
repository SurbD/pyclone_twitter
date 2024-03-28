from flask import Blueprint, render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required

from app.models import User, Post

users = Blueprint('users', __name__)

@users.route('/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username.lower()).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all() # finish post on profile page this night
    return render_template('profile.html', username=username, user=user, posts=posts)

@users.route('/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username.lower()).first()
    if current_user.username != username:
        return redirect(url_for( 'users.profile', username=username))
    return render_template('edit_profile.html', username=username, user=user)