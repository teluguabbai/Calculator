from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

def interest_calculator(request):
    result = None
    years = months = days = 0
    from_date = to_date = ''
    principal = rate = interest_type = ''

    if request.method == 'POST':
        # Get input values
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        principal = request.POST.get('principal')
        rate = request.POST.get('rate')
        interest_type = request.POST.get('interest_type')

        # Convert to proper types
        start_date = datetime.strptime(from_date, '%Y-%m-%d')
        end_date = datetime.strptime(to_date, '%Y-%m-%d')
        principal = float(principal)
        rate = float(rate)

        # Calculate date difference
        delta = relativedelta(end_date, start_date)
        years = delta.years
        months = delta.months
        days = delta.days

        total_time_years = years + months / 12 + days / 365.25

        # Calculate interest
        if interest_type == 'simple':
            result = (principal * rate * total_time_years) / 100
        elif interest_type == 'compound':
            result = principal * ((1 + rate / 100) ** total_time_years) - principal

    return render(request, 'calculator/interest_form.html', {
        'result': result,
        'years': years,
        'months': months,
        'days': days,
        'from_date': from_date,
        'to_date': to_date,
        'principal': principal,
        'rate': rate,
        'interest_type': interest_type,
    })
