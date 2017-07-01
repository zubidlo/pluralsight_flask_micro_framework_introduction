"""
ORM models
"""
from thermos import db
from datetime import datetime
from sqlalchemy import desc
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

tags = db.Table('bookmark_tag',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('bookmark_id', db.Integer, db.ForeignKey('bookmark.id'))
)

class Bookmark(db.Model):
    """
    Bookmark ORM model
    """
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship('Tag', secondary=tags, 
                            backref=db.backref('bookmarks', lazy='dynamic'))

    @staticmethod
    def newest(num):
        """
        latest num bookmarks
        """
        return Bookmark.query.order_by(desc(Bookmark.date)).limit(num)

    @property
    def tags(self):
        """
        tags
        """
        return ','.join(t.name for t in self._tags)

    @tags.setter
    def tags(self, string):
        """
        tags setter
        """
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(',')]

    def __repr__(self):
        return "'{}': '{}'".format(self.description, self.url)


class User(db.Model, UserMixin):
    """
    User ORM model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String)

    @property
    def password(self):
        """
        getter not implemented
        """
        raise AttributeError('password: write-only filed')

    @password.setter
    def password(self, password):
        """
        password setter
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        check password
        """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        """
        get by username
        """
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_id(userid):
        """
        get by id
        """
        return User.query.get(int(userid))

    @staticmethod
    def get_by_email(email):
        """
        get by email
        """
        return User.query.filter_by(email=email).first()

    def __repr__(self):
        return "{}".format(self.username)


class Tag(db.Model):
    """
    tag model
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)

    @staticmethod
    def get_or_create(name):
        """
        get or create tag
        """
        try:
            return Tag.query.filter_by(name=name).one()
        except:
            return Tag(name=name)

    @staticmethod
    def all():
        """
        all tags
        """
        return Tag.query.all()

    def __repr__(self):
        return self.name
