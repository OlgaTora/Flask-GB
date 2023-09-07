import datetime as dt
from wtforms import ValidationError


class BirthdayValidator:
    """Class for validate birthday year"""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        data = field.data
        if data > dt.datetime.today().date():
            self.message = field.gettext('Date of birth cant be more than today')
            raise ValidationError(self.message)
        if data < dt.datetime(1900, 1, 1).date():
            self.message = field.gettext('Date of birth cant be less than 01-01-1900')
            raise ValidationError(self.message)
