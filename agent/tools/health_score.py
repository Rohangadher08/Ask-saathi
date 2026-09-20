def calculate_health_score(business: dict) -> dict:
    revenue = business.get("monthly_revenue", 0)
    expenses = business.get("monthly_expenses", 0)
    emi = business.get("existing_emi", 0)
    savings = business.get("savings", 0)

    # Cash flow score
    if revenue > 0:
        surplus_ratio = (
            (revenue - expenses - emi) / revenue
        )
        cash_flow_score = min(
            max(50 + surplus_ratio * 100, 0),
            100
        )
    else:
        cash_flow_score = 0

    # Profitability score
    if revenue > 0:
        profit_margin = (
            (revenue - expenses) / revenue
        )
        profitability_score = min(
            max(profit_margin * 100, 0),
            100
        )
    else:
        profitability_score = 0

    # Debt score
    if revenue > 0:
        debt_ratio = emi / revenue
        debt_score = max(
            100 - (debt_ratio * 200),
            0
        )
    else:
        debt_score = 0

    # Savings score
    monthly_expenses = max(expenses, 1)

    reserve_months = (
        savings / monthly_expenses
    )

    savings_score = min(
        reserve_months * 25,
        100
    )

    # Overall health score
    score = (
        cash_flow_score * 0.25
        + profitability_score * 0.20
        + debt_score * 0.20
        + savings_score * 0.15
        + 70 * 0.20
    )

    score = round(
        min(max(score, 0), 100)
    )

    return {
        "health_score": score,
        "cash_flow_score": round(cash_flow_score),
        "profitability_score": round(profitability_score),
        "debt_score": round(debt_score),
        "savings_score": round(savings_score)
    }