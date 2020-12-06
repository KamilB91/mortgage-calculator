from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField, RadioField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


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
        'A month where you do single overpayment or month where you start your multiple overpayments:',
        validators=[Optional()],
        default='0'
    )
    overpayment_end = IntegerField(
        'Last month of your overpayments. If you do overpayment once, leave 0 in this field:',
        validators=[Optional()],
        default='0'
    )
    overpayment_value = IntegerField(
        'Overpayment value',
        validators=[Optional()],
        default=0
    )
    ascending_overpayment = MultiCheckboxField('Ascending overpayments?',
                                               choices=[('Yes', 'Yes')],
                                               validators=[Optional()])
    option = RadioField('How would you like to amend your installments?',
                        choices=[('lower', 'Lower instalments value'), ('short', 'Shorten mortgage period')],
                        default='short')
    mortgage_type = RadioField('Fixed or variable?',
                               choices=[('fixed', 'Fixed'), ('variable', 'Variable')],
                               default='fixed')
    submit = SubmitField('Submit')
