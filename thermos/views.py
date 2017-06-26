"""
Views
"""
from flask import render_template, flash, redirect, url_for

from thermos import app, db
from  forms import BookmarkForm
from models import User, Bookmark


def logged_in_user():
    return User.query.filter_by(username='zubidlo').first()

@app.route('/')
@app.route('/index')
def index():
    """
    index page
    """
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    add bookmark page
    """
    form = BookmarkForm()

    if form.validate_on_submit():
        url, description = form.url.data, form.description.data
        bm = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))

    return render_template('add.html', form=form)

@app.route('/user/<username>')
def user(username):
    """
    user bookmarks page
    """
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

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
