import streamlit as st
import pyrebase
import time
from streamlit_extras.let_it_rain import rain

firebaseConfig = {"apiKey": "AIzaSyAZK8DOoRPr2s8kEbljuOiccBm7tUJTvwk",
                "authDomain": "webappdb-34850.firebaseapp.com",
                "projectId": "webappdb-34850",
                "storageBucket": "webappdb-34850.appspot.com",
                "messagingSenderId": "518870328019",
                "appId": "1:518870328019:web:7b782bb7d54ed27da2ea26",
                "measurementId": "G-NN7XDB415Z",
                "databaseURL": "https://webappdb-34850-default-rtdb.asia-southeast1.firebasedatabase.app/",
                }
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def get_user_session_state():
    return st.session_state.get("user")

def MAINPAGE():
    st.title("Welcome to :orange[EnhanceAI] 🐱‍💻✨")
    st.header("Elevating :blue[Visual Excellence] with :orange[Artificial Intelligence]")
    st.subheader("👨🏻‍💻 Account Management: ")
    
    user = st.session_state.get("user")
    st.write(f"Logged in as: {user['email']}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Reset Password", use_container_width=True):
            st.session_state["page"] = "reset"
            st.rerun()
    with col2:
        if st.button("Delete Account", use_container_width=True):
            st.session_state["page"] = "delete"
            st.rerun()
    with col3:
        if st.button("Log Out", use_container_width=True):
            st.session_state["page"] = "confirmation"
            st.rerun()

def REGISTER():
    st.title("Welcome to :orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Register New Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Second Password", type="password")

    col1, col2 = st.columns(2)
    with col1:
        register = st.button("Register", use_container_width=True)
    with col2:
        login = st.button("Log In", use_container_width=True)

    if register:
        if email == "":
            st.warning("Enter Email!")
        elif password == "":
            st.warning("Enter Password!")
        elif confirm_password == "":
            st.warning("Enter Confirm Password!")
        elif password != confirm_password:
            st.warning("Password doesn't match!")
        elif password == confirm_password:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                auth.send_email_verification(user['idToken'])
                st.success("Account registered succesfully!")
                st.session_state["page"] = "login"
                rain(
                    emoji="🎇",
                    font_size=54,
                    falling_speed=5,
                    animation_length="infinite",
                )
                with st.spinner('Redirecting to login page...'):
                    time.sleep(1)
                st.success('Done!')
            except:
                st.warning("Account registration failed!")
                time.sleep(1)
            st.rerun()
    elif login:
        st.session_state["page"] = "login"
        st.rerun()

