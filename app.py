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

        q = 1+(interest/12)  # q

        mortgage_details = []
        installment_value = mortgage*(q**installments_months)*(q-1)/((q**installments_months)-1)  # R
        total_cost = installment_value*installments_months  # C
        for i in range(1, installments_months+1):
            interest_value = mortgage_remaining * interest / 12
            principal = installment_value - interest_value
            if form.overpayment_month_range:
                if i in range(int(form.overpayment_month.data), int(form.overpayment_month_range.data)+1):
                    overpayment = form.overpayment_value.data
                    mortgage_remaining -= overpayment
                else:
                    overpayment = 0
            elif str(i) in form.overpayment_month.data:
                overpayment = form.overpayment_value.data
                mortgage_remaining -= overpayment
            else:
                overpayment = 0

            if mortgage_remaining < 0:
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

            mortgage_details.append(dict(installment_value=round(installment_value, 2), principal=round(principal, 2),
                                         interest_value=round(interest_value, 2), remaining_mortgage=round(mortgage_remaining, 2),
                                         overpayment=overpayment))
        return render_template('fixed_mortgage.html', table=table(mortgage_details))

    return render_template('fixed.html', form=form)


@app.route('/variable')
def variable():
    form = forms.FixedForm()
    mortgage = 234000  # A
    interest = 0.0315  # b
    period_years = 20
    installments_months = period_years * 12  # n
    paid_rates = 0  # x
    total = []
    for _ in range(installments_months):
        Rk = mortgage / installments_months  # rata kapitalu
        Ro = ((mortgage - paid_rates) * interest) / 12  # rata oprocentowania
        paid_rates += Rk
        total.append(Rk+Ro)
        print(Rk+Ro)
    print(sum(total))
    return render_template('fixed.html', form=form)


if __name__ == '__main__':
    app.run()
