from flask_table import Table, Col


class FixedTable(Table):
    month = Col('Month')
    installment_value = Col('Installment')
    interest_value = Col('Interest Value')
    principal = Col('Principal')
    remaining_mortgage = Col('Remaining')
    overpayment = Col('Overpayment')
