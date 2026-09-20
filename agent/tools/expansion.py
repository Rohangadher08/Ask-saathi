def analyze_expansion(
    business: dict,
    expansion_cost: float,
    additional_revenue: float,
    additional_expenses: float
) -> dict:

    additional_profit = (
        additional_revenue - additional_expenses
    )

    current_surplus = (
        business.get("monthly_revenue", 0)
        - business.get("monthly_expenses", 0)
        - business.get("existing_emi", 0)
    )

    if additional_profit > 0:
        break_even_months = (
            expansion_cost / additional_profit
        )
    else:
        break_even_months = None

    funding_gap = max(
        expansion_cost - business.get("savings", 0),
        0
    )

    return {
        "expansion_cost": expansion_cost,
        "additional_revenue": additional_revenue,
        "additional_expenses": additional_expenses,
        "additional_profit": additional_profit,
        "current_surplus": current_surplus,
        "funding_gap": funding_gap,
        "break_even_months": (
            round(break_even_months, 1)
            if break_even_months is not None
            else None
        )
    }