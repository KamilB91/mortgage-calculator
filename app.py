from flask import Flask, render_template
import forms
import tables


app = Flask(__name__)
app.secret_key = 'wejbg98jc3nrkfo8OJREJ9UHJO*Oi8jejf88YT^R52o(*U2'


@app.route('/', methods=['GET', 'POST'])
def fixed():
    form = forms.FixedForm()
    table = tables.FixedTable

    if form.validate_on_submit():
        mortgage = form.mortgage.data  # A
        interest = form.interest.data*0.01  # b
        remaining_period = form.period.data * 12
        period = form.period.data * 12
        overpayment_start = form.overpayment_start.data
        overpayment_end = form.overpayment_end.data
        overpayment_value = 0
        principal = 0
        installment = 0
        outcome_list = []
        initial_installment = 0

        q = 1 + (interest / 12)
        remaining_mortgage = form.mortgage.data
        interest_value = mortgage * interest / 12
        mortgage_details = []

        for i in range(remaining_period+1):
            if i == 0:
                installment = 0
                principal = 0
                remaining_period += 1
            else:
                if form.mortgage_type.data == 'fixed':
                    installment = remaining_mortgage * (q ** remaining_period) * (q - 1) / ((q ** remaining_period) - 1)
                    interest_value = remaining_mortgage * interest / 12
                    principal = installment - interest_value
                    if i == 1:
                        initial_installment = installment
                    if form.option.data == 'short':
                        installment = mortgage * (q ** period) * (q - 1) / ((q ** period) - 1)
                        principal = installment - interest_value
                        if i == 1:
                            initial_installment = installment
                elif form.mortgage_type.data == 'variable':
                    principal = remaining_mortgage/remaining_period
                    interest_value = remaining_mortgage * interest / 12
                    installment = principal+interest_value
                    if i == 1:
                        initial_installment = installment
                    if form.option.data == 'short':
                        principal = mortgage/period
                        installment = principal + interest_value
                        if i == 1:
                            initial_installment = installment
                outcome_list.append(installment)
                if i == int(overpayment_start):
                    overpayment_value = form.overpayment_value.data
                elif i in range(int(overpayment_start), int(overpayment_end)+1):
                    overpayment_value = form.overpayment_value.data
                    if form.ascending_overpayment.data:
                        overpayment_value = overpayment_value + (initial_installment-outcome_list[-1])
                        print(outcome_list[-2], installment, (outcome_list[-2] - installment))
                else:
                    overpayment_value = 0

                if remaining_mortgage <= 0:
                    remaining_mortgage = 0
                    installment = 0
                    principal = 0
                    interest_value = 0
                elif principal > remaining_mortgage:
                    installment = remaining_mortgage + interest_value
                    principal = remaining_mortgage

                remaining_mortgage -= (principal+overpayment_value)

            mortgage_details.append(dict(month=i,
                                         installment_value=round(installment, 2),
                                         principal=round(principal, 2),
                                         interest_value=round(interest_value, 2),
                                         remaining_mortgage=round(remaining_mortgage, 2),
                                         overpayment=round(overpayment_value, 2))
                                    )
            remaining_period -= 1
        return render_template('fixed_mortgage.html', table=table(mortgage_details))
    return render_template('fixed_form.html', form=form)


if __name__ == '__main__':
    app.run(threaded=True)