def LOGIN():
    st.title("Welcome to :orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Login Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2, col3= st.columns(3)
    with col1:
        login = st.button("Login", use_container_width=True)
    with col2:
        forgot = st.button("Forgot Password", use_container_width=True)
    with col3:
        register = st.button("Register", use_container_width=True)

    if login:
        if email == "":
            st.warning("Enter Email!")
        elif password == "":
            st.warning("Enter Password!")
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                auth.refresh(user['refreshToken'])
                st.success("Account login successfully!")
                st.session_state["user"] = user
                st.session_state["page"] = "mainpage"
                rain(
                    emoji="😸",
                    font_size=54,
                    falling_speed=5,
                    animation_length="infinite",
                )
                with st.spinner('Redirecting to main page...'):
                    time.sleep(1)
                st.success('Done!')
            except:
                st.warning("Account login failed!")
                time.sleep(1)
            st.rerun()
    elif forgot:
        st.session_state["page"] = "forgot"
        st.rerun()
    elif register:
        st.session_state["page"] = "register"
        st.rerun()

def RESET():
    st.title(":orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Password Reset")
    email = st.text_input("Email")

    col1, col2 = st.columns(2)
    with col1:
        reset = st.button("Reset Password", use_container_width=True)
    with col2:
        back = st.button("Back", use_container_width=True)

    if reset:
        if email == "":
            st.warning("Enter Email!")
        elif email != "":
            try:
                auth.send_password_reset_email(email)
                st.success("Password reset email sent successfully!")
                st.session_state["page"] = "mainpage"
                rain(
                    emoji="📩",
                    font_size=54,
                    falling_speed=5,
                    animation_length="infinite",
                )
                with st.spinner('Redirecting to main page...'):
                    time.sleep(1)
                st.success('Done!')
            except:
                st.warning("Password reset failed!")
                time.sleep(1)
            st.rerun()
    elif back:
        st.session_state["page"] = "mainpage"
        st.rerun()

def FORGOT():
    st.title(":orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Password Reset")
    email = st.text_input("Email")

    col1, col2 = st.columns(2)
    with col1:
        reset = st.button("Reset Password", use_container_width=True)
    with col2:
        back = st.button("Back", use_container_width=True)

    if reset:
        if email == "":
            st.warning("Enter Email!")
        elif email != "":
            try:
                auth.send_password_reset_email(email)
                st.success("Password reset email sent successfully!")
                st.session_state["page"] = "login"
                rain(
                    emoji="📩",
                    font_size=54,
                    falling_speed=5,
                    animation_length="infinite",
                )
                with st.spinner('Redirecting to main page...'):
                    time.sleep(1)
                st.success('Done!')
            except:
                st.warning("Password reset failed!")
                time.sleep(1)
            st.rerun()
    elif back:
        st.session_state["page"] = "login"
        st.rerun()

def DELETE():
    user = st.session_state["user"]
    st.title(":orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Delete Account")
    st.write("To continue, type: 'I want to delete my account'")
    delete = st.text_input("Type: ")
    
    col1, col2 = st.columns(2)
    with col1:
        submit = st.button("Delete Account", use_container_width=True)
    with col2:
        back = st.button("Back", use_container_width=True)

    if submit:
        if delete != "I want to delete my account":
            st.warning("Check for typo(s)!")
        elif delete == "I want to delete my account":
            try:
                auth.delete_user_account(user['idToken'])
                st.success("Acount deleted successfully!")
                st.session_state["page"] = "login"
                rain(
                    emoji="😿",
                    font_size=54,
                    falling_speed=5,
                    animation_length="infinite",
                )
                with st.spinner('Redirecting to login page...'):
                    time.sleep(1)
                st.success('Done!')
            except:
                st.warning("Account Deletion Failed!")
                time.sleep(1)
            st.rerun()
    elif back:
        st.session_state["page"] = "mainpage"
        st.rerun()

def CONFIRMATION():
    st.title(":orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("Are you sure want to log out?")
    col1, col2 = st.columns(2)
    with col1:
        confirm = st.button("Yes", use_container_width=True)
    with col2:
        back = st.button("Back", use_container_width=True)
    if confirm:
        st.session_state["user"] = "user"
        st.session_state["page"] = "logout"
        st.rerun()
    elif back:
        st.session_state["page"] = "mainpage"
        st.rerun()

def LOGOUT():
    st.title(":orange[EnhanceAI] 🐱‍💻✨")
    st.subheader("You have been log out!")
    st.session_state["page"] = "login"
    rain(
            emoji="👋🏻",
                font_size=54,
                falling_speed=5,
                animation_length="infinite",
            )
    with st.spinner('Redirecting to login page...'):
        time.sleep(1)
    st.success('Done!')
    st.rerun()

def app():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    if "user" not in st.session_state:
        st.session_state["user"] = "user"

    if st.session_state["page"] == "login":
        LOGIN()
    elif st.session_state["page"] == "register":
        REGISTER()
    elif st.session_state["page"] == "mainpage":
        MAINPAGE()
    elif st.session_state["page"] == "reset":
        RESET()
    elif st.session_state["page"] == "forgot":
        FORGOT()
    elif st.session_state["page"] == "delete":
        DELETE()
    elif st.session_state["page"] == "confirmation":
        CONFIRMATION()
    elif st.session_state["page"] == "logout":
        LOGOUT()
    
    
    
