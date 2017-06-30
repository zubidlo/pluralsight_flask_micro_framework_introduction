"""
Views
"""
from flask import render_template, flash, redirect, url_for, request, abort
from thermos import app, db, login_manager
from forms import BookmarkForm, LoginForm, SignupForm
from models import User, Bookmark
from flask_login import login_required, login_user, logout_user, current_user


@login_manager.user_loader
def load_user(userid):
    """
    user loader
    """
    return User.get_by_id(userid)

@app.route('/')
@app.route('/index')
def index():
    """
    index page
    """
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    add bookmark view
    """
    form = BookmarkForm()
    if form.validate_on_submit():
        url, description = form.url.data, form.description.data
        bm = Bookmark(user=current_user, url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))
    return render_template('add.html', form=form)

@app.route('/edit/<int:bookmark_id>', methods=['GET', 'POST'])
@login_required
def edit_bookmark(bookmark_id):
    """
    edit bookmark view
    """
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    if current_user != bookmark.user:
        abort(403)
    form = BookmarkForm(obj=bookmark)
    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Stored '{}'".format(bookmark.description))
        return redirect(url_for('user', username=current_user.username))
    return render_template('bookmark_form.html', form=form, title='Edit bookmark')

@app.route('/user/<username>')
def user(username):
    """
    user bookmarks view
    """
    user = User.get_by_username(username)
    if user:
        return render_template('user.html', user=user)
    abort(404)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    login view
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Logged in successfully as {}.'.format(user.username))
            return redirect(request.args.get('next')
            or url_for('user', username=user.username))
        flash('Incorrect username or password.')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """
    logout view
    """
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    sign up view
    """
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    email=form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('Welcome, {}! Please login.'.format(user.username))
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    """
    Custom 404 response
    """
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """
    Custom 500 response
    """
    return render_template('500.html'), 500
