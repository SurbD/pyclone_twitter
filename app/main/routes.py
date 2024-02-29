from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from wtforms.validators import url

from app import db
from app.main.forms import PostForm
from app.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return render_template("landing_page.html")

    posts = Post.query.all()
    return render_template("home.html", username=current_user.username, posts=posts)
    # return render_template('home.html', username='Devyn')


@main.route("/new-post", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for("main.home"))
    return render_template(
        "new_post.html", form=form, username=current_user.username, user=current_user
    )
