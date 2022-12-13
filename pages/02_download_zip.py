import streamlit as st

from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')

if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']
    st.markdown("# Download zip folder 💥")
    st.sidebar.markdown("# Download page 💥")
    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar')

    if os.path.exists(folder_temp):
        pdf_name = get_file_name([pdf for pdf in glob.glob(folder_temp + '/**.pdf')][0])
        # Create a section for download json
        st.markdown('In this folder you have : \n - Your pdf pages as images \n - 2 json files. \n You have to upload those json files into VIA application in 2 different tabs')
        with open(st.session_state['zip_name'], "rb") as fp:
            st.download_button( label="Download ZIP", data=fp, file_name= pdf_name + ".zip", mime="application/zip" )
        st.subheader("Read the VIA tutorial 📖")
        if st.button('Go there 	📍'):
            nav_page('via_tutorial')

    else:
        st.warning('You need to upload a PDF', icon="⚠️")
        if st.button('Go there 	📍'):
            nav_page('upload_pdf')
else:
    nav_page('')