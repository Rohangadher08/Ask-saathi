def route_query(query: str) -> str:
    query = query.lower().strip()

    health_keywords = [
        "health score",
        "business health",
        "business kaisa",
        "financial health",
        "profit",
        "profitability"
    ]

    if any(keyword in query for keyword in health_keywords):
        return "health_score"

    finance_keywords = [
        "cash flow",
        "revenue",
        "expense",
        "expenses",
        "income",
        "sales",
        "finance",
        "financial"
    ]

    if any(keyword in query for keyword in finance_keywords):
        return "finance"

    government_keywords = [
        "government",
        "scheme",
        "schemes",
        "mudra",
        "pmegp",
        "cgtmse",
        "udyam",
        "subsidy"
    ]

    if any(keyword in query for keyword in government_keywords):
        return "government"

    loan_keywords = [
        "loan",
        "emi",
        "borrow",
        "borrowing",
        "credit",
        "funding",
        "5 lakh",
        "500000"
    ]

    if any(keyword in query for keyword in loan_keywords):
        return "loan"

    expansion_keywords = [
        "expansion",
        "expand",
        "second shop",
        "new shop",
        "new branch",
        "business grow",
        "growth"
    ]

    if any(keyword in query for keyword in expansion_keywords):
        return "expansion"

    document_keywords = [
        "document",
        "documents",
        "upload",
        "pdf",
        "invoice",
        "report"
    ]

    if any(keyword in query for keyword in document_keywords):
        return "documents"

    compliance_keywords = [
        "compliance",
        "gst",
        "tax",
        "registration"
    ]

    if any(keyword in query for keyword in compliance_keywords):
        return "compliance"

    return "general"