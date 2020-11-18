from flask_table import Table, Col


class FixedTable(Table):
    installment_value = Col('Installment')
    principal = Col('Principal')
    interest_value = Col('Interest Value')
    overpayment = Col('overpayment')
    remaining_mortgage = Col('Remaining')
