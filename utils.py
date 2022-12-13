# Common librairies
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# Import paddleocr
from paddleocr import PaddleOCR,draw_ocr
import os
import glob
# For images
from PIL import Image 
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
# For files
from pdf2image import convert_from_path
from streamlit.components.v1 import html
import glob, sys, fitz


import json
import shutil, random, os
import xlsxwriter
from zipfile import ZipFile

from os.path import basename
# Load model
import pickle
import string
# Import from get_label
from get_label import *
#from modify_via_json import *
# For text cleasing
import re
import nltk
# from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import unicodedata

# Text Cleansing 
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
# STOPWORDS = set(stopwords.words('english'))

# Remove words that are in NLTK stopwords list that we want to keep
not_stopwords = {'below', 'above'} 
# STOPWORDS = set([word for word in STOPWORDS if word not in not_stopwords])


# Import the english library for paddleocr
ocr = PaddleOCR(use_angle_cls = True, lang = 'en')
#from pdf2jpg import pdf2jpg

def get_file_name(filepath):
    print(os.path.splitext(os.path.basename(filepath))[0])
    return os.path.splitext(os.path.basename(filepath))[0]

def pdf_to_image_from_path(root_name,input_path,output_path):
    """
    Convert a PDF into images. Split the PDF by page and save the image in a specific path into the format JPEG
    Save PDF pages as "output_name + "_page*.jpg"

    Input :
    - output_name : main_name of the images
    - input_path : path to the PDF
    - output_path : path where we save the images

    Output :
    None

    
    """
    # To get better resolution
    zoom_x = 2.0  # horizontal zoom
    zoom_y = 2.0  # vertical zoom
    mat = fitz.Matrix(1, 1)  # zoom factor 2 in each dimension

    doc = fitz.open(input_path)  # open document
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        

        pix.save(output_path + '/' + root_name + "_page_%i.jpg" % page.number) 





def ocr_results(img_path):
    """ 
    From the path of an image return the result given by ocr for this image

    Input :
    - img_path : path to the image in input

    Output :

    - result : dict containing boxes, texts and scores of all lines detected in the image
    """

    # return ocr results from the path of an image
    result = ocr.ocr(img_path,cls=True)
    return result


def get_ocr_txts_boxes_scores(img_path):
    """
    From the path of an image return all the texts, boxes and scores given by ocr for this image

    Input :
    - img_path : path to the image in input

    Output :

    - (boxes,txts,scores) : list containing respectively the coordinates of all boxes detected, the texts inside those boxes and the confidence score of every detection
    - boxes[i] is a list of four element which are [left,top,width,height]
    
    """
    # get result from ocr
    result = ocr_results(img_path)

    #Boxes detected but are in this format [(x1,y1),(x2,y2),...]
    boxes = [line[0] for line in result]
    # Convert boxes into (left,top,right,bottom)
    boxes =  modify_boxes(boxes)
    #Text detected inside the boxes
    txts = [line[1][0] for line in result]
    #Confidence score of the detection
    scores = [line[1][1] for line in result]

    return (boxes,txts,scores)

def modify_boxes(boxes):
    """
    Modify boxes from ocr to give for every box [left,top,width,height]
    
    Input :
    boxes : list of coordinates from ocr

    Output :
    list of boxes [left,top,width,height]
    """
    for i,box in enumerate(boxes):
            left, top, right, bottom = int(min(box[0][0],box[3][0])),int(min(box[0][1],box[1][1])),int(max(box[1][0],box[2][0])),int(max(box[2][1],box[3][1]))
            boxes[i] = [left, top, right-left, bottom-top ]
    return boxes

def modify_pred_boxes(boxes):
    """
    Modify boxes from ML model to give for every box [left,top,width,height]
    
    Input :
    boxes : list of coordinates from ocr

    Output :
    list of boxes [left,top,width,height]
    """
    for i,box in enumerate(boxes):
            left, top, right, bottom = int(box[0][0]),int(box[0][1]),int(box[1][0]),int(box[1][1])
            boxes[i] = [left, top, right-left, bottom-top ]
    return boxes


def draw_ocr_boxes(img_path):
    """
    Draw boxes around detected texts of an image

    Input : 
    - path of the image

    Output : 
    None

    """
    
    boxes,_,_ = get_ocr_txts_boxes_scores(img_path)
    image = cv2.imread(img_path)
    im_show = draw_ocr(image, boxes, None,None)
    
    display(im_show)

def read_json(json_path):  
    """
    Read a json file

    Input :
    -json path

    Output :
    json file as a dictionnary

    """
    # Opening JSON file
    f = open(json_path)
    # returns JSON object as a dictionary
    return json.load(f)


