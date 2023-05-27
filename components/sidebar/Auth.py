import pyrebase
import streamlit as st
import os
import re
from dotenv import load_dotenv
load_dotenv()

config = {
    "apiKey": st.secrets['FIREBASE_API'] if not os.getenv("FIREBASE_API") else os.getenv("FIREBASE_API"),
    "authDomain": "pdf-assistant-streamlit.firebaseapp.com",
    "projectId": "pdf-assistant-streamlit",
    "storageBucket": "pdf-assistant-streamlit.appspot.com",
    "databaseURL": "https://pdf-assistant-streamlit-default-rtdb.firebaseio.com/",
    "messagingSenderId": "327866675115",
    "appId": "1:327866675115:web:515fb66ac21218531bacee",
    "measurementId": "G-408449KY82",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

def upload_data(uid, data, pdf_file):
    pdf_files = db.child("users").child(uid).child("pdf_files").get().val()

    if pdf_files is None or pdf_file not in pdf_files:
        structure = {
            pdf_file: {
                "Current Prompt": 1,
                "Prompts": {
                    "Prompt 1": data
                }
            }
        }
        db.child("users").child(uid).child("pdf_files").update(structure)
    else:
        current_prompt = db.child("users").child(uid).child("pdf_files").child(pdf_file).child("Current Prompt").get().val()

        current_prompt = int(current_prompt) + 1 if current_prompt is not None else 1
        
        new_structure = {
            f"Prompt {current_prompt}": data
        }

        db.child("users").child(uid).child("pdf_files").child(pdf_file).child("Prompts").update(new_structure)
        db.child("users").child(uid).child("pdf_files").child(pdf_file).child("Current Prompt").set(current_prompt)


def login_using_email_and_password(email, password):
    try:
        st.write("Logging in...")
        user = auth.sign_in_with_email_and_password(email, password)
        username = db.child("users").child(user["localId"]).child('user_data').get().val()['username']
        st.session_state['username'] = username
        st.session_state['logged_in'] = True
        st.session_state['uuid'] = user["localId"]
        st.session_state['login_failed'] = False
        return
    except Exception as e:
        st.session_state['login_failed'] = True
        st.session_state['login_exception'] = e
        return


def signup_using_email_and_password(email, password, username):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        user = auth.sign_in_with_email_and_password(email, password)
        
        db.child("users").child(user["localId"]).child("user_data").set(
            {
                "username": username.upper(),
                "email": email,
                "password": password,
                "uid": user["localId"],
            }
        )
        st.success(f"Successfully registered with username: {username.upper()}")
        st.session_state['logged_in'] = True
        st.session_state['username'] = username.upper()
        st.session_state['email'] = email
        st.session_state['uuid'] = user['localId']
        return
    
    except Exception as e:
        st.session_state['login_failed'] = True
        st.session_state['login_exception'] = e
        return
    
    
def authentication_comp():
    st.write('#### 🔐 Accounts')
    login_tab, signup_tab = st.tabs(["Login", "Signup"])
    with login_tab:
        login_mail = st.text_input("Email", key="login_mail", placeholder="Enter your email")

        if st.session_state['login_btn_clicked'] == True and login_mail == "":
            st.caption(":red[Please enter your email]")

        if st.session_state['login_btn_clicked'] == True and st.session_state['login_failed'] == True:
            if "INVALID_EMAIL" in str(st.session_state['login_exception']):
                st.caption(":red[Invalid email]")
                st.session_state['login_failed'] = False
            elif "EMAIL_NOT_FOUND" in str(st.session_state['login_exception']):
                st.caption(":red[Email not found]")
                st.session_state['login_failed'] = False

        login_pwd = st.text_input("Password", type="password", key="login_pwd", placeholder="Enter your password")


        if st.session_state['login_btn_clicked'] == True and login_pwd == "":
            st.caption(":red[Please enter your password]")

        if st.session_state['login_btn_clicked'] == True and st.session_state['login_failed'] == True:
            if "INVALID_PASSWORD" in str(st.session_state['login_exception']):
                st.caption(":red[Invalid password]")
                st.session_state['login_failed'] = False

        login_btn = st.button("Login 🔓")

        if login_btn:
            st.session_state['login_btn_clicked'] = True

            if login_mail == "" and login_pwd == "": # both empty
                st.error("Please enter your email and password")

            elif login_mail == "": # only email empty
                st.error("Please enter your email")

            elif login_pwd == "": # only password empty
                st.error("Please enter your password")

            else:
                login_using_email_and_password(login_mail, login_pwd)                
                st.button("dummy", on_click=st.experimental_rerun())

    with signup_tab:
        signup_username = st.text_input("Username", key="signup_username", placeholder="Username")
        if st.session_state.get('signup_btn_clicked') == True and signup_username == "":
            st.caption(":red[Please enter your username]")

        signup_mail = st.text_input("Email", key="signup_mail", placeholder="Enter your email")
        
        if signup_mail != "" and not re.match(r"[^@]+@[^@]+\.[^@]+", signup_mail): # email validation
            st.caption(":red[Invalid email address]")
        
        if st.session_state.get('signup_btn_clicked') == True and signup_mail == "": # if signup button is clicked and email is empty
            st.caption(":red[Please enter your email]")

        signup_pwd = st.text_input("Password", type="password", key="signup_pwd", placeholder="Enter your password") # password input
        
        if len(signup_pwd) >= 1 and len(signup_pwd) < 6: # if password is less than 6 characters
            st.caption(":red[Password must be at least 6 characters long.]")

        if st.session_state.get('signup_btn_clicked') == True and signup_pwd == "": # if signup button is clicked and password is empty
            st.caption(":red[Please enter your password]")

        confirm_pwd = st.text_input("Confirm Password", type="password", key="confirm_pwd", placeholder="Confirm your password") # confirm password input
        if st.session_state.get('signup_btn_clicked') == True and confirm_pwd == "": # if signup button is clicked and confirm password is empty
            st.caption(":red[Please confirm your password]")
            
        if 'signup_btn_clicked' not in st.session_state: # if signup button is not clicked
            if len(signup_pwd) >= 1 and len(signup_pwd) >= 6 and len(confirm_pwd) >= 1 and signup_pwd != confirm_pwd: # if password is not empty and confirm password is not empty and passwords do not match
                st.caption(":red[Passwords do not match]")
                
        if st.session_state.get('signup_btn_clicked') == True and signup_pwd != confirm_pwd: # if signup button is clicked and passwords do not match
            st.caption(":red[Passwords do not match]")

        signup_btn = st.button("Sign Up and Login 🔓", disabled=len(signup_pwd) >= 1 and len(signup_pwd) < 6)
        if signup_btn:
            st.session_state['signup_btn_clicked'] = True

            if signup_username == "" and signup_mail == "" and signup_pwd == "" and confirm_pwd == "": # if all fields are empty
                st.error("Please enter your username, email and password")

            elif signup_username == "": # if username is empty
                st.error("Please enter your username")

            elif signup_mail == "": # if email is empty
                st.error("Please enter your email")

            elif signup_pwd == "": # if password is empty
                st.error("Please enter your password")

            elif len(signup_pwd) < 6: # if password is less than 6 characters
                st.error("Password must be at least 6 characters long")

            elif confirm_pwd == "": # if confirm password is empty
                st.error("Please confirm your password")

            elif signup_pwd != confirm_pwd: # if passwords do not match
                st.error("Passwords do not match")
                
            else:
                with st.spinner("Signing up..."):
                    signup_using_email_and_password(signup_mail, signup_pwd, signup_username)
                    st.button("dummy", on_click=st.experimental_rerun())

    st.caption(":green[Login or Register to save your Prompts/Responses and to view your History]")
    
if __name__ == "__main__":
    authentication_comp()