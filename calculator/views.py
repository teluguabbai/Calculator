from django.shortcuts import render
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculator(request):
    result = None
    years = months = days = 0
    from_date = to_date = ''
    principal = rate = interest_type = ''

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        principal = request.POST.get('principal', '0')
        rate = request.POST.get('rate', '0')
        interest_type = request.POST.get('interest_type')

        try:
            principal = float(principal)
            rate = float(rate)
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

            if to_date_obj < from_date_obj:
                result = "Error: To Date must be after From Date"
            else:
                # Calculate duration
                delta = relativedelta(to_date_obj, from_date_obj)
                years = delta.years
                months = delta.months
                days = delta.days

                # Total months (approximate days as fraction)
                total_months = years * 12 + months + (days / 30)

                if interest_type == 'simple':
                    # Simple Interest = Principal * Rate% per month * total months
                    result = (principal * rate / 100) * total_months
                elif interest_type == 'compound':
                    # Compound Interest per month = Principal * ((1 + rate/100)^months - 1)
                    result = principal * ((1 + rate / 100) ** total_months - 1)
                else:
                    result = "Error: Invalid Interest Type"

        except Exception as e:
            result = f"Error: {str(e)}"

    context = {
        'result': round(result, 2) if isinstance(result, float) else result,
        'years': int(years),
        'months': int(months),
        'days': int(days),
        'from_date': from_date,
        'to_date': to_date,
        'principal': principal,
        'rate': rate,
        'interest_type': interest_type,
    }

    return render(request, 'calculator.html', context)