def detector_image_transformation_from_path(img_path):
    """
    To perform model detector we need to transform input images by applying a blck backgroung on which we add boxes of texts normalized as green

    Input :
    -img_path : path of the image

    Output :
    - green_merge : transformed image

    """
    boxes,_,_ = get_ocr_txts_boxes_scores(img_path)
    
    image = cv2.imread(img_path)
    # Create a image where the background is black and boudinx boxes white
    square=np.zeros(image.shape[:2])
    for box in boxes:
        left, top, w, h = box[0],box[1],box[2],box[3]
        square[int(top):int(top + h), int(left):int(left + w)]=255
    square_img = Image.fromarray(square)
    square_img=square_img.convert("RGB")
    # Copy previous text in the white boxes
    im = Image.open(img_path)
    for box in boxes:
        left, top, w, h = box[0],box[1],box[2],box[3]
        region = im.crop((left,top,left + w,top + h))
        square_img.paste(region, (left,top))
    red, green, blue = square_img.split()
    zeroed_band = red.point(lambda _: 0)
    green_merge = Image.merge( "RGB", (zeroed_band, green, zeroed_band))
    return green_merge
def detector_image_transformation(img_path,boxes):
    """
    To perform model detector we need to transform input images by applying a blck backgroung on which we add boxes of texts normalized as green

    Input :
    -img_path : path of the image

    Output :
    - green_merge : transformed image

    """
    
    image = cv2.imread(img_path)
    # Create a image where the background is black and boudinx boxes white
    square=np.zeros(image.shape[:2])
    for box in boxes:
        left, top, w, h = box[0],box[1],box[2],box[3]
        square[int(top):int(top + h), int(left):int(left + w)]=255
    square_img = Image.fromarray(square)
    square_img=square_img.convert("RGB")
    # Copy previous text in the white boxes
    im = Image.open(img_path)
    for box in boxes:
        left, top, w, h = box[0],box[1],box[2],box[3]
        region = im.crop((left,top,left + w,top + h))
        square_img.paste(region, (left,top))
    red, green, blue = square_img.split()
    zeroed_band = red.point(lambda _: 0)
    green_merge = Image.merge( "RGB", (zeroed_band, green, zeroed_band))
    return green_merge


def read_via_project_from_path(via_project_json_path):
    """
    Given a via project json file and the path of the folder containing all the image in this json_file return a dictionnary de pandaDataframe with labels, and boxes in all the image and the keys are the name of the images

    Input :
    DIT : folder path containing images of the json
    via_json_path : json from via containing labels of the boxes

    Ourput:
    res : dictionnary of pd
    
    """
    via_label_json_dict = read_json(via_project_json_path)
    res = {}
    
    for file in via_label_json_dict["_via_img_metadata"]:
        labels,boxes = [],[]
        filename = via_label_json_dict["_via_img_metadata"][file]['filename']
        for region in (via_label_json_dict["_via_img_metadata"][file]['regions']):
            label = region['region_attributes']['regions']
            x,y,w,h = region['shape_attributes']['x'],region['shape_attributes']['y'],region['shape_attributes']['width'],region['shape_attributes']['height']
            box = [x,y,w,h]
            boxes.append(box)
            labels.append(label)
        res[filename] = {'labels':labels,'boxes':boxes}
    return res




def create_folder_zip(dirName,folder_name):
    """
    Create a zip folder given the path of this folder and save it as sampleDir.zip
    """
    # create a ZipFile object
    with ZipFile(folder_name, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, basename(filePath))

def clean_text(text):
    """
        text: a string
        
        return: modified initial string
    """
    text = BeautifulSoup(text,features="html").text # HTML decoding
    text = text.lower() # Lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # Replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # Delete symbols which are in BAD_SYMBOLS_RE from text
#     text = ' '.join(word for word in text.split() if word not in STOPWORDS) # Delete stopwords from text
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore') # Normalise text

    return text

def draw_boxes_from_json(DIR,via_project_json_path):
    """

    Input :
    DIR : path where images of the json files are
    via_project_json_path : json files project
    """
    dict = read_via_project_from_path(via_project_json_path)
    image_list = []
    colors = {'price':'green','section':'orange','name':'blue','description':'purple','category':'yellow','item':'red','modifier':'black'}
    for filename in dict:
        image = Image.open( DIR + '/' + filename)
        draw = ImageDraw.Draw(image)
        for i,box in enumerate(list(dict[filename]['boxes'])):
            x,y,w,h = box[0],box[1],box[2],box[3]
            label = dict[filename]['labels'][i]
            draw.rectangle((x, y, x+w, y+h),width = 3, outline=colors[label])
        image_list.append(image)
    return image_list

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo



def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)


if __name__== "__main__":
    
    # img_path = './demo/0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf_page_1.jpg'
    # pdf_path = './demo/0016F00003jELMVBarkingDogHotel_97783642_05.11.2020BarkingDogMenu1.pdf'
    # save_via_folder_projet(pdf_path,'./temp')
    #draw_boxes_from_json('./temp','./temp/via_project_label_pdf.json')    
    #print(ocr_results('./temp/TewantinNoosaRSL5009q000001W4cR_118523277_SUMMERMENU2022_page_1.jpg'))
    pass