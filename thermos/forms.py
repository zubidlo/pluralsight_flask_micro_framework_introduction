"""
flask_wtf forms
"""
from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url

class BookmarkForm(FlaskForm):
    """
    bookmark form
    """
    url = URLField('The URL for your bookmark',
    validators=[DataRequired(), url()])
    description = StringField('Add an optional description')

    def validate(self):
        """
        custom validator modifies form before validation
        """
        if not (self.url.data.startswith("http://") or
        self.url.data.startswith("https://")):
            self.url.data = "http://" + self.url.data

        if not self.description.data:
            self.description.data = self.url.data

        return True if FlaskForm.validate(self) else False
            