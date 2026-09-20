import streamlit as st
import json
import pandas as pd
from pathlib import Path

from agent.agent import ask_agent

from database import (
    init_db,
    get_stores,
    add_store
)

from auth import show_login


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Ask Saathi",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if not st.session_state.logged_in:

    show_login()

    st.stop()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f7f9fc;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #6693F5;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Main title */
    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6b7280;
        font-size: 16px;
        margin-bottom: 25px;
    }

    /* Cards */
    .card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    .card-title {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .card-value {
        color: #111827;
        font-size: 28px;
        font-weight: 700;
    }

    /* Health score */
    .health-card {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: white;
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(37,99,235,0.20);
    }

    .health-score {
        font-size: 52px;
        font-weight: 800;
    }

    .health-label {
        font-size: 16px;
        opacity: 0.9;
    }

    /* Agent box */
    .agent-box {
        background: white;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }

    /* Insight */
    .insight {
        background: #eff6ff;
        padding: 16px;
        border-radius: 12px;
        border-left: 4px solid #2563eb;
        margin-bottom: 10px;
    }

    /* Hide Streamlit menu */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# DEMO BUSINESS DATA
# =========================================================

business = {
    "business_name": "Ramesh Provision Store",
    "owner": "Ramesh",
    "business_type": "Kirana Store",
    "location": "Ahmedabad, Gujarat",
    "monthly_revenue": 120000,
    "monthly_expenses": 80000,
    "existing_emi": 10000,
    "savings": 62500,
    "business_age": 4
}

surplus = (
    business["monthly_revenue"]
    - business["monthly_expenses"]
    - business["existing_emi"]
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🤝Ask Saathi ")

    st.caption("Your AI Business Partner")
    st.markdown("---")

    st.markdown(
        f"### 👤 {st.session_state.user_name}"
    )

    st.markdown("### 🏪 My Stores")

    stores = get_stores(
        st.session_state.user_id
    )

    if stores:

        store_names = [
            store["business_name"]
            for store in stores
        ]

        selected_store_name = st.selectbox(
            "Select Store",
            store_names,
            key="store_selector"
        )

        selected_store = next(
            store
            for store in stores
            if store["business_name"] == selected_store_name
        )

        st.session_state.selected_store = selected_store

        st.success(
            f"Active: {selected_store['business_name']}"
        )

    else:

        st.warning("No stores added yet.")

    if st.button(
        "➕ Add New Store",
        use_container_width=True
    ):
        st.session_state.show_add_store = True

    st.divider()

    

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview",
            "🤖 AI Business Agent",
            "💚 Business Health",
            "💰 Cash Flow",
            "🏛️ Government Schemes",
            "📋 Policies & Compliance",
            "🏦 Loans & Funding",
            "📈 Business Expansion",
            "📄 Documents",
            "📊 Reports"
        ]
    )

    st.divider()

    language = st.selectbox(
    "🌐 Language",
    ["English", "Hindi", "Gujarati", "Hinglish"]
)
# =========================================================
# ADD NEW STORE
# =========================================================

if st.session_state.get("show_add_store", False):

    st.markdown("## ➕ Add New Store")

    with st.form("add_store_form"):

        business_name = st.text_input(
            "Business Name"
        )

        business_type = st.text_input(
            "Business Type"
        )

        location = st.text_input(
            "Location"
        )

        monthly_revenue = st.number_input(
            "Monthly Revenue",
            min_value=0.0,
            step=1000.0
        )

        monthly_expenses = st.number_input(
            "Monthly Expenses",
            min_value=0.0,
            step=1000.0
        )

        existing_emi = st.number_input(
            "Existing EMI",
            min_value=0.0,
            step=500.0
        )

        savings = st.number_input(
            "Savings",
            min_value=0.0,
            step=1000.0
        )

        submitted = st.form_submit_button(
            "Create Store"
        )

        if submitted:

            if not business_name.strip():

                st.error(
                    "Please enter a business name."
                )

            else:

                new_store = {
                    "business_name": business_name,
                    "business_type": business_type,
                    "location": location,
                    "monthly_revenue": monthly_revenue,
                    "monthly_expenses": monthly_expenses,
                    "existing_emi": existing_emi,
                    "savings": savings,
                    "business_age_years": 0,
                    "expansion_goal": "",
                    "employees": 0,
                    "monthly_rent": 0,
                    "monthly_inventory_cost": 0,
                    "owner_experience_years": 0
                }

                add_store(
                    st.session_state.user_id,
                    new_store
                )

                st.session_state.show_add_store = False

                st.success(
                    f"{business_name} added successfully!"
                )

                st.rerun()
