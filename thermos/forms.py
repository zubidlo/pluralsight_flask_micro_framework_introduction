"""
flask_wtf forms
"""
from models import User
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, url, Length, Regexp, EqualTo, Email, ValidationError

class BookmarkForm(FlaskForm):
    """
    bookmark form
    """
    url = URLField('The URL for your bookmark',
    validators=[DataRequired(), url()])
    description = StringField('Add an optional description')
    tags = StringField('Tags', validators=[Regexp(r'^[a-zA-z0-9, ]*$',
                       message='Tags can only be letters and numbers')])

    def validate(self):
        """
        custom validator modifies form before validation
        """
        if not (self.url.data.startswith("http://") or
        self.url.data.startswith("https://")):
            self.url.data = "http://" + self.url.data

        if not self.description.data:
            self.description.data = self.url.data

        # filter out empty and dubplicate tags
        stripped = [t.strip() for t in self.tags.data.split(',')]
        not_empty = [tag for tag in stripped if tag]
        tagset = set(not_empty)
        self.tags.data = ','.join(tagset)

        return True if FlaskForm.validate(self) else False
