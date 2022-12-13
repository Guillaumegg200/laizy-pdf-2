import streamlit as st

from streamlit_app import *
try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')


if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']

    st.header('VIA application 🎓')
    st.sidebar.markdown("# VIA application 🎓")

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar')


    st.markdown('- Dezip the folder that you have downloaded \n  ')

    link='[link](https://www.robots.ox.ac.uk/~vgg/software/via/via.html)'

    st.markdown("Open VIA with this " + link ,unsafe_allow_html=True)

    st.markdown('- Upload the json file called "via_label_project_pdf.json" \n - Upload the images in the folder \n - Correct the labels and try to not reshape boxes \n - Once done, download annotations as json file \n - Upload this json file into  ')

    st.markdown('Upload this json file that you downloaded them from VIA')

    if st.button('Go there 📍'):
        nav_page('upload_json')

    link='[link](https://www.robots.ox.ac.uk/~vgg/software/via/via.html)'

    st.markdown("Open a new VIA tab with this " + link ,unsafe_allow_html=True)

    st.markdown( ' - Upload the json file called "via_detector_project_pdf.json" \n  - Upload again the images \n - Reshape the boxes to get items and sections \n - You have to go on VIA website first \n - Once done, download annotations as json file ')

    st.markdown('Upload this other json file that you downloaded them from VIA')

    if st.button('Go there (again)📍'):
        nav_page('upload_json')

    st.subheader("Watch a tutorial")
else:
    nav_page('')
