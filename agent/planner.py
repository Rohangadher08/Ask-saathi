from agent.router import route_query


def create_plan(query: str) -> dict:
    intent = route_query(query)

    plans = {
        "health_score": {
            "tools": ["finance", "health_score"],
            "rag": False,
            "description": "Analyze the business financial health and health score."
        },

        "finance": {
            "tools": ["finance"],
            "rag": False,
            "description": "Analyze revenue, expenses and cash flow."
        },

        "government": {
            "tools": ["finance", "government"],
            "rag": True,
            "rag_sources": ["schemes", "policies"],
            "description": "Find relevant government schemes and policy information."
        },

        "loan": {
            "tools": ["finance", "loan", "government"],
            "rag": True,
            "rag_sources": ["schemes", "policies"],
            "description": "Analyze loan affordability and relevant government support."
        },

        "expansion": {
            "tools": [
                "finance",
                "expansion",
                "loan",
                "government"
            ],
            "rag": True,
            "rag_sources": ["schemes"],
            "description": "Analyze business expansion and funding options."
        },

        "documents": {
            "tools": ["documents"],
            "rag": False,
            "description": "Handle business documents."
        },

        "compliance": {
            "tools": ["government"],
            "rag": True,
            "rag_sources": ["policies"],
            "description": "Find relevant compliance information."
        },

        "general": {
            "tools": ["finance", "health_score"],
            "rag": True,
            "rag_sources": ["schemes", "policies"],
            "description": "General business assistance."
        }
    }

    plan = plans.get(
        intent,
        plans["general"]
    ).copy()

    plan["intent"] = intent
    plan["query"] = query

    return plan