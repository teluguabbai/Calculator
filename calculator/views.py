from django.shortcuts import render
from datetime import datetime

def interest_calculator(request):
    result = None
    years = months = days = 0
    principal = rate = from_date = to_date = interest_type = ''

    if request.method == "POST":
        principal_str = request.POST.get("principal", "0")
        rate_str = request.POST.get("rate", "0")
        from_date = request.POST.get("from_date", "")
        to_date = request.POST.get("to_date", "")
        interest_type = request.POST.get("interest_type", "")

        try:
            principal = float(principal_str)
            rate = float(rate_str)

            if from_date and to_date:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

                delta = to_date_obj - from_date_obj
                total_days = delta.days

                years = total_days // 365
                months = (total_days % 365) // 30
                days = (total_days % 365) % 30

                time_in_years = total_days / 365.0

                if interest_type == "simple":
                    result = (principal * rate * time_in_years) / 100
                elif interest_type == "compound":
                    result = principal * ((1 + rate/100) ** time_in_years) - principal

        except ValueError:
            result = "Invalid input"

    return render(request, "calculator.html", {
        "result": result,
        "principal": principal,
        "rate": rate,
        "from_date": from_date,
        "to_date": to_date,
        "interest_type": interest_type,
        "years": years,
        "months": months,
        "days": days
    })