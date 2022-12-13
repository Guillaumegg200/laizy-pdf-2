import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')

if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']
    st.markdown("# Download excel 🪄")
    st.sidebar.markdown("# Download excel page 🪄")

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar')


    if os.path.exists(folder_temp + '/menu_template.xlsx'):
        pdf_name = get_file_name([pdf for pdf in glob.glob(folder_temp + '/**.pdf')][0])
        df_menu =pd.read_excel(folder_temp + '/menu_template.xlsx')
        st.markdown('Download your final excel menu')
        user_input = st.text_input("How do you want to name your csv before downloading ? Don't forget .xlsx ", pdf_name + '.xlsx')
        with open(folder_temp + '/menu_template.xlsx', 'rb') as my_file:
            if st.download_button(label = 'Press to dowload your excel file', data = my_file, file_name = user_input, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):      
                st.success('Thank you for using me')
    else:
        if not os.path.exists(folder_temp):
            st.warning('You need to upload a PDF', icon="⚠️")
            if st.button('Go there 	📍'):
                nav_page("upload_pdf")
        else:
            st.warning('You need to upload the json files', icon="⚠️")
            if st.button('Go there 	📍'):
                nav_page("upload_json")
else:
    nav_page('')