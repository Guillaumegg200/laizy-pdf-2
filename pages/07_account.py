
import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')



if st.session_state['authentication_status']:
    with open('./streamlit_auth/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    name = config['credentials']['usernames'][st.session_state['username']]['name']
    email = config['credentials']['usernames'][st.session_state['username']]['email']

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar') 


    st.header('Your account')
    st.write("Name : " + name)
    st.write("Username : " + st.session_state['username'])
    st.write("Email : " + email)
    if st.button('Update details') or 'updateyourdetail' in st.session_state:
        st.session_state['updateyourdetail'] = True
        try:
            if authenticator.update_user_details(st.session_state['username'], 'Update your details'):
                st.success('Entries updated successfully')
                with open('./streamlit_auth/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                del st.session_state['updateyourdetail'] 
                nav_page('account')
        except Exception as e:
            st.error(e)
    if st.button('Reset password') or 'resetyourpassword' in st.session_state:
        st.session_state['resetyourpassword'] = True
        try:     
            if authenticator.reset_password(st.session_state['username'], 'Reset password'):
                st.success('Password modified successfully')
                with open('./streamlit_auth/config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                del st.session_state['resetyourpassword']
                nav_page('account')
        except Exception as e:
            st.error(e)
            
else:
    nav_page('')