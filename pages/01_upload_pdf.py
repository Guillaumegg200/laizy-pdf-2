import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')

if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']
    st.markdown("# Upload PDF 📄")
    st.sidebar.markdown("# Upload PDF page ")

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)
    authenticator.logout('Logout', 'sidebar')


    if not os.path.exists(folder_temp):
        # Create file uploader object
        upload_file = st.file_uploader('Upload a PDF containing a menu')
        if upload_file is not None:
            if os.path.exists(folder_temp):
                shutil.rmtree(folder_temp)
            os.makedirs(folder_temp)
            with open(folder_temp + '/' + upload_file.name, 'wb') as f:
                f.write(upload_file.getvalue())
            pdf_path = folder_temp + '/' + upload_file.name
            pdf_to_image_from_path(root_name =get_file_name(pdf_path),input_path = pdf_path,output_path = folder_temp )
            # Display PDF pages
            image_list = [Image.open(filename) for filename in glob.glob(folder_temp + '/*.jpg') if 'test.jpg' not in filename ]
            st.image(image_list, use_column_width=True, caption=["menu page"] * len(image_list))

            with st.spinner('We are processing your images...'):
                save_via_folder_projet(pdf_path = pdf_path,output_path =folder_temp)
                username_list[username_temp]
                create_folder_zip(folder_temp,st.session_state['zip_name'])

                st.success('Done!')
            
            # Create a section for download json
            st.subheader('Look at what we have so far !')
            image_labels_draw_list = draw_boxes_from_json(folder_temp,folder_temp + '/via_label_project_pdf.json')
            st.image(image_labels_draw_list, use_column_width=True, caption=["menu page after detection"] * len(image_labels_draw_list))
            image_detector_draw_list = draw_boxes_from_json(folder_temp,folder_temp + '/via_detector_project_pdf.json')
            st.image(image_detector_draw_list, use_column_width=True, caption=["menu page after detection"] * len(image_detector_draw_list))

            nav_page('upload_pdf')

    else:
        if st.button('Upload a new PDF')or 'uploadpdf' in st.session_state:
            st.session_state['uploadpdf'] = True
            st.error("Do you really, really, wanna do this?")
            if st.button("Yes"):
                shutil.rmtree(folder_temp)
                del st.session_state["uploadpdf"]
                nav_page('upload_pdf')
            if st.button("No"):
                del st.session_state["uploadpdf"]
                nav_page('upload_pdf')

    
        
        # Display PDF pages
        image_list = [Image.open(filename) for filename in glob.glob(folder_temp + '/*.jpg')]
        st.image(image_list, use_column_width=True, caption=["menu page"] * len(image_list))
        
        # Display images with boxes
        st.subheader('Look at what we have so far !')
        image_labels_draw_list = draw_boxes_from_json(folder_temp,folder_temp + '/via_label_project_pdf.json')
        st.image(image_labels_draw_list, use_column_width=True, caption=["menu page after detection"] * len(image_labels_draw_list))
        image_detector_draw_list = draw_boxes_from_json(folder_temp,folder_temp + '/via_detector_project_pdf.json')
        st.image(image_detector_draw_list, use_column_width=True, caption=["menu page after detection"] * len(image_detector_draw_list))

        if st.button('Go there to download your ZIP 📍'):
            nav_page('download_zip')
else:
    nav_page('')