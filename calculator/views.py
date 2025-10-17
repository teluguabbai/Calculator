from django.shortcuts import render
from datetime import datetime
import math

def interest_calculator(request):
    result = None
    years = months = days = 0
    principal = rate = from_date = to_date = interest_type = None

    if request.method == "POST":
        principal = float(request.POST.get("principal"))
        rate = float(request.POST.get("rate"))
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        interest_type = request.POST.get("interest_type")

        # Convert dates
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

        # Duration in days
        delta = to_date_obj - from_date_obj
        days = delta.days

        # Convert to years and months
        years = days // 365
        months = (days % 365) // 30
        days = (days % 365) % 30

        time_in_years = (to_date_obj - from_date_obj).days / 365.0  # fraction of years

        # Simple Interest
        if interest_type == "simple":
            result = (principal * rate * time_in_years) / 100

        # Compound Interest
        elif interest_type == "compound":
            # Compounded yearly
            result = principal * ((1 + (rate / 100)) ** time_in_years) - principal

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