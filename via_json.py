from utils import *
from detector.predict import *
import streamlit as st
from get_label import *

def via_detector_file_dict(img_path):
    """
    For an image return a dictionnary given the information for this image in the way of via displays it

    Input :
    - img_path : path of the image

    Output :
    -dict_file
    """
    
    
    img_name = img_path.split('/')[-1]
    size = os.stat(img_path).st_size

    img = detector_image_transformation(img_path)

    #Item

    
    #model.load_state_dict(torch.load(args_item["model"]))
    #model = torch.load(args_item["model"])
    model = torch.load(item_model)
    pred_boxes, _, _ = get_prediction(model,img, confidence=item_conf)
    pred_boxes = modify_pred_boxes(pred_boxes)
    regions = []
    for i,box in enumerate(pred_boxes):
        label = 'item'
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})   
    #Section
    model = torch.load(section_model)
    print(type(model))
    try:
        pred_boxes, _, _ = get_prediction(model,img, confidence=section_conf)
    except:
        pred_boxes = []
    pred_boxes = modify_pred_boxes(pred_boxes)
    for i,box in enumerate(pred_boxes):
        label = 'section'
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})    
  
    dict_file = {"filename": img_name,"size":size,"regions":regions,"file_attributes":{}}
    return dict_file    

def via_detector_project_json(img_paths):

    """ 
    Given an list of image paths (Should be in the same folder) return the corresponding via json file
    
    Input :
    - list of image paths

    Output:
    - Return json file that VIA gets as input
    """
    files_list = []
    dict_file = {}
    for img_path in img_paths:
        # Default file_path of the image
        size = os.stat(img_path).st_size  
        dict_file[os.path.basename(img_path) + str(size)] = via_detector_file_dict(img_path)
        filename = os.path.basename(img_path)
        files_list.append(filename + str(os.stat(img_path).st_size))
    default_filepath = './'
    options = {"section":'',"price":'',"name":'',"description":'','category':'','dietary':''}
    via_project = {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":True,"show_image_policy":"all"},"image":{"region_label":"regions","region_color":"regions","region_label_font":"8px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":default_filepath},"project":{"name":"pdf"}},"_via_img_metadata": dict_file,"_via_attributes":{"region":{"regions":{"type":"radio","description":"","options":options,"default_options":{"section":True}}},"file":{}},"_via_data_format_version":"2.0.10","_via_image_id_list":files_list}
    return via_project

def via_file_dict(img_path):
    """
    For an image return a dictionnary given the information for this image in the way of via displays it

    Input :
    - img_path : path of the image

    Output :
    -dict_file
    """
    
    dict_file = {}
    img_name = img_path.split('/')[-1]
    size = os.stat(img_path).st_size
    boxes,txts,scores = get_ocr_txts_boxes_scores(img_path)
    labels = get_all_label_list(txts)

    regions = []
    for i,box in enumerate(boxes):
        label = labels[i]
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})
    dict_file['label'] = {"filename": img_name,"size":size,"regions":regions,"file_attributes":{}}

    img = detector_image_transformation(img_path,boxes)
    
    #model.load_state_dict(torch.load(args_item["model"]))
    model = torch.load(item_model)
    print(type(model))
    try:
        pred_boxes, _, _ = get_prediction(model,img, confidence=item_conf)
    except:
        pred_boxes = []
    pred_boxes = modify_pred_boxes(pred_boxes)
    regions = []
    for i,box in enumerate(pred_boxes):
        label = 'item'
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})    


    model = torch.load(section_model)
    print(type(model))
    try:
        pred_boxes, _, _ = get_prediction(model,img, confidence=section_conf)
    except:
        pred_boxes = []
    pred_boxes = modify_pred_boxes(pred_boxes)
    for i,box in enumerate(pred_boxes):
        label = 'section'
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})    
 
    
    
    dict_file['detector'] =  {"filename": img_name,"size":size,"regions":regions,"file_attributes":{}}
    
   
    return dict_file  


def via_label_file_dict(img_path):
    """
    For an image return a dictionnary given the information for this image in the way of via displays it

    Input :
    - img_path : path of the image

    Output :
    -dict_file
    """
    img_name = img_path.split('/')[-1]
    size = os.stat(img_path).st_size

    boxes,txts,scores = get_ocr_txts_boxes_scores(img_path)
    # When we will get the label
    labels = get_all_label_list(txts)

    regions = []
    for i,box in enumerate(boxes):
        label = labels[i]
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})
    dict_file = {"filename": img_name,"size":size,"regions":regions,"file_attributes":{}}
    return dict_file




