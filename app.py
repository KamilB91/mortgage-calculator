from flask import Flask, url_for, render_template
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
        mortgage_remaining = form.mortgage.data
        interest = form.interest.data*0.01  # b
        period_years = form.period.data
        installments_months = period_years * 12  # n
        overpayment = 0

        mortgage_details = []

        if form.mortgage_type.data == 'fixed':
            q = 1 + (interest / 12)  # q
            installment_value = mortgage*(q**installments_months)*(q-1)/((q**installments_months)-1)  # R
            total_cost = installment_value*installments_months  # C
            if form.option.data == 'short':
                for i in range(1, installments_months+1):
                    interest_value = mortgage_remaining * interest / 12
                    principal = installment_value - interest_value
                    if form.overpayment_end.data != 0:
                        if i in range(int(form.overpayment_start.data), int(form.overpayment_end.data)+1):
                            overpayment = form.overpayment_value.data
                            mortgage_remaining -= overpayment
                        else:
                            overpayment = 0
                    elif i == form.overpayment_start.data:
                        overpayment = form.overpayment_value.data
                        mortgage_remaining -= overpayment
                    else:
                        overpayment = 0

                    if mortgage_remaining <= 0:
                        mortgage_remaining = 0
                        installment_value = 0
                        principal = 0
                        interest_value = 0
                    elif mortgage_remaining < installment_value:
                        interest_value = mortgage_remaining * interest / 12
                        installment_value = mortgage_remaining + interest_value
                        principal = installment_value - interest_value
                        mortgage_remaining -= principal
                    else:
                        mortgage_remaining -= principal

                    mortgage_details.append(dict(month=i, installment_value=round(installment_value, 2), principal=round(principal, 2),
                                                 interest_value=round(interest_value, 2), remaining_mortgage=round(mortgage_remaining, 2),
                                                 overpayment=overpayment))
                return render_template('fixed_mortgage.html', table=table(mortgage_details))
            elif form.option.data == 'lower':
                remaining_months = installments_months
                for i in range(1, installments_months+1):
                    interest_value = mortgage_remaining * interest / 12
                    principal = installment_value - interest_value
                    if form.overpayment_end.data != 0:
                        if i in range(int(form.overpayment_start.data), int(form.overpayment_end.data)+1):
                            overpayment = form.overpayment_value.data
                            mortgage_remaining -= overpayment
                        else:
                            overpayment = 0
                    elif i == form.overpayment_start.data:
                        overpayment = form.overpayment_value.data
                        mortgage_remaining -= overpayment
                    else:
                        overpayment = 0

                    remaining_months -= 1

                    if mortgage_remaining <= 0:
                        mortgage_remaining = 0
                        installment_value = 0
                        principal = 0
                        interest_value = 0
                    elif mortgage_remaining < installment_value:
                        interest_value = mortgage_remaining * interest / 12
                        installment_value = mortgage_remaining + interest_value
                        principal = installment_value - interest_value
                        mortgage_remaining -= principal
                    else:
                        mortgage_remaining -= principal

                    mortgage_details.append(dict(month=i, installment_value=round(installment_value, 2), principal=round(principal, 2),
                                                 interest_value=round(interest_value, 2), remaining_mortgage=round(mortgage_remaining, 2),
                                                 overpayment=overpayment))
                    if remaining_months > 0:
                        installment_value = mortgage_remaining * (q ** remaining_months) * (q - 1) / ((q ** remaining_months) - 1)
                return render_template('fixed_mortgage.html', table=table(mortgage_details))

        elif form.mortgage_type.data == 'variable':
            principal = mortgage / installments_months  # principal
            if form.option.data == 'short':
                for i in range(1, installments_months+1):
                    if form.overpayment_end.data != 0:
                        if i in range(int(form.overpayment_start.data), int(form.overpayment_end.data)+1):
                            overpayment = form.overpayment_value.data
                            mortgage_remaining -= overpayment
                        else:
                            overpayment = 0
                    elif i == form.overpayment_start.data:
                        overpayment = form.overpayment_value.data
                        mortgage_remaining -= overpayment
                    else:
                        overpayment = 0

                    interest_value = (mortgage_remaining * interest) / 12  # interest
                    installment = principal + interest_value
                    if mortgage_remaining < 0:
                        mortgage_remaining = 0
                        installment = 0
                        principal = 0
                        interest_value = 0
                    elif mortgage_remaining < installment:
                        interest_value = mortgage_remaining * interest / 12
                        installment = mortgage_remaining + interest_value
                        principal = installment - interest_value
                        mortgage_remaining -= principal
                    else:
                        mortgage_remaining -= principal
                    mortgage_details.append(dict(month=i, installment_value=round(installment, 2), principal=round(principal, 2),
                                                 interest_value=round(interest_value, 2), remaining_mortgage=round(mortgage_remaining, 2),
                                                 overpayment=overpayment))
                return render_template('fixed_mortgage.html', table=table(mortgage_details))
            elif form.option.data == 'lower':
                remaining_months = installments_months
                for i in range(1, installments_months+1):
                    if form.overpayment_end.data != 0:
                        if i in range(int(form.overpayment_start.data), int(form.overpayment_end.data)+1):
                            overpayment = form.overpayment_value.data
                            mortgage_remaining -= overpayment
                            principal = mortgage_remaining / remaining_months
                        else:
                            overpayment = 0
                    elif i == form.overpayment_start.data:
                        overpayment = form.overpayment_value.data
                        mortgage_remaining -= overpayment
                    else:
                        overpayment = 0
                    interest_value = (mortgage_remaining * interest) / 12  # interest
                    installment = principal + interest_value
                    if mortgage_remaining < 0:
                        mortgage_remaining = 0
                        installment = 0
                        principal = 0
                        interest_value = 0
                    elif mortgage_remaining < installment:
                        interest_value = mortgage_remaining * interest / 12
                        installment = mortgage_remaining + interest_value
                        principal = installment - interest_value
                        mortgage_remaining -= principal
                    else:
                        mortgage_remaining -= principal
                    remaining_months -= 1
                    mortgage_details.append(
                        dict(month=i, installment_value=round(installment, 2), principal=round(principal, 2),
                             interest_value=round(interest_value, 2), remaining_mortgage=round(mortgage_remaining, 2),
                             overpayment=overpayment))
                    if remaining_months > 0:
                        principal = mortgage_remaining / remaining_months
                return render_template('fixed_mortgage.html', table=table(mortgage_details))

    return render_template('fixed_form.html', form=form)


if __name__ == '__main__':
    app.run()  # host="192.168.0.206"
