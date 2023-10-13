from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', username=current_user.username)
    
    return render_template('landing_page.html')
    # return render_template('home.html', username='Devyn')