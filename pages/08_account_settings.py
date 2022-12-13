
import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')
with open('./streamlit_auth/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

if st.session_state['authentication_status']:
    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar') 

    if st.session_state['username'] == 'ggg':

        st.header('All users accounts')
        if st.button("Manage user accounts") or 'manage' in st.session_state:
    
            st.session_state['manage'] = True
            # with open('./streamlit_auth/config.yaml') as file:
            #     config = yaml.load(file, Loader=SafeLoader)
            username_option = st.selectbox('Which account do you want to manage ?',tuple([username_t for username_t in config['credentials']['usernames'].keys() if username_t!=username]))
            user = config['credentials']['usernames'][username_option]
            name_option,email_option = user['name'],user['email']
            st.header('User account :')
            st.write("Name : " + name_option)
            st.write("Username : " + username_option)
            st.write('Email : ' + email_option)
            try:
                if authenticator.update_user_details(username_option, 'Update user details'):
                    st.success('Entries updated successfully')
                    with open('./streamlit_auth/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    del st.session_state['manage']
                    nav_page('account_settings')
            except Exception as e:
                st.error(e)

            try:     
                if authenticator.reset_password(username_option, 'Reset password of this user'):
                    st.success('Password modified successfully')
                    with open('./streamlit_auth/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    del st.session_state['manage']
                    nav_page('account_settings')
            except Exception as e:
                st.error(e)
            

        if st.button("Add user account") or 'add' in st.session_state:
            st.session_state['add'] = True
            try:
                if authenticator.register_user('Register new user', preauthorization=False):
                    st.success('User registered successfully')
                    with open('./streamlit_auth/config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
                    del st.session_state['add']
                    nav_page('account_settings')
            except Exception as e:
                st.error(e)
            
    else:
        st.warning('You do not have access to this page')
else:
    nav_page('')