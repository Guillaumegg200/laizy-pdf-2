import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')



if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']
    st.markdown("# Settings page 💻 ")
    st.sidebar.markdown("# Settings page 💻")

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar')

    if not os.path.exists(folder_temp):
        st.warning('You need to upload a PDF ', icon="⚠️")
        if st.button('Go there 	📍'):
            nav_page("upload_pdf")
    else:
        st.markdown('Do you want to upload a new PDF ?')
        if st.button('Upload a new PDF') or 'settingsuploadpdf' in  st.session_state:
            st.session_state['settingsuploadpdf'] = True
            st.error("Do you really, really, wanna do this?")
            if st.button("Yes"):
                shutil.rmtree(folder_temp)
                del st.session_state['settingsuploadpdf']
                nav_page('upload_pdf')
            if st.button("No"):
                del st.session_state['settingsuploadpdf']
                nav_page('settings')

        if not os.path.exists(folder_temp + '/menu_template.xlsx'):
            st.warning('You need to upload json files', icon="⚠️")
            if st.button('Go there to download the zip file	📍'):
                nav_page("download_zip")
            if st.button('Go there to upload json files	📍'):
                nav_page("upload_json")
        else:
            st.markdown('Do you want to upload new json files ?')
    
            if st.button('Upload new json files') or 'settingsuploadjson' in st.session_state:
                st.session_state['settingsuploadjson'] = True
                st.error("Do you really, really, wanna do this?")
                if st.button("Yes"):
                    os.remove(folder_temp + '/menu_template.xlsx')
                    del st.session_state['settingsuploadjson']
                    nav_page("upload_json")
                if st.button("No"):
                    del st.session_state['settingsuploadjson']
                    nav_page("settings")
else:
    nav_page('')