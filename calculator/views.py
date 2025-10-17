from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculator(request):
    result = None
    total_amount = None
    years = months = days = 0
    from_date = to_date = ''
    principal = rate = ''
    interest_type = 'simple'

    if request.method == 'POST':
        from_date = request.POST.get('from_date', '')
        to_date = request.POST.get('to_date', '')
        principal = request.POST.get('principal', '0')
        rate = request.POST.get('rate', '0')  # monthly rate in %

        try:
            start_date = datetime.strptime(from_date, '%Y-%m-%d')
            end_date = datetime.strptime(to_date, '%Y-%m-%d')
            P = float(principal)
            R = float(rate)   # monthly rate in %
        except Exception:
            return render(request, 'calculator.html', {'error': 'Invalid input!'})

        interest_type = request.POST.get('interest_type', 'simple')

        # Difference in years, months, days
        delta = relativedelta(end_date, start_date)
        years, months, days = delta.years, delta.months, delta.days

        # Convert period into months (with fractional part for days)
        total_months = years * 12 + months + (days / 30)

        if interest_type == 'simple':
            # Simple Interest
            result = P * (R / 100) * total_months
            total_amount = P + result
        else:
            # Compound Interest (monthly compounding)
            total_amount = P * ((1 + (R / 100)) ** total_months)
            result = total_amount - P

        result = round(result, 2)
        total_amount = round(total_amount, 2)

    return render(request, 'calculator.html', {
        'result': result,
        'total_amount': total_amount,
        'years': years,
        'months': months,
        'days': days,
        'from_date': from_date,
        'to_date': to_date,
        'principal': principal,
        'rate': rate,
        'interest_type': interest_type,
    })