import streamlit as st

from database import (
    create_user,
    login_user
)


def show_login():

    st.markdown(
        """
        <div style="text-align:center;">
            <h1>🤝</h1>
            <p>Your AI Business Partner</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.user_name = user[1]
                st.session_state.user_email = user[2]

                st.rerun()

            else:

                st.error(
                    "Invalid email or password."
                )

    with signup_tab:

        name = st.text_input(
            "Your Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.warning(
                    "Please fill all fields."
                )

            else:

                success, message = create_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)