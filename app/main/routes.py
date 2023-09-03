from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def index():
    return render_template('landing_page.html')