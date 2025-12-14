import streamlit as st
from app.data.users import login_user, register_user

st.set_page_config(
    page_title="Intelligence Platform",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = "user"


def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("## Multi-Domain Intelligence Platform")
        st.markdown("---")

        tab1, tab2 = st.tabs(["Login", "Register"])

        with tab1:
            st.subheader("Welcome Back")

            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)

                if submit:
                    if username == "" or password == "":
                        st.error("Username and password are required")
                    else:
                        result = login_user(username, password)

                        if type(result) == tuple:
                            success = result[0]
                            role = result[1]
                        else:
                            success = result
                            role = "user"

                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.session_state.role = role
                            st.success("Login successful")
                           
                        else:
                            st.error("Invalid username or password")

        with tab2:
            st.subheader("Create New Account")

            with st.form("register_form"):
                new_username = st.text_input("New Username")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                role = st.selectbox("Select Role", ["user", "analyst", "admin"])
                submit_reg = st.form_submit_button("Register", use_container_width=True)

                if submit_reg:
                    if new_username == "" or new_password == "" or confirm_password == "":
                        st.error("All fields are required")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        try:
                            result = register_user(new_username, new_password, role)
                        except TypeError:
                            result = register_user(new_username, new_password)

                        if type(result) == tuple:
                            created = result[0]
                            message = result[1]
                        else:
                            created = result
                            message = "Account created"

                        if created:
                            st.success(message)
                        else:
                            st.error(message)


def main():
    if st.session_state.logged_in:
        st.success("Login successful, open Dashboard from the sidebar.")
        st.write("Username:", st.session_state.username)
        st.write("Role:", st.session_state.role)
    else:
        login_page()

if __name__ == "__main__":
    main()
