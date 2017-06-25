from flask import Flask, render_template, url_for

app = Flask(__name__)


class User(object):
    """
    User
    """
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname

    def initials(self):
        """
        initials
        """
        return "{}. {}.".format(self.firstname[0], self.lastname[0])

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)

@app.route('/')
@app.route('/index')
def index():
    """
    index.html template
    """
    return render_template('index.html')

@app.route('/add')
def add():
    """
    add.html template
    """
    return render_template('add.html')

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
    app.run(debug=True)
