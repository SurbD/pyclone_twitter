from flask import Blueprint, flash, redirect, render_template, url_for, request, current_app, abort
from flask_login import current_user, login_required

from app import db
from app.main.forms import PostForm
from app.models import Post, User

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return render_template("landing_page.html")

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['XCLONE_POSTS_PER_PAGE'], 
        error_out=False)
    posts = pagination.items
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("home.html", username=current_user.username, 
                           posts=posts, pagination=pagination)


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

@main.route("/post/<int:id>/")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post], user=current_user)

@main.route("/delete_post/<int:id>")
def delete_post(id):
    post = Post.query.get_or_404(id)

    if not current_user == post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("users.profile", username=current_user.username))

@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.home'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('users.profile', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}')
    return redirect(url_for('users.profile', username=username))


@main.route('/unfollow/<username>/')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.home'))
    
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('users.profile', username=username))
    
    current_user.unfollow(user)
    db.session.commit()

    flash(f'You are no longer following {username}')
    return redirect(url_for('users.profile', username=username))

@main.route('/followers/<username>')
def followers(username:str):
    # TODO: Test out this route and make sure you understand exactly pagination and followers query works
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page=page, per_page=current_app.config['XCLONE_FOLLOWERS_PER_PAGE'], error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Follower of',
                           endpoint='main.followers', pagination=pagination, follows=follows)

@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash('Invalid user.')
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page=page, per_page=current_app.config['XCLONE_FOLLOWERS_PER_PAGE'], error_out=False)
    
    follows = [{'user': item.followed, 'timestamp': item.timestamp} for item in pagination.items]
    return render_template('followers.html', user=user, title='Followed by', 
                           endpoint='main.followed_by', pagination=pagination, follows=follows)