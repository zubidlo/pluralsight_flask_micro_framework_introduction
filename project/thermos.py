"""
flask app
"""
import os
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from forms import BookmarkForm
from sqlalchemy import desc

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x93\x94!q\xdeV\xdcb\x93-\x81$@\xe2S\xd0\xa2\xbdw\xd9\xe6m$%'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


# models
class Bookmark(db.Model):
    """
    Bookmark ORM model
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def newest(num):
        """
        latest num bookmarks
        """
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    def __repr__(self):
        return "'{}': '{}'".format(self.description, self.url)


class User(db.Model):
    """
    User ORM model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    def __repr__(self):
        return "{}".format(self.username)


def logged_in_user():
    return User.query.filter_by(username='zubidlo').first()

@app.route('/')
@app.route('/index')
def index():
    """
    index.html template
    """
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    add.html template
    """
    form = BookmarkForm()

    if form.validate_on_submit():
        url, description = form.url.data, form.description.data
        bm = Bookmark(user=logged_in_user(), url=url, description=description)
        db.session.add(bm)
        db.session.commit()
        flash("Stored bookmark '{}'".format(description))
        return redirect(url_for('index'))

    print form
    return render_template('add.html', form=form)

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

if __name__ == '__main__':
    app.run(debug=False)