LANGUAGE_INSTRUCTIONS = {
    "English": "Reply in English.",
    "Hindi": "Reply in Hindi using simple Hindi. You may keep common business terms in English.",
    "Gujarati": "Reply in Gujarati using simple Gujarati. You may keep common business terms in English.",
    "Hinglish": "Reply in simple Hinglish using Hindi and English naturally."
}

language_instruction = LANGUAGE_INSTRUCTIONS[language]

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">Ask Saathi  🤝</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI business partner — from daily cash flow to business growth.</div>',
    unsafe_allow_html=True
)


# =========================================================
# OVERVIEW
# =========================================================

if page == "🏠 Overview":

    st.markdown(
        f"### Good evening, {business['owner']} 👋"
    )

    st.write(
        f"Here is the current status of **{business['business_name']}**."
    )

    st.write("")

    # -----------------------------
    # TOP CARDS
    # -----------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Monthly Revenue</div>
                <div class="card-value">₹{business['monthly_revenue']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Monthly Expenses</div>
                <div class="card-value">₹{business['monthly_expenses']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Monthly Surplus</div>
                <div class="card-value">₹{surplus:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">Savings</div>
                <div class="card-value">₹{business['savings']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # -----------------------------
    # HEALTH + AGENT
    # -----------------------------

    col1, col2 = st.columns([1, 2])

    with col1:

        st.markdown(
            """
            <div class="health-card">
                <div class="health-label">Business Health Score</div>
                <div class="health-score">78/100</div>
                <div class="health-label">
                    Your business is financially stable.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.progress(0.78)

        st.caption(
            "Based on cash flow, profitability, debt, savings and compliance."
        )

    with col2:

        st.markdown(
            """
            <div class="agent-box">
                <h3>🤖 Ask Your Business Agent</h3>
                <p>
                    Ask anything about your business. The AI agent will
                    automatically analyze your business data and provide
                    relevant insights.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_query = st.chat_input(
            "Ask your business agent..."
        )

        if user_query:

            st.chat_message("user").write(user_query)

            with st.chat_message("assistant"):

                st.write(
                    "🤖 I'm analyzing your business data..."
                )

                st.write(
                    f"""
                    Based on your current data:

                    - Monthly revenue: **₹{business['monthly_revenue']:,}**
                    - Monthly expenses: **₹{business['monthly_expenses']:,}**
                    - Existing EMI: **₹{business['existing_emi']:,}**
                    - Monthly surplus: **₹{surplus:,}**
                    - Savings: **₹{business['savings']:,}**

                    Your Business Health Score is **78/100**.

                    I can also analyze loans, government schemes,
                    compliance and business expansion for you.
                    """
                )

    # -----------------------------
    # AI INSIGHTS
    # -----------------------------

    st.write("")
    st.markdown("### 💡 AI Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="insight">
            <b>💰 Cash Flow</b><br>
            Your business generates a positive monthly surplus.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="insight">
            <b>🏦 Funding</b><br>
            You may be able to evaluate additional funding for expansion.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="insight">
            <b>📈 Growth</b><br>
            Your positive cash flow can support expansion planning.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# AI AGENT
# =========================================================

elif page == "🤖 AI Business Agent":

    st.markdown("## 🤖 AI Business Agent")

    st.write(
        "Talk to your business agent. It automatically decides "
        "which business analysis is required."
    )

    st.info(
        "Example: Ask about your health, loan, government schemes, "
        "cash flow or business expansion."
    )

    user_query = st.chat_input(
        "Ask anything about your business..."
    )

    if user_query:

     st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Analyzing your business..."):

            try:

                response = ask_agent(
                    f"""
                    Reply in {language}.

                    User question:
                    {user_query}
                    """
                )

                st.write(response)

            except Exception as e:

                st.error(
                    f"Unable to process your request: {str(e)}"
                )


# =========================================================
# BUSINESS HEALTH
# =========================================================

elif page == "💚 Business Health":

    st.markdown("## 💚 Business Health")

    st.markdown(
        """
        <div class="health-card">
            <div class="health-label">Overall Business Health</div>
            <div class="health-score">78/100</div>
            <div class="health-label">
                Financially stable with opportunities for growth.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Health Breakdown")

        st.metric("Cash Flow", "88/100")
        st.metric("Revenue Stability", "72/100")
        st.metric("Profitability", "82/100")

    with col2:
        st.subheader("Financial Strength")

        st.metric("Debt Health", "80/100")
        st.metric("Savings", "65/100")
        st.metric("Compliance", "70/100")


# =========================================================
# CASH FLOW
# =========================================================

elif page == "💰 Cash Flow":

    st.markdown("## 💰 Cash Flow")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Revenue",
        f"₹{business['monthly_revenue']:,}"
    )

    col2.metric(
        "Expenses",
        f"₹{business['monthly_expenses']:,}"
    )

    col3.metric(
        "Surplus",
        f"₹{surplus:,}"
    )

    st.write("")

    st.subheader("Monthly Cash Flow")

    st.bar_chart(
        {
            "Revenue": [110000, 115000, 118000, 120000],
            "Expenses": [76000, 78000, 79000, 80000]
        }
    )


# =========================================================
# GOVERNMENT SCHEMES
# =========================================================

elif page == "🏛️ Government Schemes":

    st.markdown("## 🏛️ Government Schemes")

    st.info(
        "Explore government schemes that may be relevant "
        "for your small business."
    )

    # PMMY / MUDRA
    st.markdown("### 🏦 PMMY / MUDRA")

    if st.button("View Details", key="mudra_details"):
        st.success("PMMY / MUDRA")
        st.write(
            "Credit support for eligible micro enterprises."
        )
        st.write("**Purpose:** Business funding and credit support.")
        st.write(
            "**Eligibility:** Depends on applicable government "
            "guidelines and lender requirements."
        )
        st.write("**Source:** Government of India")

    st.divider()

    # PMEGP
    st.markdown("### 🏭 PMEGP")

    if st.button("View Details", key="pmegp_details"):
        st.success("PMEGP")
        st.write(
            "Support for eligible new micro-enterprises."
        )
        st.write("**Purpose:** Support for eligible new businesses.")
        st.write(
            "**Eligibility:** Depends on applicable scheme guidelines."
        )
        st.write("**Source:** Government of India / KVIC")

    st.divider()

    # CGTMSE
    st.markdown("### 🛡️ CGTMSE")

    if st.button("View Details", key="cgtmse_details"):
        st.success("CGTMSE")
        st.write(
            "Credit guarantee support for eligible credit facilities."
        )
        st.write("**Purpose:** Credit guarantee support.")
        st.write(
            "**Eligibility:** Depends on lender and scheme guidelines."
        )
        st.write("**Source:** CGTMSE / Government of India")

    st.divider()

    # Udyam
    st.markdown("###📝 Udyam")

    if st.button("View Details", key="udyam_details"):
        st.success("Udyam Registration")
        st.write(
            "Official MSME registration for eligible enterprises."
        )
        st.write("**Purpose:** MSME registration.")
        st.write(
            "**Eligibility:** Depends on applicable MSME criteria."
        )
        st.write("**Source:** Government of India")
        
# =========================================================
# POLICIES & COMPLIANCE
# =========================================================

elif page == "📋 Policies & Compliance":

    st.markdown("## 📋 Policies & Compliance")

    st.write(
        "Track important registrations, licenses and compliance requirements."
    )

    st.divider()

    # =========================
    # UDYAM REGISTRATION
    # =========================

    with st.expander("📝 Udyam Registration — View Details"):

        st.markdown("### 📝 Udyam Registration")

        udyam_file = Path("udyam_file.csv")

        if udyam_file.exists():

            udyam_df = pd.read_csv(udyam_file)

            # -------------------------
            # Registration Steps
            # -------------------------

            st.markdown("### 🔹 Registration Steps")

            steps_df = udyam_df[
                udyam_df["section"] == "steps"
            ].sort_values("step_no")

            for _, row in steps_df.iterrows():

                step_number = int(row["step_no"])

                st.markdown(
                    f"#### Step {step_number}: {row['title']}"
                )

                st.write(row["details"])

                if pd.notna(row["inputs_needed"]):
                    st.write(
                        f"**📌 Inputs Needed:** "
                        f"{row['inputs_needed']}"
                    )

                if pd.notna(row["output"]):
                    st.write(
                        f"**✅ Output:** "
                        f"{row['output']}"
                    )

                st.divider()

            # -------------------------
            # Requirements
            # -------------------------

            st.markdown("### 📌 Requirements")

            requirements_df = udyam_df[
                udyam_df["section"] == "requirements"
            ]

            for _, row in requirements_df.iterrows():

                st.markdown(
                    f"#### {row['title']}"
                )

                st.write(row["details"])

            # -------------------------
            # Rules
            # -------------------------

            st.markdown("### 📜 Important Rules")

            rules_df = udyam_df[
                udyam_df["section"] == "rules"
            ]

            for _, row in rules_df.iterrows():

                st.markdown(
                    f"#### {row['title']}"
                )

                st.write(row["details"])

            # -------------------------
            # FAQ
            # -------------------------

            st.markdown("### ❓ Frequently Asked Questions")

            faq_df = udyam_df[
                udyam_df["section"] == "faq"
            ]

            for _, row in faq_df.iterrows():

                with st.expander(
                    f"❓ {row['title']}"
                ):
                    st.write(row["details"])

        else:

            st.error(
                "udyam_registration_steps.csv not found."
            )

    # =========================
    # GST
    # =========================

    with st.expander("🧾 GST — View Details"):

        st.markdown("### 🧾 GST Information")

        gst_file = Path("gst_file.csv")

        if gst_file.exists():

            gst_df = pd.read_csv(gst_file)

            sector = st.selectbox(
                "Select Business Sector",
                gst_df["Business Sector"].tolist(),
                key="gst_sector"
            )

            selected = gst_df[
                gst_df["Business Sector"] == sector
            ].iloc[0]

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Primary GST Rate",
                    f"{selected['Primary GST Rate (%)']}%"
                )

                st.write(
                    f"**Registration Threshold:** "
                    f"{selected['Registration Threshold']}"
                )

                st.write(
                    f"**SAC/HSN Code Range:** "
                    f"{selected['SAC/HSN Code Range']}"
                )

            with col2:

                st.write(
                    f"**Primary Return Form:** "
                    f"{selected['Primary Return Form']}"
                )

            st.divider()

            st.markdown("### 📊 GST Dataset")

            st.dataframe(
                gst_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error(
                "gst_file.csv not found. "
                "Place it in the same folder as app.py."
            )

    # ==============================
    # TRADE LICENSE
    # ==============================

    with st.expander(
        "🏪 Local Trade License — View Details"
    ):

        st.markdown("### 🏪 Local Trade License")

        trade_file = Path(
            "trade_file.csv"
        )

        if trade_file.exists():

            trade_df = pd.read_csv(trade_file)

            # ------------------------------
            # CITY / REGION
            # ------------------------------

            cities = sorted(
                trade_df["City_or_Region"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_city = st.selectbox(
                "📍 Select City / Region",
                cities,
                key="trade_license_city"
            )

            # ------------------------------
            # SELECTED CITY DATA
            # ------------------------------

            city_df = trade_df[
                trade_df["City_or_Region"]
                == selected_city
            ].sort_values("Step_No")

            if not city_df.empty:

                # ------------------------------
                # BASIC INFORMATION
                # ------------------------------

                authority = city_df.iloc[0][
                    "Issuing_Authority"
                ]

                state = city_df.iloc[0][
                    "State_UT"
                ]

                col1, col2 = st.columns(2)

                with col1:

                    st.markdown(
                        "**🏛️ Issuing Authority**"
                    )

                    st.write(authority)

                with col2:

                    st.markdown(
                        "**📍 State / UT**"
                    )

                    st.write(state)

                st.divider()

                # ------------------------------
                # REGISTRATION STEPS
                # ------------------------------

                st.markdown(
                    f"### 📋 Registration Steps — "
                    f"{selected_city}"
                )

                for _, row in city_df.iterrows():

                    step_number = int(
                        row["Step_No"]
                    )

                    st.markdown(
                        f"#### Step {step_number}:"
                    )

                    st.write(
                        row["Step"]
                    )

                    if pd.notna(
                        row["Steps_Verified"]
                    ):

                        st.write(
                            f"**🔎 Verification:** "
                            f"{row['Steps_Verified']}"
                        )

                    if pd.notna(
                        row["Confidence"]
                    ):

                        st.write(
                            f"**📊 Confidence:** "
                            f"{row['Confidence']}"
                        )

                    st.divider()

            else:

                st.warning(
                    "No trade license information "
                    "found for this city."
                )

        else:

            st.error(
                "Trade license dataset not found."
            )



    # =========================
    # TAX COMPLIANCE
    # =========================

    with st.expander("💰 Tax Compliance — View Details"):

        st.markdown("### 💰 Tax Compliance")

        st.write(
            "Businesses may need to maintain appropriate "
            "records and comply with applicable tax requirements."
        )

        st.markdown("""
        **Important areas:**

        - Income tax
        - GST, where applicable
        - Business expense records
        - Sales and purchase records
        - Invoices and bills
        """)

    # =========================
    # INVOICE & RECORD KEEPING
    # =========================

    with st.expander("📄 Invoice & Record Keeping — View Details"):

        st.markdown("### 📄 Invoice & Record Keeping")

        st.write(
            "Maintain proper invoices, purchase records, "
            "sales records and business expenses."
        )

        st.markdown("""
        **Recommended records:**

        - Sales invoices
        - Purchase invoices
        - Expense records
        - Bank transaction records
        - GST records, where applicable
        """)

    st.divider()

    st.info(
        "💡 Compliance requirements can vary based on "
        "business type, location and applicable rules. "
        "Verify current requirements with official authorities."
    )


# =====================================================
# LOANS & FUNDING
# =====================================================

elif page == "🏦 Loans & Funding":

    st.markdown("## 🏦 Loans & Funding")

    st.write(
        "Evaluate loan affordability before taking a business loan."
    )

    st.divider()

    business = st.session_state.get(
        "selected_store"
    )

    if business:

        loan_amount = st.number_input(
            "💰 Loan Amount",
            min_value=0.0,
            value=500000.0,
            step=50000.0
        )

        interest_rate = st.number_input(
            "📈 Annual Interest Rate (%)",
            min_value=0.0,
            value=12.0,
            step=0.5
        )

        tenure = st.number_input(
            "📅 Loan Tenure (Years)",
            min_value=1,
            max_value=15,
            value=5
        )

        if st.button(
            "🔍 Analyze Loan",
            use_container_width=True
        ):

            from agent.tools.loan import calculate_loan

            result = calculate_loan(
                business,
                loan_amount,
                interest_rate,
                tenure
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Estimated EMI",
                    f"₹{result['estimated_emi']:,}"
                )

            with col2:
                st.metric(
                    "Total Interest",
                    f"₹{result['total_interest']:,}"
                )

            with col3:
                st.metric(
                    "Surplus After EMI",
                    f"₹{result['surplus_after_emi']:,}"
                )

            if result["cash_flow_status"] == "Positive":

                st.success(
                    "Cash flow remains positive after the estimated EMI."
                )

            else:

                st.warning(
                    "The estimated EMI would put pressure on "
                    "monthly cash flow."
                )

    else:

        st.warning(
            "Please add and select a store first."
        )

    # ---------------------------------------------------------
    # GST
    # ---------------------------------------------------------

    with st.expander("🧾 GST — View Details"):

        st.markdown("### 🧾 GST Information by Business Sector")

        gst_file = Path("gst_file.csv")

        if gst_file.exists():

            gst_df = pd.read_csv(gst_file)

            sector = st.selectbox(
                "Select Business Sector",
                gst_df["Business Sector"].tolist(),
                key="gst_sector"
            )

            selected = gst_df[
                gst_df["Business Sector"] == sector
            ].iloc[0]

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Primary GST Rate",
                    f"{selected['Primary GST Rate (%)']}%"
                )

                st.write(
                    f"**Registration Threshold:** "
                    f"{selected['Registration Threshold']}"
                )

                st.write(
                    f"**SAC/HSN Code Range:** "
                    f"{selected['SAC/HSN Code Range']}"
                )

            with col2:
                st.write(
                    f"**Primary Return Form:** "
                    f"{selected['Primary Return Form']}"
                )

            st.divider()

            st.markdown("#### 📋 Complete GST Dataset")

            st.dataframe(
                gst_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.error(
                "GST dataset not found. Put "
                "gst_file.csv "
                "in the same folder as app.py."
            )
    # ---------------------------------------------------------
    # LOCAL TRADE LICENSE
    # ---------------------------------------------------------

    with st.expander("🏪 Local Trade License — View Details"):

        st.markdown("### Local Trade License")

        st.write(
            "Some businesses may require local registrations, "
            "licenses or permissions depending on their location "
            "and business activity."
        )

        st.write("**Business Action:**")
        st.write(
            "Check the requirements applicable to your local "
            "municipal authority and type of business."
        )

        st.warning(
            "Local requirements can vary by location and business activity."
        )

    # ---------------------------------------------------------
    # TAX COMPLIANCE
    # ---------------------------------------------------------

    with st.expander("💰 Tax Compliance — View Details"):

        st.markdown("### Tax Compliance")

        st.write(
            "Businesses should maintain appropriate income, "
            "expense and transaction records."
        )

        st.write("**Business Action:**")

        st.write(
            "Keep sales, purchase, expense and other relevant "
            "financial records organized."
        )

        st.write(
            "Applicable tax registration, payment and filing "
            "requirements depend on the business and current rules."
        )

    # ---------------------------------------------------------
    # INVOICING
    # ---------------------------------------------------------

    with st.expander("📄 Invoice & Record Keeping — View Details"):

        st.markdown("### Invoice & Record Keeping")

        st.write(
            "Maintain proper invoices, purchase records, sales "
            "records and expense documents."
        )

        st.write("**Benefits:**")

        st.write(
            "Good record keeping can support accounting, tax "
            "compliance and financial planning."
        )

    st.divider()

    st.warning(
        "Compliance requirements can change. Always verify current "
        "requirements with the relevant official government authority "
        "or a qualified professional."
    )

# =========================================================
# LOANS
# =========================================================

elif page == "🏦 Loans & Funding":

    st.markdown("## 🏦 Loans & Funding")

    st.write(
        "Evaluate loan affordability before taking a business loan."
    )

    loan_amount = st.number_input(
        "Desired Loan Amount",
        min_value=0,
        value=500000,
        step=50000
    )

    interest_rate = st.number_input(
        "Expected Annual Interest Rate (%)",
        min_value=0.0,
        value=12.0,
        step=0.5
    )

    tenure = st.number_input(
        "Tenure (Years)",
        min_value=1,
        value=5,
        step=1
    )

    monthly_rate = interest_rate / 12 / 100
    months = tenure * 12

    if monthly_rate > 0:

        emi = (
            loan_amount
            * monthly_rate
            * (1 + monthly_rate) ** months
            / ((1 + monthly_rate) ** months - 1)
        )

    else:
        emi = loan_amount / months

    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Estimated EMI",
        f"₹{emi:,.0f}"
    )

    col2.metric(
        "Current Surplus",
        f"₹{surplus:,}"
    )

    remaining = surplus - emi

    col3.metric(
        "Surplus After EMI",
        f"₹{remaining:,.0f}"
    )

    if remaining > 0:
        st.success(
            "The scenario leaves a positive estimated monthly surplus. "
            "This is not a loan approval or recommendation."
        )
    else:
        st.warning(
            "This scenario may create significant pressure on monthly cash flow."
        )


# =========================================================
# BUSINESS EXPANSION
# =========================================================

elif page == "📈 Business Expansion":

    st.markdown("## 📈 Business Expansion")

    st.write(
        "Plan expansion based on your current business cash flow."
    )

    expansion_cost = st.number_input(
        "Estimated Expansion Cost",
        min_value=0,
        value=400000,
        step=50000
    )

    additional_revenue = st.number_input(
        "Expected Additional Monthly Revenue",
        min_value=0,
        value=60000,
        step=5000
    )

    additional_expenses = st.number_input(
        "Expected Additional Monthly Expenses",
        min_value=0,
        value=30000,
        step=5000
    )

    additional_profit = (
        additional_revenue - additional_expenses
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Expansion Cost",
        f"₹{expansion_cost:,}"
    )

    col2.metric(
        "Additional Monthly Revenue",
        f"₹{additional_revenue:,}"
    )

    col3.metric(
        "Estimated Additional Profit",
        f"₹{additional_profit:,}"
    )

    if additional_profit > 0:

        break_even = expansion_cost / additional_profit

        st.success(
            f"Estimated simple break-even: "
            f"approximately **{break_even:.1f} months**."
        )


# =========================================================
# DOCUMENTS
# =========================================================

elif page == "📄 Documents":

    st.markdown("## 📄 Documents")

    st.write(
        "Upload business documents. The AI agent can later extract "
        "information and prepare reports automatically."
    )

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "png", "jpg", "jpeg", "xlsx", "csv"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for file in uploaded_files:
            st.success(
                f"Uploaded: {file.name}"
            )


# =========================================================
# REPORTS
# =========================================================

elif page == "📊 Reports":

    st.markdown("## 📊 Reports")

    st.write(
        "Generate a business summary containing your financial health, "
        "loan analysis and growth opportunities."
    )

    if st.button("📄 Generate Business Report"):

        st.success(
            "Report generation started."
        )

        st.write(
            """
            Report will include:

            ✓ Business profile  
            ✓ Revenue & expenses  
            ✓ Business Health Score  
            ✓ Cash-flow summary  
            ✓ Loan scenario  
            ✓ Government scheme matches  
            ✓ Expansion analysis  
            ✓ AI recommendations
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "ASk Saathi AI • AI-powered business assistance for small businesses"
)