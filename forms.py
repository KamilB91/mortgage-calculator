from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Optional


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
    overpayment_start = IntegerField(
        'Overpayment month',
        validators=[Optional()],
        default='0'
    )
    overpayment_end = IntegerField(
        'Overpayment month range',
        validators=[Optional()],
        default='0'
    )
    overpayment_value = IntegerField(
        'Overpayment value',
        validators=[Optional()],
        default=0
    )
    option = RadioField('How would you like to amend your installments?',
                        choices=[('lower', 'Lower instalments value'), ('short', 'Shorten mortgage period')],
                        default='short')
    mortgage_type = RadioField('Fixed or variable?',
                               choices=[('fixed', 'Fixed'), ('variable', 'Variable')],
                               default='fixed')
    submit = SubmitField('Submit')