def via_project_json(img_paths,project_name):

    """ 
    Given an list of image paths (Should be in the same folder) return the corresponding via json file
    
    Input :
    - list of image paths

    Output:
    - Return json file that VIA gets as input
    """
    via_project = {}
    files_list = []
    dict_file = {'label':{},'detector':{}}
    for img_path in img_paths:
        via_dict_file = via_file_dict(img_path)
        filename = os.path.basename(img_path)
        files_list.append(filename + str(os.stat(img_path).st_size))
        for key in ['label','detector']:
        # Default file_path of the image
            size = os.stat(img_path).st_size  
            dict_file[key][os.path.basename(img_path) + str(size)] = via_dict_file[key] 
    default_filepath = './'
    options = {"section":'',"price":'',"name":'',"description":'','category':'','item':'','modifier':'','dietary':''}
    for key in ['label','detector']:
        via_project[key] =  {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":True,"show_image_policy":"all"},"image":{"region_label":"regions","region_color":"regions","region_label_font":"8px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":default_filepath},"project":{"name":key + '_' + project_name }},"_via_img_metadata": dict_file[key],"_via_attributes":{"region":{"regions":{"type":"radio","description":"","options":options,"default_options":{"section":True}}},"file":{}},"_via_data_format_version":"2.0.10","_via_image_id_list":files_list}
    
    return via_project
def via_label_project_json(img_paths):

    """ 
    Given an list of image paths (Should be in the same folder) return the corresponding via json file
    
    Input :
    - list of image paths

    Output:
    - Return json file that VIA gets as input
    """
    files_list = []
    dict_file = {}
    for img_path in img_paths:
        # Default file_path of the image
        size = os.stat(img_path).st_size  
        dict_file[os.path.basename(img_path) + str(size)] = via_label_file_dict(img_path)
        filename = os.path.basename(img_path)
        files_list.append(filename + str(os.stat(img_path).st_size))
    default_filepath = './'
    options = {"section":'',"price":'',"name":'',"description":'','category':'','modifier':'','dietary':''}
    via_project = {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":True,"show_image_policy":"all"},"image":{"region_label":"regions","region_color":"regions","region_label_font":"8px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":default_filepath},"project":{"name":"menu"}},"_via_img_metadata": dict_file,"_via_attributes":{"region":{"regions":{"type":"radio","description":"","options":options,"default_options":{"section":True}}},"file":{}},"_via_data_format_version":"2.0.10","_via_image_id_list":files_list}
    return via_project





def save_via_label_project_json(json_name,img_paths):
    """
    Save a json file for a list of images which are in the same folder

    Input :
    json_name : the name of the json file
    img_paths : list of path of images

    Output :
    None
    """
    via_project = via_label_project_json(img_paths)
    json_object = json.dumps(via_project, indent=0,separators=  (',',':') )

    # Writing to sample.json
    with open('/'.join(img_paths[0].split('/')[0:-1]) + '/'+ json_name, "w") as outfile:
        outfile.write(json_object)

def save_via_detector_project_json(json_name,img_paths):
    """
    Save a json file for a list of images which are in the same folder

    Input :
    json_name : the name of the json file with .json at the end
    img_paths : list of path of images

    Output :
    None
    """
    via_project = via_detector_project_json(img_paths)
    json_object = json.dumps(via_project, indent=0,separators=  (',',':') )

    # Writing to sample.json
    with open('/'.join(img_paths[0].split('/')[0:-1]) + '/'+ json_name, "w") as outfile:
        outfile.write(json_object)
def save_via_folder_projet(pdf_path,output_path):
    """
    Save in a temp folder a json file an the corresponding image from a PDF
    Input :
    -pdf_path : path to the PDF
    -output_path : where we store the temporary folder

    Ouput :
    None
    """
    folder_temp = output_path
    
    # Create folder temp

    # if os.path.exists(folder_temp):
    #     shutil.rmtree(folder_temp)
    # os.makedirs(folder_temp)
    
    pdf_to_image_from_path(root_name = get_file_name(pdf_path),input_path = pdf_path,output_path = folder_temp )
    img_paths = [os.path.join(folder_temp, filename) for filename in os.listdir(folder_temp) if 'jpg' in filename ]
    via_project = via_project_json(img_paths,get_file_name(pdf_path))
    #via_label_project_json(img_paths)
    
    # Label
    via_label_project = via_project['label']
    
    #via_label_project = via_label_project_json(img_paths)
    via_label_json_object = json.dumps(via_label_project, indent=0,separators=  (',',':') )
    # Writing to sample.json
    with open(output_path + '/via_label_project_pdf.json', "w") as outfile:
        outfile.write(via_label_json_object)
    # Detector
    #via_detector_project = via_detector_project_json(img_paths)
    via_detector_project = via_project['detector']
    via_detector_json_object = json.dumps(via_detector_project, indent=0,separators=  (',',':') )
    # Writing to sample.json
    with open(output_path + '/via_detector_project_pdf.json', "w") as outfile:
        outfile.write(via_detector_json_object)




if __name__== "__main__":
    
    img_path = './demo/0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf_page_1.jpg'
    img_path_2 = './demo/0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf_page_2.jpg'

    print(via_file_dict(img_path))
