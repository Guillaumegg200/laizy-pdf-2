from utils import *
from detector.predict import *



def transform_folder(DIRIN,DIROUT):
    """
    Given a DIRIN folder where there are images will save those images in another folder DIROUT by applying a transformation for the detector

    Input :
    -DIRIN : path of the inout folder
    -DIROUT path of the out put folder

    Output :
    None

    """
    for filename in os.listdir(DIRIN):
        img_path = os.path.join(DIRIN, filename)
        # checking if it is a file
        if 'jpg' in img_path or 'png' in img_path:
            if not os.path.exists(DIROUT + filename):
                green_merge = detector_image_transformation_from_path(img_path)
                green_merge.save(os.path.join(DIROUT, filename))

def via_detector_dataset_file_dict(img_path):
    """
    For an image return a dictionnary given the information for this image in the way of via displays it

    Input :
    - img_path : path of the image

    Output :
    -dict_file
    """
    
    
    img_name = img_path.split('/')[-1]
    size = os.stat(img_path).st_size

    regions = []

    # model = torch.load(item_model)
    # print(img_path)
    # try:
    #     pred_boxes, _, _ = get_prediction_from_path(model,img_path, confidence = item_conf)
    #     pred_boxes = modify_pred_boxes(pred_boxes)
    # except:
    #     pred_boxes=[]
    # for i,box in enumerate(pred_boxes):
    #     label = 'item'
    #     region_attributes = {"regions":label}        
    #     left, top, width, height = box[0],box[1],box[2],box[3]
    #     regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})    
    
    
    model = torch.load(section_model)

    try:
        pred_boxes, _, _ = get_prediction_from_path(model,img_path, confidence = item_conf)
        pred_boxes = modify_pred_boxes(pred_boxes)
    except:
        pred_boxes=[]
    for i,box in enumerate(pred_boxes):
        label = 'section'
        region_attributes = {"regions":label}        
        left, top, width, height = box[0],box[1],box[2],box[3]
        regions.append({"shape_attributes":{"name":"rect","x":left,"y":top,"width": width,"height":height},"region_attributes":region_attributes})    
 
    dict_file = {"filename": img_name,"size":size,"regions":regions,"file_attributes":{}}
    return dict_file  

def via_detector_dataset_project_json(img_paths):

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
        dict_file[os.path.basename(img_path) + str(size)] = via_detector_dataset_file_dict(img_path)
        filename = os.path.basename(img_path)
        files_list.append(filename + str(os.stat(img_path).st_size))
    default_filepath = './'
    options = {"section":'',"price":'',"name":'',"description":'','category':'','item':''}
    via_project = {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":True,"show_image_policy":"all"},"image":{"region_label":"regions","region_color":"regions","region_label_font":"8px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":default_filepath},"project":{"name":"pdf"}},"_via_img_metadata": dict_file,"_via_attributes":{"region":{"regions":{"type":"radio","description":"","options":options,"default_options":{"section":True}}},"file":{}},"_via_data_format_version":"2.0.10","_via_image_id_list":files_list}
    return via_project

def save_via_detector_datset_project_json(json_name,img_paths):
    """
    Save a json file for a list of images which are in the same folder

    Input :
    json_name : the name of the json file with .json at the end
    img_paths : list of path of images

    Output :
    None
    """
    via_project = via_detector_dataset_project_json(img_paths)
    json_object = json.dumps(via_project, indent=0,separators=  (',',':') )

    # Writing to sample.json
    with open('/'.join(img_paths[0].split('/')[0:-1]) + '/'+ json_name, "w") as outfile:
        outfile.write(json_object)

def join_via_json_project(json_1,json_2):
    """
    Given 2 json files from VIA application the function merge them in json_1 and return the merged json

    Input :
    json_1 : json via project
    json_2 : json via project

    return json
    
    """
    for filename in json_2["_via_image_id_list"]:
        dict_file = json_2["_via_img_metadata"][filename]
        json_1["_via_image_id_list"].append(filename)
        json_1["_via_img_metadata"][filename] = dict_file
    return json_1
def via_annotation_to_project(json_annotations):
    """
    Given a json file for annotation transform it into a project

    Input : json that you download from via ti get annotations

    Output :
    via json that you can upload on via

    """

    dict_file = json_annotations
    files_list = json_annotations.keys()
    default_filepath = './'
    options = {"section":'',"price":'',"name":'',"description":'','category':'','item':'','modifier':'','dietary':''}
    json_project = {"_via_settings":{"ui":{"annotation_editor_height":25,"annotation_editor_fontsize":0.8,"leftsidebar_width":18,"image_grid":{"img_height":80,"rshape_fill":"none","rshape_fill_opacity":0.3,"rshape_stroke":"yellow","rshape_stroke_width":2,"show_region_shape":True,"show_image_policy":"all"},"image":{"region_label":"regions","region_color":"regions","region_label_font":"8px Sans","on_image_annotation_editor_placement":"NEAR_REGION"}},"core":{"buffer_size":"18","filepath":{},"default_filepath":default_filepath},"project":{"name":"menu"}},"_via_img_metadata": dict_file,"_via_attributes":{"region":{"regions":{"type":"radio","description":"","options":options,"default_options":{"section":True}}},"file":{}},"_via_data_format_version":"2.0.10","_via_image_id_list":files_list}
    return json_project
def split_json_detector(json):
    """
    Given a json from via containing annotations from section and item split into 2 jsons
    Input : json annotations from VIA

    Output:
    2 dictionnaries 
    """
    dict_item, dict_section = {},{}

    for filename in json.keys():
        dict_temp = json[filename].copy()
        if [region for region in json[filename]["regions"] if region["region_attributes"]["regions"] == "section"]!=[]:
            dict_temp["regions"] = [region for region in json[filename]["regions"] if region["region_attributes"]["regions"] == "section"]
            dict_section[filename] = dict_temp
        dict_temp = json[filename].copy()
        if [region for region in json[filename]["regions"] if region["region_attributes"]["regions"] == "item"]!=[]:
            dict_temp["regions"] = [region for region in json[filename]["regions"] if region["region_attributes"]["regions"] == "item"]
            dict_item[filename] = dict_temp
    print('item',dict_item)
    print('dict_section',dict_section)
    return dict_item,dict_section


if __name__=='__main__':
    for type in ['item','section']:
        for set in ['train','val']:
            data =json.load(open('./detector/Dataset copy/via_' + type + '_' + set + '.json'))
            data_new =json.load(open('./detector/Dataset copy/new_' + set + '_' + type + '.json'))
            via_project = join_via_json_project(data,data_new)
            json_object = json.dumps(via_project, indent=0,separators=  (',',':') )
            # Writing to sample.json
            with open('./detector/Dataset copy/via_' + type + '_' + set + '_joined.json', "w") as outfile:
                outfile.write(json_object)
    #Fro the new val dataset
    # transform_folder('./New/Images val','./New/val')
    # For the new train dataset
    #transform_folder('./New/Images train','./New/train')

    #save_via_detector_datset_project_json('new_train_dataset_item.json',[f for f in glob.glob('./New/train/*')])
    #save_via_detector_datset_project_json('new_train_dataset_section.json',[f for f in glob.glob('./New/train/*')])
    # save_via_detector_datset_project_json('new_val_dataset_item.json',[f for f in glob.glob('./New/val/*')])
    #save_via_detector_datset_project_json('new_val_dataset_section.json',[f for f in glob.glob('./New/val/*')])
    pass