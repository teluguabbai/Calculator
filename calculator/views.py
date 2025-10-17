from django.shortcuts import render
from datetime import datetime

def interest_calculator(request):
    # Initialize variables for template
    result = None
    years = months = days = 0
    principal = rate = ''
    from_date = to_date = ''
    interest_type = ''

    if request.method == "POST":
        # Get POST data safely
        principal_str = request.POST.get("principal", "").strip()
        rate_str = request.POST.get("rate", "").strip()
        from_date = request.POST.get("from_date", "").strip()
        to_date = request.POST.get("to_date", "").strip()
        interest_type = request.POST.get("interest_type", "").strip()

        try:
            # Convert principal and rate only if provided
            principal = float(principal_str) if principal_str else 0.0
            rate = float(rate_str) if rate_str else 0.0

            # Convert dates only if both are provided
            if from_date and to_date:
                from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
                to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")

                delta = to_date_obj - from_date_obj
                total_days = delta.days

                # Avoid negative durations
                if total_days < 0:
                    raise ValueError("To date must be after from date")

                # Convert days into years, months, days
                years = total_days // 365
                months = (total_days % 365) // 30
                days = (total_days % 365) % 30

                time_in_years = total_days / 365.0

                # Calculate interest
                if interest_type == "simple":
                    result = (principal * rate * time_in_years) / 100
                elif interest_type == "compound":
                    result = principal * ((1 + rate / 100) ** time_in_years) - principal

        except ValueError as e:
            # Catch any conversion or logic errors
            result = f"Error: {str(e)}"

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