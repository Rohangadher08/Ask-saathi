def find_government_schemes(business: dict, query: str = "") -> list:

    schemes = [
        {
            "name": "PMMY / MUDRA",
            "purpose": "Credit support for eligible micro enterprises",
            "relevance": "Potentially relevant for eligible micro businesses",
            "source": "Government of India"
        },
        {
            "name": "PMEGP",
            "purpose": "Support for eligible new micro-enterprises",
            "relevance": "Potentially relevant depending on business conditions",
            "source": "Government of India / KVIC"
        },
        {
            "name": "CGTMSE",
            "purpose": "Credit guarantee support for eligible credit facilities",
            "relevance": "Potentially relevant depending on lender and eligibility",
            "source": "CGTMSE / Government of India"
        },
        {
            "name": "Udyam Registration",
            "purpose": "Official MSME registration for eligible enterprises",
            "relevance": "Potentially useful for eligible MSMEs",
            "source": "Government of India / Udyam Registration"
        }
    ]

    return schemes