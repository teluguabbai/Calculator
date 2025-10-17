from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculator(request):
    result = None
    years = months = days = 0
    from_date = to_date = ''
    principal = rate = ''

    if request.method == 'POST':
        from_date = request.POST.get('from_date', '')
        to_date = request.POST.get('to_date', '')
        principal = request.POST.get('principal', '0')
        rate = request.POST.get('rate', '0')  # monthly rate in %

        try:
            start_date = datetime.strptime(from_date, '%Y-%m-%d')
            end_date = datetime.strptime(to_date, '%Y-%m-%d')
            P = float(principal)
            R = float(rate)   # monthly % (ex: 2 means 2% per month)
        except Exception:
            return render(request, 'calculator.html', {'error': 'Invalid input!'})

        # Difference in years, months, days
        delta = relativedelta(end_date, start_date)
        years, months, days = delta.years, delta.months, delta.days

        # Total months + fractional months
        total_months = years * 12 + months + (days / 30)  # approx days as fraction of month

        # Interest = Principal * (Rate/100) * months
        result = P * (R / 100) * total_months

        result = round(result, 2)

    return render(request, 'calculator.html', {
        'result': result,
        'years': years,
        'months': months,
        'days': days,
        'from_date': from_date,
        'to_date': to_date,
        'principal': principal,
        'rate': rate,
    })