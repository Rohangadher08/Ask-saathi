def calculate_loan(
    business: dict,
    loan_amount: float,
    annual_interest: float = 12,
    years: int = 5
) -> dict:

    revenue = business.get("monthly_revenue", 0)
    expenses = business.get("monthly_expenses", 0)
    existing_emi = business.get("existing_emi", 0)

    current_surplus = (
        revenue
        - expenses
        - existing_emi
    )

    months = years * 12

    monthly_rate = (
        annual_interest / 12 / 100
    )

    if monthly_rate > 0:

        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** months
            / (
                (1 + monthly_rate) ** months - 1
            )
        )

    else:

        emi = loan_amount / months

    remaining_surplus = (
        current_surplus - emi
    )

    total_repayment = emi * months

    total_interest = (
        total_repayment - loan_amount
    )

    return {
        "loan_amount": loan_amount,
        "interest_rate": annual_interest,
        "tenure_years": years,
        "estimated_emi": round(emi),
        "current_surplus": round(current_surplus),
        "surplus_after_emi": round(remaining_surplus),
        "total_repayment": round(total_repayment),
        "total_interest": round(total_interest),
        "cash_flow_status": (
            "Positive"
            if remaining_surplus > 0
            else "Under pressure"
        )
    }