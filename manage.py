#! /usr/bin/env python
"""
databese manager script
"""
from thermos import db, app
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def insert_data():
    """
    creates database
    """
    db.create_all()
    zubidlo = User(username='zubidlo', email='zubidlo@gmail.com', password="password")
    db.session.add(zubidlo)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description, user=zubidlo, tags=tags))

    for name in ['python', 'flask', 'programming']:
        db.session.add(Tag(name=name))

    add_bookmark("http://www.pluralsight.com", "Hardcore development traininng.", "programming")
    add_bookmark("http://www.python.org", "My favourite language", "python")
    add_bookmark("http://www.flask.pocaa.org", "Web development", "flask")

    db.session.commit()
    print "inserted the data"

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
