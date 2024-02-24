from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

from app.main.forms import PostForm

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', username=current_user.username)
    
    return render_template('landing_page.html')
    # return render_template('home.html', username='Devyn')

@main.route('/new-post')
@login_required
def new_post():
    form = PostForm()
    
    return render_template('new_post.html', form=form, username=current_user.username, user=current_user)
