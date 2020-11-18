from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField, StringField
from wtforms.validators import DataRequired


class FixedForm(FlaskForm):
    mortgage = IntegerField(
        'Mortgage value',
        validators=[DataRequired()]
    )
    interest = FloatField(
        'Interest',
        validators=[
            DataRequired()
        ]
    )
    period = IntegerField(
        'For how long is mortgage?',
        validators=[
            DataRequired()
        ]
    )
    overpayment_month = StringField(
        'overpayment month'
    )
    overpayment_month_range = StringField(
        'overpayment month range'
    )
    overpayment_value = IntegerField(
        'overpayment value'
    )
    submit = SubmitField('Submit')