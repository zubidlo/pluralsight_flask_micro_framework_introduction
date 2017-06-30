#! /usr/bin/env python
"""
databese manager script
"""
from thermos import db, app
from thermos.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    """
    creates database
    """
    db.create_all()
    db.session.add(User(username='zubidlo', email='zubidlo@gmail.com', password="password"))
    db.session.add(User(username='tomaszuber', email='tomaszuber@gmail.com', password="password"))
    db.session.commit()
    print "Initialized the database"

@manager.command
def dropdb():
    """
    drops the database
    """
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print "Dropped the database"

if __name__ == "__main__":
    manager.run()
