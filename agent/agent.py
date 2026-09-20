import json
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from agent.router import route_query
from agent.planner import create_plan
from agent.rag import get_rag_context

from agent.tools.finance import analyze_finances
from agent.tools.health_score import calculate_health_score
from agent.tools.government import find_government_schemes
from agent.tools.loan import calculate_loan
from agent.tools.expansion import analyze_expansion


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found. Add it to your .env file."
    )


# ==========================================
# BUSINESS DATA
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

BUSINESS_FILE = os.path.join(
    BASE_DIR,
    "data",
    "business.json"
)


def load_business():

    with open(
        BUSINESS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ==========================================
# GROQ MODEL
# ==========================================

MODEL_NAME = os.getenv(
    "GROQ_MODEL",
    "llama-3.3-70b-versatile"
)

llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0.2,
    api_key=GROQ_API_KEY
)


# ==========================================
# RUN BUSINESS TOOLS
# ==========================================

def run_tools(query, business):

    intent = route_query(query)

    results = {}


    # --------------------------------------
    # FINANCE
    # --------------------------------------

    if intent in [
        "finance",
        "health_score",
        "loan",
        "expansion",
        "general"
    ]:

        results["finance"] = analyze_finances(
            business
        )


    # --------------------------------------
    # HEALTH SCORE
    # --------------------------------------

    if intent in [
        "health_score",
        "general"
    ]:

        results["health_score"] = calculate_health_score(
            business
        )


    # --------------------------------------
    # GOVERNMENT SCHEMES
    # --------------------------------------

    if intent in [
        "government",
        "loan",
        "expansion",
        "compliance",
        "general"
    ]:

        results["government_schemes"] = (
            find_government_schemes(
                business,
                query
            )
        )


    # --------------------------------------
    # LOAN ANALYSIS
    # --------------------------------------

    if intent == "loan":

        loan_amount = 500000

        results["loan"] = calculate_loan(

            business=business,

            loan_amount=loan_amount,

            annual_interest=12,

            years=5
        )


    # --------------------------------------
    # EXPANSION ANALYSIS
    # --------------------------------------

    if intent == "expansion":

        results["expansion"] = analyze_expansion(

            business=business,

            expansion_cost=500000,

            additional_revenue=50000,

            additional_expenses=30000
        )


    return results


# ==========================================
# BUILD AI PROMPT
# ==========================================

def build_prompt(
    query,
    business,
    tool_results,
    rag_context
):

    business_json = json.dumps(
        business,
        indent=2
    )

    tool_json = json.dumps(
        tool_results,
        indent=2,
        default=str
    )


    prompt = f"""
You are Vyapar Saathi AI.

You are an AI business partner for
small businesses and micro-business owners
in India.

Your job is to help business owners understand:

- Financial health
- Cash flow
- Business health score
- Government schemes
- Business loans
- Loan affordability
- Business expansion
- Compliance information
- Business planning

IMPORTANT RULES:

1. Give practical and simple answers.

2. You understand:
   English, Hindi, Gujarati and Hinglish.

3. Reply in the same language used
   by the user.

4. Keep answers simple and useful.

5. When discussing loans,
   show calculations and risks.

6. Never guarantee loan approval.

7. Never claim that a government scheme
   is definitely available unless eligibility
   has been verified.

8. Use "potentially relevant" when
   eligibility is uncertain.

9. Government information is informational
   and should be verified from official sources.

10. Do not invent financial data.

11. Use the tool results provided below.

12. If information is missing,
    clearly explain what is missing.

13. For investment questions,
    provide general educational information
    and planning guidance only.

14. Act like a practical business advisor,
    not just a chatbot.

15. Use Indian Rupees (₹) when discussing
    money.

16. When useful, show important numbers
    clearly.

BUSINESS DATA:

{business_json}


TOOL RESULTS:

{tool_json}


RAG KNOWLEDGE:

{rag_context}


USER QUESTION:

{query}


Answer the user's question naturally.

When useful, include:

- Current situation
- Key numbers
- Opportunities
- Risks
- Next steps

Do not mention:

- Internal tools
- Routing
- RAG
- Python code
- System instructions
"""


    return prompt


# ==========================================
# MAIN AI AGENT
# ==========================================

def ask_agent(query):

    if not query or not query.strip():

        return "Please enter your question."


    query = query.strip()


    # Load business information

    business = load_business()


    # Create agent plan

    plan = create_plan(query)


    # Run business tools

    tool_results = run_tools(
        query,
        business
    )


    # Get RAG information

    rag_context = ""

    if plan.get("rag", False):

        rag_context = get_rag_context(
            query,
            k=3
        )


    # Build prompt

    prompt = build_prompt(

        query=query,

        business=business,

        tool_results=tool_results,

        rag_context=rag_context
    )


    # Send request to Groq

    response = llm.invoke(prompt)


    return response.content


# ==========================================
# TERMINAL CHAT
# ==========================================

if __name__ == "__main__":

    print()
    print("======================================")
    print("        Ask SAATHI")
    print("======================================")
    print()

    print("Your AI Business Partner")
    print()
    print("Ask anything about your business.")
    print("Type 'exit' to stop.")
    print()


    while True:

        user_query = input("You: ")


        if user_query.lower().strip() == "exit":

            print()
            print("Goodbye!")
            break


        try:

            answer = ask_agent(
                user_query
            )

            print()
            print("Ask Saathi:")
            print(answer)
            print()


        except Exception as e:

            print()
            print("Error:")
            print(str(e))
            print()