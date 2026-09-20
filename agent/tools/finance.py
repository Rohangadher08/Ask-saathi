def analyze_finances(business: dict) -> dict:
    revenue = business.get("monthly_revenue", 0)
    expenses = business.get("monthly_expenses", 0)
    emi = business.get("existing_emi", 0)

    operating_profit = revenue - expenses

    monthly_surplus = (
        revenue - expenses - emi
    )

    profit_margin = (
        (operating_profit / revenue) * 100
        if revenue > 0
        else 0
    )

    return {
        "revenue": revenue,
        "expenses": expenses,
        "existing_emi": emi,
        "operating_profit": operating_profit,
        "monthly_surplus": monthly_surplus,
        "profit_margin": round(profit_margin, 2)
    }