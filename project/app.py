"""
flask app
"""
from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import BookmarkForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x93\x94!q\xdeV\xdcb\x93-\x81$@\xe2S\xd0\xa2\xbdw\xd9\xe6m$%'

bookmarks = []

def store_booksmark(url, description):
    """
    stores bookmark to global list bookmarks
    """
    bookmarks.append(dict(
        url=url,
        description=description,
        user="martin",
        date=datetime.utcnow()
    ))

def new_bookmarks(num):
    """
    returns last num bookmarks
    """
    return sorted(bookmarks, key=lambda bm: bm['date'], reverse=True)[:num]

@app.route('/')
@app.route('/index')
def index():
    """
    index.html template
    """
    return render_template('index.html', new_bookmarks=new_bookmarks(5))

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    add.html template
    """
    form = BookmarkForm()

    if form.validate_on_submit():
        url, description = form.url.data, form.description.data
        store_booksmark(url, description)
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
