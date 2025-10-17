from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta
import math

def calculator(request):
    context = {
        'result': None,
        'total_amount': None,
        'years': 0, 'months': 0, 'days': 0,
        'from_date': '', 'to_date': '',
        'principal': '', 'rate': '', 'interest_type': '',
        'compounding': 'annual',
        'error': None,
    }

    if request.method == 'POST':
        # Read inputs (use defaults to avoid None)
        from_date = request.POST.get('from_date', '')
        to_date = request.POST.get('to_date', '')
        principal = request.POST.get('principal', '0')
        rate = request.POST.get('rate', '0')
        interest_type = request.POST.get('interest_type', 'simple')  # 'simple' or 'compound'
        compounding = request.POST.get('compounding', 'annual')      # 'annual','semiannual','quarterly','monthly','daily','continuous'

        context.update({
            'from_date': from_date, 'to_date': to_date,
            'principal': principal, 'rate': rate,
            'interest_type': interest_type, 'compounding': compounding
        })

        # Validate + parse
        try:
            start_date = datetime.strptime(from_date, '%Y-%m-%d')
            end_date = datetime.strptime(to_date, '%Y-%m-%d')
        except ValueError:
            context['error'] = 'Please enter valid dates (YYYY-MM-DD).'
            return render(request, 'calculator.html', context)

        if end_date < start_date:
            context['error'] = 'End date must be after start date.'
            return render(request, 'calculator.html', context)

        try:
            P = float(principal)
            r = float(rate)
        except ValueError:
            context['error'] = 'Principal and rate must be numeric.'
            return render(request, 'calculator.html', context)

        # human-friendly breakdown for display
        delta = relativedelta(end_date, start_date)
        context['years'] = delta.years
        context['months'] = delta.months
        context['days'] = delta.days

        # precise total-time-in-years using actual days
        total_days = (end_date - start_date).days
        DAY_COUNT = 365.25   # choose convention: 365, 365.25, or 360 depending on your needs
        t_years = total_days / DAY_COUNT

        # compute interest
        interest = 0.0
        total_amount = None

        if interest_type == 'simple':
            # Simple interest: I = P * r * t
            interest = P * (r / 100.0) * t_years
            total_amount = P + interest

        else:  # compound
            if compounding == 'continuous':
                total_amount = P * math.exp((r / 100.0) * t_years)
                interest = total_amount - P
            else:
                freq_map = {
                    'annual': 1,
                    'semiannual': 2,
                    'quarterly': 4,
                    'monthly': 12,
                    'daily': 365,
                }
                n = freq_map.get(compounding, 1)
                # A = P * (1 + r/(100*n))^(n*t)
                total_amount = P * ((1 + (r / 100.0) / n) ** (n * t_years))
                interest = total_amount - P

        # Round results for display
        context['result'] = round(interest, 2)
        context['total_amount'] = round(total_amount, 2)

    return render(request, 'calculator.html', context)