import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
from utils import *
from modify_via_json import *
import time
from via_json import *
from modify_via_json import *
from streamlit.components.v1 import html
from manage_dataset import *
from streamlit_auth.authentification import *
import streamlit_authenticator as stauth
import yaml
from yaml import SafeLoader

# [theme]
# primaryColor="#fff7f6"
# backgroundColor="#06173e"
# secondaryBackgroundColor="#e8959e"
# textColor="#ffffff"


#streamlit run streamlit_app.py



with open('./streamlit_auth/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

#name, authentication_status, username = authenticator.login("Login", "main")
username = 'ggg'
authentication_status = True
st.session_state['username'] = username

username_list = {}
for i,username_temp in enumerate(config['credentials']['usernames'].keys()):
    username_list[username_temp] = str(i)

st.session_state['authentication_status'] = authentication_status

if authentication_status== False:
    st.session_state['authentication_status'] = authentication_status
    st.error("Username or password is incorrect")

    #Commented next lines because we could add the possibilty to send an email if the password or username is incorrect




    # if st.button("I forgot my password") or 'forgotpassword' in st.session_state:
    #     st.session_state['forgotpassword'] = True
    #     try:
    #         username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    #         if username_forgot_pw:

    #             st.success('New password sent securely')
    #             del st.session_state['forgotpassword']
    #             nav_page('')
    #             # Random password to be transferred to user securely
    #         elif username_forgot_pw == False:
    #             st.error('Username not found')
    #     except Exception as e:
    #         st.error(e)
    # if st.button("I forgot my username") or 'forgotusername' in st.session_state:
    #     st.session_state['forgotusername'] = True
    #     try:
    #         username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    #         if username_forgot_username:
    #             st.success('Username sent securely')
    #             del st.session_state['forgotusername']
    #             # Username to be transferred to user securely
    #         elif username_forgot_username == False:
    #             st.error('Email not found')
    #     except Exception as e:
    #         st.error(e)

elif authentication_status == None:
    st.session_state['authentication_status'] = authentication_status
    st.warning("Please enter your username and password")

elif authentication_status:
    st.session_state['authentication_status'] = authentication_status
    st.session_state['folder'] = './temp' + username_list[st.session_state['username']]
    folder_temp = st.session_state['folder']
    st.session_state['zip_name'] = 'via_files' + username_list[st.session_state['username']] + '.zip'
    
    st.title('LAIzy PDF 💡')
    st.markdown('This is a web app to read PDF menus ')

    st.sidebar.markdown("# Main page ")
    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    if authenticator.logout('Logout', 'sidebar'):
        del st.session_state['username']
    # video_file = open('./Video/short_demo_x2.mp4', 'rb')
    # video_bytes = video_file.read()

    # st.video(video_bytes)

    if st.button('Click here to start 🎈'):
        if os.path.exists(folder_temp):
            shutil.rmtree(folder_temp)
        nav_page("upload_pdf")
    st.subheader('Watch our video 📽️')








