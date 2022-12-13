import streamlit as st
from streamlit_app import *

try:
    if st.session_state['authentication_status']:
        print('ok')
except KeyError as error:
    nav_page('')
    
if st.session_state['authentication_status']:
    folder_temp = st.session_state['folder']
    st.markdown("# Upload VIA json files 	💫")
    st.sidebar.markdown("# Upload json page 💫 ")

    my_logo = add_logo(logo_path="./streamlit_images/meandu-logo-red.png", width=50, height=50)
    st.sidebar.image(my_logo)

    authenticator.logout('Logout', 'sidebar')

    link='[link](https://www.robots.ox.ac.uk/~vgg/software/via/via.html)'

    st.markdown("Open VIA with this " + link ,unsafe_allow_html=True)

    # Create a section for upload
    if os.path.exists(folder_temp):
        if not os.path.exists(folder_temp +'/menu_template.xlsx'):
            # Create file uploader object
            upload_json_label_file = st.file_uploader('Upload json file with the label annotations')
            st.warning('Be careful this is the one with  price, name, description ...')
            if upload_json_label_file is not None and 'json_label_uploaded' not in st.session_state:
                with st.spinner('We are processing your files...'):
                    via_label_json_dict = json.load(upload_json_label_file)
                    dict_df_labels  = read_text_via(folder_temp,via_label_json_dict)
                    st.session_state['json_label_uploaded'] = dict_df_labels
            
            if 'json_label_uploaded' in st.session_state:
                st.success('Great the first one has been processed !')
                upload_json_detector_file = st.file_uploader('Upload json file with detector annotations')
                st.warning('Be careful this is the one with section and item ...')
                if upload_json_detector_file is not None:
                    flag = False
                    st.error('Can we save your files to train the model ?')
                    st.warning("We need a good accuracy  !!!", icon="⚠️")
                    #Check if the PDF is already in the database
                    for filename in os.listdir(folder_temp):
                        file_path = os.path.join(folder_temp, filename)
                        if filename.endswith(".pdf") and os.path.exists(os.path.join('./detector/History/PDF',filename)):
                            flag = True
                    # If the PDF not in history
                    if not flag:        
                        if st.button('No'):
                            with st.spinner('We are processing your files...'):
                                dict_df_labels = st.session_state['json_label_uploaded']
                                # Create file uploader object
                                via_detector_json_dict = json.load(upload_json_detector_file)
                                dict_item_boxes = get_item_boxes(via_detector_json_dict)
                                dict_section_boxes = get_section_boxes(via_detector_json_dict)        
                                group_item(folder_temp,dict_df_labels,dict_item_boxes,dict_section_boxes)
                                st.success('Done!')
                                del st.session_state['json_label_uploaded']
                            nav_page('download_excel')
                        if st.button('Yes'):
                            via_detector_json_dict = json.load(upload_json_detector_file)
                            dict_item,dict_section = split_json_detector(via_detector_json_dict)
                            via_label_json_dict = json.load(upload_json_label_file)

                            # To keep an history

                            dict = {'item':dict_item,'section':dict_section,'label':via_label_json_dict}

        
                            if len(os.listdir('./detector/History/val'))< 0.22 * len(os.listdir('./detector/History/train')):
                                for type in ['item','section','label']:
                                # Opening JSON file
                                    data_train =json.load( open('./detector/History/via_' + type + '_train.json'))
                                    data_val = json.load(open('./detector/History/via_' + type + '_val.json'))

                                    via_project = join_via_json_project(data_val,via_annotation_to_project(dict[type]))
                                    json_object = json.dumps(via_project, indent=0,separators=  (',',':') )
                                    with open('./detector/History/via_' + type + '_val.json', "w") as outfile:
                                        outfile.write(json_object)
                                for filename in os.listdir(folder_temp):
                                    file_path = os.path.join(folder_temp, filename)
                                    if filename.endswith(".pdf"):
                                        print('pdf',filename)
                                        shutil.copyfile(file_path, os.path.join('./detector/History/PDF',filename))
                                    # checking if it is a file
                                    if 'jpg' in file_path or 'png' in file_path and "test.jpg" not in file_path:
                                        shutil.copyfile(file_path, os.path.join('./detector/History/Images val', filename))
                                        shutil.copyfile(file_path, os.path.join('./detector/History/Images', filename))
                                        green_merge = detector_image_transformation_from_path(file_path)
                                        green_merge.save(os.path.join('./detector/History/val', filename)) 
                            else:
                                for type in ['item','section','label']:
                                    data_train =json.load( open('./detector/History/via_' + type + '_train.json'))
                                    data_val = json.load(open('./detector/History/via_' + type + '_val.json'))
                                    via_project = join_via_json_project(data_train,via_annotation_to_project(dict[type]))
                                    json_object = json.dumps(via_project, indent=0,separators=  (',',':') )
                                    # Writing to sample.json
                                    with open('./detector/History/via_' + type + '_train.json', "w") as outfile:
                                        outfile.write(json_object)
                                for filename in os.listdir(folder_temp):
                                    file_path = os.path.join(folder_temp, filename)
                                    if filename.endswith(".pdf"):
                                        print('pdf',filename)
                                        shutil.copyfile(file_path, os.path.join('./detector/History/PDF',filename))
                                    # checking if it is a file
                                    if 'jpg' in file_path or 'png' in file_path and "test.jpg" not in file_path:
                                        shutil.copyfile(file_path, os.path.join('./detector/History/Images train', filename))
                                        shutil.copyfile(file_path, os.path.join('./detector/History/Images', filename))
                                        green_merge = detector_image_transformation_from_path(file_path)
                                        green_merge.save(os.path.join('./detector/History/train', filename))
                    
                            with st.spinner('We are processing your files...'):
                                dict_df_labels = st.session_state['json_label_uploaded']
                                # Create file uploader object
                                # via_detector_json_dict = json.load(upload_json_detector_file)
                                dict_item_boxes = get_item_boxes(via_detector_json_dict)
                                dict_section_boxes = get_section_boxes(via_detector_json_dict)        
                                group_item(folder_temp,dict_df_labels,dict_item_boxes,dict_section_boxes)
                                st.success('Done!')
                                del st.session_state['json_label_uploaded']
                            nav_page('download_excel')
                    else:  
                        with st.spinner('We are processing your files...'):
                            dict_df_labels = st.session_state['json_label_uploaded']
                            # Create file uploader object
                            via_detector_json_dict = json.load(upload_json_detector_file)
                            dict_item_boxes = get_item_boxes(via_detector_json_dict)
                            dict_section_boxes = get_section_boxes(via_detector_json_dict)        
                            group_item(folder_temp,dict_df_labels,dict_item_boxes,dict_section_boxes)
                            st.success('Done!')
                            del st.session_state['json_label_uploaded']
                        nav_page('download_excel')
                
                    
        else:
            st.markdown('You have already upload json files so go on the next page to download your excel')
            if st.button('Go there 	📍'):
                nav_page('download_excel')
            if st.button('Upload new json files') or  "uploadjson" in st.session_state:
                st.session_state['uploadjson'] = True
                st.error("Do you really, really, wanna do this?")
                if st.button("Yes"):
                    os.remove(folder_temp + '/menu_template.xlsx')
                    del st.session_state['uploadjson']
                    nav_page('upload_json')
                if st.button("No"):
                    del st.session_state['uploadjson']
                    nav_page('upload_json')
    else:
        st.warning('You need to upload a PDF', icon="⚠️")
        if st.button('Go there 	📍'):
            nav_page('upload_pdf')
else:
    nav_page('')